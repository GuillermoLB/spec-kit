"""Anthropic API client wrapper.

This module provides a clean interface to the Anthropic Claude API
with streaming support and error handling.
"""

import anthropic
from typing import Dict, List, Iterator, Any
from src.config import get_config


class AnthropicClient:
    """Wrapper for Anthropic API client.

    Provides streaming chat completions with proper error handling.
    """

    def __init__(self, api_key: str | None = None):
        """Initialize the Anthropic client.

        Args:
            api_key: Optional API key (uses config if not provided)
        """
        config = get_config()
        self.api_key = api_key or config.anthropic_api_key

        if not self.api_key:
            raise ValueError("Anthropic API key is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = config.model_name
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    def create_stream(
        self,
        messages: List[Dict[str, str]],
        system: str | None = None
    ) -> Iterator[Any]:
        """Create a streaming chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system: Optional system prompt

        Yields:
            Message stream events from the API

        Raises:
            anthropic.APIError: If API request fails
            anthropic.RateLimitError: If rate limit is exceeded
        """
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": messages,
                "stream": True,
            }

            if system:
                kwargs["system"] = system

            with self.client.messages.stream(**kwargs) as stream:
                for event in stream:
                    yield event

        except anthropic.RateLimitError as e:
            # Extract retry-after if available
            retry_after = getattr(e, "retry_after", None)
            if retry_after:
                raise anthropic.RateLimitError(
                    f"Rate limit exceeded. Please wait {retry_after} seconds."
                ) from e
            raise

        except anthropic.APIError as e:
            raise anthropic.APIError(
                f"API Error: {e.__class__.__name__} - {str(e)}"
            ) from e

    def get_usage(self, stream) -> Dict[str, int]:
        """Get token usage from a completed stream.

        Args:
            stream: Completed message stream

        Returns:
            Dict with input_tokens and output_tokens counts
        """
        try:
            final_message = stream.get_final_message()
            return {
                "input_tokens": final_message.usage.input_tokens,
                "output_tokens": final_message.usage.output_tokens,
            }
        except Exception:
            return {"input_tokens": 0, "output_tokens": 0}
