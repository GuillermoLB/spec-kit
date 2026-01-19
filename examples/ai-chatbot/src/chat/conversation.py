"""Conversation management for multi-turn chat.

This module handles conversation history, context trimming,
and message formatting.
"""

from typing import Dict, List
from src.config import get_config


class ConversationManager:
    """Manages conversation history and context.

    Maintains message history with automatic trimming to stay
    within context limits.
    """

    def __init__(self, max_turns: int | None = None):
        """Initialize conversation manager.

        Args:
            max_turns: Maximum number of conversation turns to keep
                      (uses config default if not provided)
        """
        config = get_config()
        self.max_turns = max_turns or config.max_context_turns
        self.messages: List[Dict[str, str]] = []
        self.system_prompt: str | None = None

    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation.

        Args:
            content: User message content
        """
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")

        self.messages.append({
            "role": "user",
            "content": content.strip()
        })
        self._trim_history()

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the conversation.

        Args:
            content: Assistant message content
        """
        self.messages.append({
            "role": "assistant",
            "content": content
        })
        self._trim_history()

    def set_system_prompt(self, prompt: str) -> None:
        """Set or update the system prompt.

        Args:
            prompt: System prompt content
        """
        self.system_prompt = prompt

    def get_messages(self) -> List[Dict[str, str]]:
        """Get current message history.

        Returns:
            List of message dictionaries
        """
        return self.messages.copy()

    def get_system_prompt(self) -> str | None:
        """Get the system prompt.

        Returns:
            System prompt or None
        """
        return self.system_prompt

    def clear(self) -> None:
        """Clear conversation history."""
        self.messages = []

    def get_message_count(self) -> int:
        """Get number of messages in conversation.

        Returns:
            Message count
        """
        return len(self.messages)

    def get_turn_count(self) -> int:
        """Get number of conversation turns (user+assistant pairs).

        Returns:
            Turn count
        """
        # Count user messages as turns
        return sum(1 for msg in self.messages if msg["role"] == "user")

    def _trim_history(self) -> bool:
        """Trim conversation history to stay within max turns.

        Returns:
            True if history was trimmed, False otherwise
        """
        turn_count = self.get_turn_count()

        if turn_count <= self.max_turns:
            return False

        # Calculate how many messages to remove
        # We remove pairs of messages (user + assistant)
        turns_to_remove = turn_count - self.max_turns

        # Remove oldest turn pairs
        messages_to_remove = turns_to_remove * 2

        # Make sure we don't remove more than we have
        if messages_to_remove >= len(self.messages):
            messages_to_remove = len(self.messages) - 2  # Keep at least last exchange

        if messages_to_remove > 0:
            self.messages = self.messages[messages_to_remove:]
            return True

        return False

    def was_trimmed(self) -> bool:
        """Check if history was trimmed on last message addition.

        Returns:
            True if last operation trimmed history
        """
        return self.get_turn_count() == self.max_turns
