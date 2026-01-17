"""JWT token creation and verification utilities."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import UUID

from jose import JWTError, jwt

from src.config import get_settings

settings = get_settings()


def create_access_token(
    user_id: UUID,
    email: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token for authenticated user.

    Args:
        user_id: User's unique identifier
        email: User's email address
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token

    Example:
        token = create_access_token(
            user_id=user.id,
            email=user.email
        )
    """
    if expires_delta is None:
        expires_delta = timedelta(hours=settings.jwt_expiration_hours)

    expire = datetime.utcnow() + expires_delta

    # JWT claims per constitution requirements
    to_encode: Dict[str, Any] = {
        "sub": str(user_id),  # Subject: user ID
        "email": email,  # User email for convenience
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at
        "type": "access",  # Token type
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )

    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode JWT token.

    Args:
        token: JWT token string

    Returns:
        Dict[str, Any]: Decoded token payload

    Raises:
        JWTError: If token is invalid, expired, or malformed

    Example:
        try:
            payload = verify_token(token)
            user_id = UUID(payload["sub"])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        # Validate required claims
        if payload.get("sub") is None:
            raise JWTError("Token missing 'sub' claim")

        if payload.get("exp") is None:
            raise JWTError("Token missing 'exp' claim")

        return payload

    except JWTError as e:
        # Re-raise with context
        raise JWTError(f"Token verification failed: {str(e)}")


def extract_user_id_from_token(token: str) -> UUID:
    """Extract and validate user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        UUID: User ID from token

    Raises:
        JWTError: If token is invalid or user_id cannot be extracted

    Example:
        user_id = extract_user_id_from_token(token)
    """
    payload = verify_token(token)
    user_id_str = payload.get("sub")

    if not user_id_str:
        raise JWTError("Token does not contain user ID")

    try:
        return UUID(user_id_str)
    except (ValueError, AttributeError) as e:
        raise JWTError(f"Invalid user ID format in token: {str(e)}")
