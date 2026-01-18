"""Application configuration.

This module manages application settings using pydantic-settings.
Configuration is loaded from environment variables or .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings.

    All settings can be configured via environment variables.
    Default values are provided for development.

    Attributes:
        database_url: SQLAlchemy database connection URL
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        cors_origins: List of allowed CORS origins (comma-separated in env)

    Example .env file:
        DATABASE_URL=sqlite:///./todos.db
        LOG_LEVEL=INFO
        CORS_ORIGINS=http://localhost:3000,http://localhost:8080
    """

    # Database configuration
    database_url: str = "sqlite:///./todos.db"

    # Logging configuration
    log_level: str = "INFO"

    # CORS configuration (comma-separated origins)
    cors_origins: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string.

        Returns:
            List of origin URLs, or ["*"] if none configured

        Example:
            CORS_ORIGINS="http://localhost:3000,http://localhost:8080"
            -> ["http://localhost:3000", "http://localhost:8080"]
        """
        if not self.cors_origins:
            return ["*"]  # Allow all origins in development
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Uses lru_cache to create a singleton Settings instance,
    avoiding repeated file reads and parsing.

    Returns:
        Settings instance

    Example:
        from src.config import get_settings
        settings = get_settings()
        print(settings.database_url)
    """
    return Settings()
