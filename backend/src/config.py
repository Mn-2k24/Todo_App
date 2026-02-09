"""Application configuration management."""

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database Configuration
    database_url: str = Field(
        ...,
        description="PostgreSQL database connection URL",
        json_schema_extra={"env": "DATABASE_URL"},
    )

    # JWT Configuration
    jwt_secret: str = Field(
        ...,
        min_length=32,
        description="JWT signing secret (minimum 32 characters)",
        json_schema_extra={"env": "JWT_SECRET"},
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT signing algorithm",
        json_schema_extra={"env": "JWT_ALGORITHM"},
    )
    jwt_expiration_hours: int = Field(
        default=1,
        ge=1,
        le=24,
        description="JWT token expiration time in hours",
        json_schema_extra={"env": "JWT_EXPIRATION_HOURS"},
    )

    # Better Auth Configuration
    better_auth_secret: str = Field(
        ...,
        min_length=32,
        description="Better Auth shared secret (minimum 32 characters)",
        json_schema_extra={"env": "BETTER_AUTH_SECRET"},
    )

    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins",
        json_schema_extra={"env": "CORS_ORIGINS"},
    )

    # Application Configuration
    app_name: str = Field(
        default="Todo App",
        description="Application name",
        json_schema_extra={"env": "APP_NAME"},
    )
    app_version: str = Field(
        default="2.0.0",
        description="Application version",
        json_schema_extra={"env": "APP_VERSION"},
    )
    debug: bool = Field(
        default=False,
        description="Debug mode (enables verbose logging)",
        json_schema_extra={"env": "DEBUG"},
    )

    # Phase III: Gemini API Configuration
    gemini_api_key: str = Field(
        ...,
        min_length=1,
        description="Google Gemini API key for Phase III AI chatbot",
        json_schema_extra={"env": "GEMINI_API_KEY"},
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate and convert PostgreSQL URL to async driver."""
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql+asyncpg://"):
            return v
        else:
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'"
            )

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings singleton

    Example:
        from src.config import get_settings

        settings = get_settings()
        print(settings.app_name)
    """
    return Settings()  # type: ignore
