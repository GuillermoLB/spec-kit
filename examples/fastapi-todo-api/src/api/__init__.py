"""API routers for the Todo API.

This package contains all API endpoint implementations.
"""

from src.api.todos import router as todos_router

__all__ = ["todos_router"]
