"""Tests for conversation management."""

import pytest
from src.chat.conversation import ConversationManager


def test_add_user_message():
    """Test adding user message to conversation."""
    conv = ConversationManager(max_turns=5)

    conv.add_user_message("Hello!")

    messages = conv.get_messages()
    assert len(messages) == 1
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello!"


def test_add_assistant_message():
    """Test adding assistant message to conversation."""
    conv = ConversationManager(max_turns=5)

    conv.add_user_message("Hello!")
    conv.add_assistant_message("Hi there!")

    messages = conv.get_messages()
    assert len(messages) == 2
    assert messages[1]["role"] == "assistant"
    assert messages[1]["content"] == "Hi there!"


def test_add_empty_message_raises_error():
    """Test that adding empty message raises ValueError."""
    conv = ConversationManager(max_turns=5)

    with pytest.raises(ValueError, match="cannot be empty"):
        conv.add_user_message("")

    with pytest.raises(ValueError, match="cannot be empty"):
        conv.add_user_message("   ")


def test_message_count():
    """Test message count tracking."""
    conv = ConversationManager(max_turns=5)

    assert conv.get_message_count() == 0

    conv.add_user_message("Hello")
    assert conv.get_message_count() == 1

    conv.add_assistant_message("Hi")
    assert conv.get_message_count() == 2


def test_turn_count():
    """Test turn count tracking."""
    conv = ConversationManager(max_turns=5)

    assert conv.get_turn_count() == 0

    conv.add_user_message("Hello")
    assert conv.get_turn_count() == 1

    conv.add_assistant_message("Hi")
    assert conv.get_turn_count() == 1  # Still 1 turn

    conv.add_user_message("How are you?")
    assert conv.get_turn_count() == 2


def test_history_trimming():
    """Test conversation history is trimmed when max turns exceeded."""
    conv = ConversationManager(max_turns=2)

    # Add 3 turns (6 messages)
    conv.add_user_message("Message 1")
    conv.add_assistant_message("Response 1")
    conv.add_user_message("Message 2")
    conv.add_assistant_message("Response 2")
    conv.add_user_message("Message 3")
    conv.add_assistant_message("Response 3")

    # Should keep only last 2 turns (4 messages)
    messages = conv.get_messages()
    assert len(messages) == 4
    assert conv.get_turn_count() == 2

    # First message should be "Message 2"
    assert messages[0]["content"] == "Message 2"


def test_system_prompt():
    """Test system prompt management."""
    conv = ConversationManager(max_turns=5)

    assert conv.get_system_prompt() is None

    conv.set_system_prompt("You are a helpful assistant")
    assert conv.get_system_prompt() == "You are a helpful assistant"


def test_clear_conversation():
    """Test clearing conversation history."""
    conv = ConversationManager(max_turns=5)

    conv.add_user_message("Hello")
    conv.add_assistant_message("Hi")
    assert conv.get_message_count() == 2

    conv.clear()
    assert conv.get_message_count() == 0
    assert len(conv.get_messages()) == 0


def test_was_trimmed():
    """Test detecting when history was trimmed."""
    conv = ConversationManager(max_turns=2)

    conv.add_user_message("Message 1")
    assert not conv.was_trimmed()

    conv.add_assistant_message("Response 1")
    conv.add_user_message("Message 2")
    conv.add_assistant_message("Response 2")
    assert conv.was_trimmed()

    # Adding one more turn should keep trim status
    conv.add_user_message("Message 3")
    conv.add_assistant_message("Response 3")
    assert conv.was_trimmed()
