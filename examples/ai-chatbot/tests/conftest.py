"""Pytest fixtures and test configuration.

This module provides shared fixtures for testing with mocked API responses.
"""

import pytest
import os
from unittest.mock import Mock, MagicMock
from typing import List, Dict


@pytest.fixture(scope="function", autouse=True)
def reset_env():
    """Reset environment variables before each test."""
    # Set test environment variables
    os.environ["ANTHROPIC_API_KEY"] = "test-api-key-12345"
    os.environ["MODEL_NAME"] = "claude-sonnet-4-5-20250929"
    os.environ["TEMPERATURE"] = "1.0"
    os.environ["MAX_TOKENS"] = "4096"
    os.environ["MAX_CONTEXT_TURNS"] = "10"

    # Reset config before each test
    from src.config import reset_config
    reset_config()

    yield

    # Cleanup
    reset_config()


@pytest.fixture
def mock_stream_events():
    """Create mock streaming events.

    Returns:
        List of mock streaming events
    """
    events = []

    # Message start event
    start_event = Mock()
    start_event.type = "message_start"
    start_event.message = Mock()
    start_event.message.usage = Mock()
    start_event.message.usage.input_tokens = 15
    events.append(start_event)

    # Content block start
    block_start = Mock()
    block_start.type = "content_block_start"
    events.append(block_start)

    # Content deltas (text chunks)
    for text in ["Hello", " ", "there", "!", " ", "How", " ", "can", " ", "I", " ", "help", "?"]:
        delta_event = Mock()
        delta_event.type = "content_block_delta"
        delta_event.delta = Mock()
        delta_event.delta.text = text
        events.append(delta_event)

    # Message delta with usage
    delta_event = Mock()
    delta_event.type = "message_delta"
    delta_event.usage = Mock()
    delta_event.usage.output_tokens = 13
    events.append(delta_event)

    # Content block stop
    block_stop = Mock()
    block_stop.type = "content_block_stop"
    events.append(block_stop)

    # Message stop
    stop_event = Mock()
    stop_event.type = "message_stop"
    events.append(stop_event)

    return events


@pytest.fixture
def mock_anthropic_client(mock_stream_events):
    """Create a mocked Anthropic client.

    Args:
        mock_stream_events: Mock streaming events fixture

    Returns:
        Mocked Anthropic client
    """
    mock_client = MagicMock()

    # Mock the stream context manager
    mock_stream = MagicMock()
    mock_stream.__enter__ = Mock(return_value=iter(mock_stream_events))
    mock_stream.__exit__ = Mock(return_value=False)

    # Mock the messages.stream method
    mock_client.messages.stream = Mock(return_value=mock_stream)

    return mock_client


@pytest.fixture
def sample_messages() -> List[Dict[str, str]]:
    """Create sample conversation messages.

    Returns:
        List of message dictionaries
    """
    return [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
        {"role": "user", "content": "Tell me about Python"},
    ]


@pytest.fixture
def mock_config():
    """Create a mock configuration object.

    Returns:
        Mock configuration
    """
    mock_cfg = Mock()
    mock_cfg.anthropic_api_key = "test-api-key"
    mock_cfg.model_name = "claude-sonnet-4-5-20250929"
    mock_cfg.temperature = 1.0
    mock_cfg.max_tokens = 4096
    mock_cfg.max_context_turns = 10
    mock_cfg.input_token_cost = 3.00 / 1_000_000
    mock_cfg.output_token_cost = 15.00 / 1_000_000
    mock_cfg.show_stats = True
    mock_cfg.debug = False
    return mock_cfg
