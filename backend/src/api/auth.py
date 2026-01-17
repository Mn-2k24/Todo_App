"""Authentication API endpoints.

Implements the OpenAPI contract defined in plan.md contracts/auth.yaml:
- POST /api/auth/register - User registration
- POST /api/auth/login - User login
- POST /api/auth/logout - User logout (client-side only for stateless backend)
"""

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from uuid import UUID
from sqlmodel import select

from src.database import get_session
from src.schemas.auth import AuthResponse, LoginRequest, LogoutResponse, RegisterRequest
from src.services.auth_service import authenticate_user, register_user
from src.auth.jwt import verify_token
from src.models.user import User, UserPublic

router = APIRouter()


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account and return JWT token",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "email": "user@example.com",
                            "created_at": "2026-01-09T12:00:00Z",
                        },
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        400: {
            "description": "Invalid input (email format, password length)",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Invalid input",
                        "code": "INVALID_INPUT",
                        "status": 400,
                    }
                }
            },
        },
        409: {
            "description": "Email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "error": "An account with this email already exists",
                        "code": "EMAIL_EXISTS",
                        "status": 409,
                    }
                }
            },
        },
    },
)
async def register(
    register_data: RegisterRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """Register new user account.

    - Validates email format and password strength (min 8 chars)
    - Checks for duplicate email addresses
    - Hashes password with bcrypt
    - Creates user record in database
    - Sets httpOnly cookie with JWT token for secure authentication
    - Returns user info (token also in response for API clients)

    Args:
        register_data: User registration data (email, password)
        response: FastAPI response object for setting cookies
        session: Database session (injected)

    Returns:
        AuthResponse: User info and JWT token

    Raises:
        HTTPException 400: Invalid input (handled by Pydantic)
        HTTPException 409: Email already exists (handled by ConflictError)
    """
    auth_response = await register_user(register_data, session)

    # Set httpOnly cookie for secure browser-based authentication
    response.set_cookie(
        key="todo_app_token",
        value=auth_response.token,
        httponly=True,        # Prevents JavaScript access (XSS protection)
        secure=False,         # Set True for HTTPS in production (False for local HTTP dev)
        samesite="lax",       # CSRF protection
        max_age=24 * 60 * 60, # 24 hours (matches JWT_EXPIRATION_HOURS)
        path="/",
    )

    return auth_response


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user and return JWT token",
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "email": "user@example.com",
                            "created_at": "2026-01-09T12:00:00Z",
                        },
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        400: {
            "description": "Invalid input",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Invalid input",
                        "code": "INVALID_INPUT",
                        "status": 400,
                    }
                }
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Invalid email or password",
                        "code": "INVALID_CREDENTIALS",
                        "status": 401,
                    }
                }
            },
        },
    },
)
async def login(
    login_data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> AuthResponse:
    """Login existing user.

    - Validates email and password
    - Verifies credentials against database
    - Sets httpOnly cookie with JWT token for secure authentication
    - Returns user info (token also in response for API clients)

    Args:
        login_data: User login data (email, password)
        response: FastAPI response object for setting cookies
        session: Database session (injected)

    Returns:
        AuthResponse: User info and JWT token

    Raises:
        HTTPException 401: Invalid email or password (handled by UnauthorizedError)
    """
    auth_response = await authenticate_user(login_data, session)

    # Set httpOnly cookie for secure browser-based authentication
    # JWT_EXPIRATION_HOURS is 24 hours = 86400 seconds
    response.set_cookie(
        key="todo_app_token",
        value=auth_response.token,
        httponly=True,        # Prevents JavaScript access (XSS protection)
        secure=False,         # Set True for HTTPS in production (False for local HTTP dev)
        samesite="lax",       # CSRF protection
        max_age=24 * 60 * 60, # 24 hours (matches JWT_EXPIRATION_HOURS)
        path="/",
    )

    return auth_response


@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout user",
    description="Logout user and clear httpOnly cookie",
    responses={
        200: {
            "description": "Logout successful",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Successfully logged out",
                    }
                }
            },
        },
    },
)
async def logout(response: Response) -> LogoutResponse:
    """Logout user and clear httpOnly cookie.

    Clears the httpOnly cookie containing the JWT token and returns success message.
    The frontend should also:
    1. Clear user session data from localStorage
    2. Redirect to home or login page

    Args:
        response: FastAPI response object for clearing cookies

    Returns:
        LogoutResponse: Success message
    """
    # Clear the httpOnly cookie by setting it with max_age=0
    response.delete_cookie(
        key="todo_app_token",
        path="/",
        samesite="lax",
    )

    return LogoutResponse(message="Successfully logged out")


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get currently authenticated user from JWT cookie",
    responses={
        200: {
            "description": "Current user retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "user": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "email": "user@example.com",
                            "created_at": "2026-01-09T12:00:00Z",
                        }
                    }
                }
            },
        },
        401: {
            "description": "Not authenticated or invalid token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated",
                    }
                }
            },
        },
    },
)
async def get_me(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """Get current authenticated user from JWT cookie.

    Reads JWT token from httpOnly cookie and returns user information.
    Used by frontend to validate authentication state.

    Args:
        request: FastAPI request object (to read cookies)
        session: Database session (injected)

    Returns:
        dict: User information

    Raises:
        HTTPException 401: If no token or invalid token
    """
    # Get token from cookie
    token = request.cookies.get("todo_app_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        # Verify token and extract payload
        payload = verify_token(token)
        user_id_str = payload.get("sub")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Convert to UUID
        try:
            user_id = UUID(user_id_str)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # Fetch user from database
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Return user data
    return {
        "user": UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        )
    }
