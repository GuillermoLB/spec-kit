"""Main CLI entry point for AI chatbot.

This module provides the interactive command-line interface for
chatting with Claude using streaming responses.
"""

import sys
import argparse
import anthropic
from typing import Optional

from src.config import get_config, reset_config
from src.chat import AnthropicClient, ConversationManager, StreamingHandler
from src.utils import CostTracker, UI


class ChatBot:
    """Interactive chatbot with streaming responses."""

    def __init__(self, debug: bool = False, show_stats: bool = True):
        """Initialize chatbot.

        Args:
            debug: Enable debug mode
            show_stats: Show statistics after session
        """
        self.debug = debug
        self.show_stats_on_exit = show_stats
        self.ui = UI()

        try:
            config = get_config()
            config.validate()

            self.client = AnthropicClient()
            self.conversation = ConversationManager()
            self.streaming = StreamingHandler()
            self.cost_tracker = CostTracker()
            self.model_name = config.model_name

        except ValueError as e:
            self.ui.show_error(str(e))
            sys.exit(1)

    def run(self) -> None:
        """Run the interactive chat loop."""
        self.ui.show_welcome(self.model_name)

        try:
            while True:
                # Get user input
                try:
                    user_input = self.ui.show_user_prompt()
                except (EOFError, KeyboardInterrupt):
                    self.ui.show_newline()
                    break

                # Handle commands
                if not user_input.strip():
                    continue

                command = user_input.strip().lower()

                if command in ["quit", "exit"]:
                    break

                elif command == "clear":
                    self.conversation.clear()
                    self.ui.show_info("Conversation cleared")
                    continue

                elif command == "stats":
                    stats = self.cost_tracker.get_stats()
                    self.ui.show_stats(stats)
                    continue

                # Add user message to conversation
                try:
                    self.conversation.add_user_message(user_input)
                except ValueError as e:
                    self.ui.show_error(str(e))
                    continue

                # Check if history was trimmed
                if self.conversation.was_trimmed():
                    self.ui.show_warning(
                        "Trimmed old messages to fit context window"
                    )

                # Get and stream response
                try:
                    self._stream_response()
                except KeyboardInterrupt:
                    self.ui.show_newline()
                    self.ui.show_warning("Response cancelled")
                    # Remove the incomplete exchange
                    if self.conversation.get_message_count() > 0:
                        self.conversation.messages.pop()  # Remove user message
                    continue
                except anthropic.RateLimitError as e:
                    self.ui.show_error(str(e))
                    # Remove the user message since we couldn't respond
                    if self.conversation.get_message_count() > 0:
                        self.conversation.messages.pop()
                    continue
                except anthropic.APIError as e:
                    self.ui.show_error(str(e))
                    # Remove the user message since we couldn't respond
                    if self.conversation.get_message_count() > 0:
                        self.conversation.messages.pop()
                    continue
                except Exception as e:
                    self.ui.show_error(f"Unexpected error: {str(e)}")
                    if self.debug:
                        raise
                    # Remove the user message since we couldn't respond
                    if self.conversation.get_message_count() > 0:
                        self.conversation.messages.pop()
                    continue

        finally:
            # Show final stats if enabled
            if self.show_stats_on_exit and self.cost_tracker.message_count > 0:
                self.ui.show_newline()
                stats = self.cost_tracker.get_stats()
                self.ui.show_stats(stats)

    def _stream_response(self) -> None:
        """Stream a response from the API."""
        messages = self.conversation.get_messages()
        system_prompt = self.conversation.get_system_prompt()

        # Reset streaming handler
        self.streaming.reset()

        # Create stream
        stream = self.client.create_stream(
            messages=messages,
            system=system_prompt
        )

        # Display assistant prefix
        self.ui.show_assistant_prefix()

        # Process and display stream
        for chunk in self.streaming.process_stream(stream):
            self.ui.show_streaming_text(chunk)

        self.ui.show_newline()
        self.ui.show_newline()

        # Get the full response and add to conversation
        full_response = self.streaming.get_full_text()
        self.conversation.add_assistant_message(full_response)

        # Track usage
        usage = self.streaming.get_usage()
        self.cost_tracker.add_usage(
            usage["input_tokens"],
            usage["output_tokens"]
        )


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Chatbot using Claude API"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--no-stats",
        action="store_true",
        help="Don't show statistics on exit"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Override model name (e.g., claude-opus-4-5-20251101)"
    )

    args = parser.parse_args()

    # Override model if specified
    if args.model:
        import os
        os.environ["MODEL_NAME"] = args.model
        reset_config()

    # Create and run chatbot
    chatbot = ChatBot(
        debug=args.debug,
        show_stats=not args.no_stats
    )
    chatbot.run()


if __name__ == "__main__":
    main()
