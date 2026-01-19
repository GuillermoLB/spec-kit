"""Tests for configuration management."""

import pytest
import os
from src.config import Config, get_config, reset_config


def test_config_loads_from_env():
    """Test configuration loads from environment variables."""
    os.environ["ANTHROPIC_API_KEY"] = "test-key-123"
    os.environ["MODEL_NAME"] = "custom-model"
    os.environ["TEMPERATURE"] = "0.5"
    os.environ["MAX_TOKENS"] = "2000"

    reset_config()
    config = get_config()

    assert config.anthropic_api_key == "test-key-123"
    assert config.model_name == "custom-model"
    assert config.temperature == 0.5
    assert config.max_tokens == 2000


def test_config_defaults():
    """Test configuration uses defaults when env vars not set."""
    os.environ.pop("MODEL_NAME", None)
    os.environ.pop("TEMPERATURE", None)

    reset_config()
    config = get_config()

    assert config.model_name == "claude-sonnet-4-5-20250929"
    assert config.temperature == 1.0


def test_config_validation_missing_api_key():
    """Test validation fails when API key is missing."""
    os.environ.pop("ANTHROPIC_API_KEY", None)

    reset_config()
    config = get_config()

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not set"):
        config.validate()


def test_config_validation_invalid_temperature():
    """Test validation fails for invalid temperature."""
    os.environ["TEMPERATURE"] = "3.0"

    reset_config()
    config = get_config()

    with pytest.raises(ValueError, match="TEMPERATURE must be between"):
        config.validate()


def test_config_validation_invalid_max_tokens():
    """Test validation fails for invalid max tokens."""
    os.environ["MAX_TOKENS"] = "10000"

    reset_config()
    config = get_config()

    with pytest.raises(ValueError, match="MAX_TOKENS must be between"):
        config.validate()


def test_config_singleton():
    """Test that get_config returns the same instance."""
    reset_config()
    config1 = get_config()
    config2 = get_config()

    assert config1 is config2


def test_reset_config():
    """Test that reset_config clears the singleton."""
    config1 = get_config()
    reset_config()
    config2 = get_config()

    assert config1 is not config2
