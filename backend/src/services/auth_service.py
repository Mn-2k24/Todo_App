"""Authentication service with user registration and login logic."""

import logging
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.jwt import create_access_token
from src.models.user import User, UserPublic
from src.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from src.utils.errors import ConflictError, UnauthorizedError

# Configure logger
logger = logging.getLogger(__name__)

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password

    Example:
        hashed = hash_password("SecurePassword123")
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        bool: True if password matches

    Example:
        if verify_password(input_password, user.password_hash):
            # Password correct
            pass
    """
    return pwd_context.verify(plain_password, hashed_password)


async def register_user(
    register_data: RegisterRequest,
    session: AsyncSession,
) -> AuthResponse:
    """Register new user and return auth response with JWT token.

    Args:
        register_data: Registration request data
        session: Database session

    Returns:
        AuthResponse: User info and JWT token

    Raises:
        ConflictError: If email already exists

    Example:
        response = await register_user(
            RegisterRequest(email="user@example.com", password="password123"),
            session
        )
    """
    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == register_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ConflictError(
            message="An account with this email already exists",
            code="EMAIL_EXISTS",
        )

    # Hash password
    password_hash = hash_password(register_data.password)

    # Create new user
    new_user = User(
        email=register_data.email,
        name=register_data.name,
        password_hash=password_hash,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Create JWT token
    token = create_access_token(
        user_id=new_user.id,
        email=new_user.email,
    )

    # Return auth response
    return AuthResponse(
        user=UserPublic(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            created_at=new_user.created_at,
        ),
        token=token,
    )


async def authenticate_user(
    login_data: LoginRequest,
    session: AsyncSession,
) -> AuthResponse:
    """Authenticate user and return auth response with JWT token.

    Args:
        login_data: Login request data
        session: Database session

    Returns:
        AuthResponse: User info and JWT token

    Raises:
        UnauthorizedError: If email not found or password incorrect

    Example:
        response = await authenticate_user(
            LoginRequest(email="user@example.com", password="password123"),
            session
        )
    """
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    # Check if user exists and password is correct
    if not user:
        # Log failed login attempt - user not found (FR-054)
        logger.warning(
            "Failed login attempt: User not found",
            extra={"email": login_data.email, "reason": "user_not_found"},
        )
        raise UnauthorizedError(
            message="Invalid email or password",
            code="INVALID_CREDENTIALS",
        )

    if not verify_password(login_data.password, user.password_hash):
        # Log failed login attempt - incorrect password (FR-054)
        logger.warning(
            "Failed login attempt: Incorrect password",
            extra={"email": login_data.email, "reason": "incorrect_password"},
        )
        raise UnauthorizedError(
            message="Invalid email or password",
            code="INVALID_CREDENTIALS",
        )

    # Create JWT token
    token = create_access_token(
        user_id=user.id,
        email=user.email,
    )

    # Return auth response
    return AuthResponse(
        user=UserPublic(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
        ),
        token=token,
    )


async def get_user_by_email(
    email: str,
    session: AsyncSession,
) -> Optional[User]:
    """Get user by email address.

    Args:
        email: User email
        session: Database session

    Returns:
        Optional[User]: User if found, None otherwise

    Example:
        user = await get_user_by_email("user@example.com", session)
    """
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()
