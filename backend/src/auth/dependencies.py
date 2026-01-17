"""FastAPI authentication dependencies for route protection."""

from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.jwt import verify_token
from src.database import get_session
from src.models.user import User

# HTTP Bearer token scheme for Authorization header (auto_error=False allows cookie fallback)
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    """Get currently authenticated user from JWT token.

    This dependency:
    1. Extracts JWT token from Authorization header OR httpOnly cookie
    2. Verifies token signature and expiration
    3. Extracts user_id from token claims
    4. Fetches user from database
    5. Returns User object for use in route handlers

    Args:
        request: FastAPI request object (to read cookies)
        credentials: Optional HTTP Bearer credentials from Authorization header
        session: Database session

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException: 401 if token is invalid, expired, or user not found

    Example:
        @app.get("/me")
        async def get_me(current_user: User = Depends(get_current_user)):
            return current_user
    """
    # Extract token from Authorization header or httpOnly cookie
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Fallback to httpOnly cookie
        token = request.cookies.get("todo_app_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Verify token and extract payload
        payload = verify_token(token)
        user_id_str: Optional[str] = payload.get("sub")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert to UUID
        try:
            user_id = UUID(user_id_str)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch user from database
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_id(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> UUID:
    """Get current user ID from JWT token without database lookup.

    Faster alternative to get_current_user when only user ID is needed.

    Args:
        request: FastAPI request object (to read cookies)
        credentials: Optional HTTP Bearer credentials from Authorization header

    Returns:
        UUID: User ID from token

    Raises:
        HTTPException: 401 if token is invalid or expired

    Example:
        @app.get("/tasks")
        async def get_tasks(user_id: UUID = Depends(get_current_user_id)):
            # Use user_id for database filtering
            pass
    """
    # Extract token from Authorization header or httpOnly cookie
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Fallback to httpOnly cookie
        token = request.cookies.get("todo_app_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = verify_token(token)
        user_id_str: Optional[str] = payload.get("sub")

        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            return UUID(user_id_str)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
