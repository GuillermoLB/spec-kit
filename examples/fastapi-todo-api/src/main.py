"""FastAPI Todo API - Main Application.

This is the entry point for the FastAPI Todo API example.
It demonstrates spec-driven development using spec-kit.

Run with:
    uvicorn src.main:app --reload

API docs available at:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.config import get_settings
from src.database import init_db
from src.api import todos_router

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    This function runs on startup and shutdown.
    Initializes database tables on startup.

    Args:
        app: FastAPI application instance
    """
    # Startup: Initialize database
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")

    yield

    # Shutdown: Cleanup if needed
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="A simple Todo API demonstrating spec-driven development with spec-kit",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    todos_router,
    prefix="/api/v1",
    tags=["todos"]
)


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint.

    Returns API status to verify the service is running.

    Returns:
        dict: Health status

    Example:
        GET /health
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}


@app.get("/", tags=["root"])
async def root():
    """Root endpoint.

    Returns welcome message and links to documentation.

    Returns:
        dict: Welcome message and docs links
    """
    return {
        "message": "Welcome to Todo API - Spec-driven development example",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1/todos"
    }
