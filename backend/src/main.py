"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.database import init_db
from src.utils.errors import AppException

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup: Initialize database (optional, use Alembic in production)
    if settings.debug:
        await init_db()

    yield

    # Shutdown: cleanup if needed
    pass


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Full-Stack Todo Web Application with Multi-user Support",
    debug=settings.debug,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for custom app exceptions
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )


# Health check endpoint
@app.get(
    "/health",
    tags=["Health"],
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: Application health status
    """
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
    }


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    response_model=dict,
)
async def root() -> dict:
    """Root endpoint with API information.

    Returns:
        dict: API information
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


# Register API routers
from src.api import auth, tasks

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"],
)

app.include_router(
    tasks.router,
    prefix="/api/tasks",
    tags=["Tasks"],
)
