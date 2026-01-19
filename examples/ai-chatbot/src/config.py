"""Configuration management for AI chatbot.

This module handles environment variables and application settings.
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration.

    Loads settings from environment variables with sensible defaults.
    """

    def __init__(self):
        """Initialize configuration from environment variables."""
        # API Configuration
        self.anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

        # Model Configuration
        self.model_name: str = os.getenv(
            "MODEL_NAME",
            "claude-sonnet-4-5-20250929"
        )
        self.temperature: float = float(os.getenv("TEMPERATURE", "1.0"))
        self.max_tokens: int = int(os.getenv("MAX_TOKENS", "4096"))

        # Context Management
        self.max_context_turns: int = int(os.getenv("MAX_CONTEXT_TURNS", "10"))

        # Cost Tracking (Claude Sonnet 4.5 pricing - Jan 2026)
        self.input_token_cost: float = 3.00 / 1_000_000  # $3 per million
        self.output_token_cost: float = 15.00 / 1_000_000  # $15 per million

        # CLI Settings
        self.show_stats: bool = os.getenv("SHOW_STATS", "true").lower() == "true"
        self.debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    def validate(self) -> None:
        """Validate configuration.

        Raises:
            ValueError: If required configuration is missing or invalid
        """
        if not self.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not set. "
                "Please set it in your .env file. "
                "See .env.example for setup instructions."
            )

        if self.temperature < 0 or self.temperature > 2:
            raise ValueError(f"TEMPERATURE must be between 0 and 2, got {self.temperature}")

        if self.max_tokens < 1 or self.max_tokens > 8192:
            raise ValueError(f"MAX_TOKENS must be between 1 and 8192, got {self.max_tokens}")

        if self.max_context_turns < 1:
            raise ValueError(f"MAX_CONTEXT_TURNS must be at least 1, got {self.max_context_turns}")


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance.

    Returns:
        Config: Application configuration
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reset_config() -> None:
    """Reset global configuration (useful for testing)."""
    global _config
    _config = None
