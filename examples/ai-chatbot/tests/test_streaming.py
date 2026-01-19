"""Tests for streaming response handler."""

import pytest
from unittest.mock import Mock
from src.chat.streaming import StreamingHandler


def test_process_stream(mock_stream_events):
    """Test processing a stream of events."""
    handler = StreamingHandler()

    chunks = list(handler.process_stream(iter(mock_stream_events)))

    # Should get text chunks
    expected_text = "Hello there! How can I help?"
    assert "".join(chunks) == expected_text
    assert handler.get_full_text() == expected_text


def test_get_usage(mock_stream_events):
    """Test extracting usage information from stream."""
    handler = StreamingHandler()

    list(handler.process_stream(iter(mock_stream_events)))

    usage = handler.get_usage()
    assert usage["input_tokens"] == 15
    assert usage["output_tokens"] == 13


def test_reset_handler():
    """Test resetting handler state."""
    handler = StreamingHandler()

    # Process a stream
    mock_events = [
        Mock(type="content_block_delta", delta=Mock(text="Hello")),
        Mock(type="message_stop")
    ]
    list(handler.process_stream(iter(mock_events)))

    assert handler.get_full_text() == "Hello"

    # Reset
    handler.reset()

    assert handler.get_full_text() == ""
    assert handler.get_usage() == {"input_tokens": 0, "output_tokens": 0}


def test_empty_stream():
    """Test handling an empty stream."""
    handler = StreamingHandler()

    mock_events = [
        Mock(type="message_start", message=Mock(usage=Mock(input_tokens=5))),
        Mock(type="message_stop")
    ]

    chunks = list(handler.process_stream(iter(mock_events)))

    assert chunks == []
    assert handler.get_full_text() == ""


def test_stream_with_only_deltas():
    """Test stream with only content deltas."""
    handler = StreamingHandler()

    mock_events = [
        Mock(type="content_block_delta", delta=Mock(text="First")),
        Mock(type="content_block_delta", delta=Mock(text=" ")),
        Mock(type="content_block_delta", delta=Mock(text="Second")),
        Mock(type="message_stop")
    ]

    chunks = list(handler.process_stream(iter(mock_events)))

    assert "".join(chunks) == "First Second"
    assert handler.get_full_text() == "First Second"


def test_multiple_streams_with_reset():
    """Test processing multiple streams with reset between."""
    handler = StreamingHandler()

    # First stream
    mock_events1 = [
        Mock(type="content_block_delta", delta=Mock(text="First")),
        Mock(type="message_stop")
    ]
    list(handler.process_stream(iter(mock_events1)))
    assert handler.get_full_text() == "First"

    # Reset for second stream
    handler.reset()

    # Second stream
    mock_events2 = [
        Mock(type="content_block_delta", delta=Mock(text="Second")),
        Mock(type="message_stop")
    ]
    list(handler.process_stream(iter(mock_events2)))
    assert handler.get_full_text() == "Second"
