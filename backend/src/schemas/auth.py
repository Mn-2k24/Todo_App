"""Authentication request and response schemas.

These schemas match the OpenAPI contracts defined in plan.md contracts/auth.yaml.
"""

from pydantic import EmailStr, Field
from sqlmodel import SQLModel

from src.models.user import UserPublic


class RegisterRequest(SQLModel):
    """User registration request schema.

    Validates email format, name, and password strength.
    """

    email: EmailStr = Field(
        description="User email address (must be unique)",
        examples=["user@example.com"],
    )
    name: str = Field(
        min_length=2,
        max_length=100,
        description="User's full name (2-100 characters)",
        examples=["John Doe"],
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Password (minimum 8 characters)",
        examples=["SecurePassword123"],
    )


class LoginRequest(SQLModel):
    """User login request schema."""

    email: EmailStr = Field(
        description="User email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        min_length=8,
        max_length=100,
        description="User password",
        examples=["SecurePassword123"],
    )


class AuthResponse(SQLModel):
    """Authentication response schema.

    Returned on successful registration or login.
    """

    user: UserPublic = Field(description="User information (excludes password)")
    token: str = Field(description="JWT access token")
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer')",
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
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


class LogoutResponse(SQLModel):
    """Logout response schema."""

    message: str = Field(
        default="Successfully logged out",
        description="Success message",
    )
