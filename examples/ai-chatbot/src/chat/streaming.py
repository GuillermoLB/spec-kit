"""Streaming response handler.

This module handles real-time streaming of AI responses,
displaying tokens as they arrive.
"""

from typing import Iterator, Any, Dict
import anthropic


class StreamingHandler:
    """Handles streaming responses from the API.

    Processes stream events and yields text content as it arrives.
    """

    def __init__(self):
        """Initialize streaming handler."""
        self.current_text = ""
        self.usage: Dict[str, int] = {
            "input_tokens": 0,
            "output_tokens": 0
        }

    def process_stream(
        self,
        stream: Iterator[Any]
    ) -> Iterator[str]:
        """Process a streaming response.

        Args:
            stream: API stream iterator

        Yields:
            Text content chunks as they arrive

        Raises:
            anthropic.APIError: If stream processing fails
        """
        self.current_text = ""

        try:
            for event in stream:
                # Handle different event types
                if event.type == "content_block_start":
                    continue

                elif event.type == "content_block_delta":
                    # Extract text from delta
                    if hasattr(event.delta, "text"):
                        chunk = event.delta.text
                        self.current_text += chunk
                        yield chunk

                elif event.type == "content_block_stop":
                    continue

                elif event.type == "message_start":
                    # Capture usage info if available
                    if hasattr(event.message, "usage"):
                        self.usage["input_tokens"] = event.message.usage.input_tokens

                elif event.type == "message_delta":
                    # Capture output token usage
                    if hasattr(event, "usage"):
                        self.usage["output_tokens"] = event.usage.output_tokens

                elif event.type == "message_stop":
                    # Stream complete
                    break

        except anthropic.APIError as e:
            raise anthropic.APIError(
                f"Stream processing failed: {str(e)}"
            ) from e

        except Exception as e:
            raise RuntimeError(
                f"Unexpected error during streaming: {str(e)}"
            ) from e

    def get_full_text(self) -> str:
        """Get the complete accumulated text.

        Returns:
            Full response text
        """
        return self.current_text

    def get_usage(self) -> Dict[str, int]:
        """Get token usage from the stream.

        Returns:
            Dict with input_tokens and output_tokens
        """
        return self.usage.copy()

    def reset(self) -> None:
        """Reset handler state for new stream."""
        self.current_text = ""
        self.usage = {"input_tokens": 0, "output_tokens": 0}
