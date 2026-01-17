"""
Anthropic Claude API Client Template

A production-ready client for integrating Claude API into your applications.
Includes error handling, retry logic, streaming, and cost tracking.
"""

import os
import logging
import time
from typing import Optional, Iterator, List, Dict, Any
from dataclasses import dataclass
from anthropic import Anthropic, AsyncAnthropic, RateLimitError, APIError

logger = logging.getLogger(__name__)


@dataclass
class UsageMetrics:
    """Track API usage and costs."""
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0

    # Pricing per 1K tokens (update as needed)
    INPUT_COST_PER_1K: float = 0.003
    OUTPUT_COST_PER_1K: float = 0.015

    def add_request(self, input_tokens: int, output_tokens: int):
        """Record usage from a request."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.requests += 1

    @property
    def total_cost(self) -> float:
        """Calculate total cost in USD."""
        input_cost = (self.input_tokens / 1000) * self.INPUT_COST_PER_1K
        output_cost = (self.output_tokens / 1000) * self.OUTPUT_COST_PER_1K
        return input_cost + output_cost

    def summary(self) -> Dict[str, Any]:
        """Get usage summary."""
        return {
            "requests": self.requests,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.input_tokens + self.output_tokens,
            "total_cost_usd": round(self.total_cost, 4)
        }


class ClaudeClient:
    """
    Production-ready Anthropic Claude API client.

    Features:
    - Automatic retries with exponential backoff
    - Streaming support
    - Cost tracking
    - Error handling
    - Multi-turn conversations
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        temperature: float = 1.0,
        max_retries: int = 3,
        timeout: float = 60.0
    ):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            max_retries: Max retry attempts on rate limits
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key, timeout=timeout)
        self.async_client = AsyncAnthropic(api_key=self.api_key, timeout=timeout)

        # Configuration
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.max_retries = max_retries

        # Metrics
        self.metrics = UsageMetrics()

        logger.info(f"Initialized ClaudeClient with model: {model}")

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate a text response from Claude.

        Args:
            prompt: User message/prompt
            system: System prompt (optional)
            max_tokens: Override default max_tokens
            temperature: Override default temperature

        Returns:
            Generated text response

        Raises:
            APIError: If API request fails after retries
        """
        messages = [{"role": "user", "content": prompt}]

        response = self._create_message_with_retry(
            messages=messages,
            system=system,
            max_tokens=max_tokens or self.max_tokens,
            temperature=temperature or self.temperature
        )

        # Track usage
        self.metrics.add_request(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )

        return response.content[0].text

    def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> Iterator[str]:
        """
        Stream response from Claude.

        Args:
            prompt: User message/prompt
            system: System prompt (optional)
            max_tokens: Override default max_tokens

        Yields:
            Text chunks as they arrive

        Raises:
            APIError: If streaming fails
        """
        messages = [{"role": "user", "content": prompt}]

        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=self.temperature,
                system=system,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text

                # Track usage after stream completes
                final_message = stream.get_final_message()
                self.metrics.add_request(
                    input_tokens=final_message.usage.input_tokens,
                    output_tokens=final_message.usage.output_tokens
                )

        except Exception as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Multi-turn conversation.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system: System prompt (optional)
            max_tokens: Override default max_tokens

        Returns:
            Assistant's response

        Example:
            messages = [
                {"role": "user", "content": "Hello!"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "How are you?"}
            ]
            response = client.chat(messages)
        """
        response = self._create_message_with_retry(
            messages=messages,
            system=system,
            max_tokens=max_tokens or self.max_tokens,
            temperature=self.temperature
        )

        # Track usage
        self.metrics.add_request(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )

        return response.content[0].text

    def _create_message_with_retry(self, **kwargs):
        """
        Create message with exponential backoff retry on rate limits.

        Args:
            **kwargs: Arguments to pass to messages.create()

        Returns:
            Message response

        Raises:
            APIError: If request fails after max retries
        """
        backoff_factor = 2.0

        for attempt in range(self.max_retries):
            try:
                return self.client.messages.create(
                    model=self.model,
                    **kwargs
                )

            except RateLimitError as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Rate limit exceeded after {self.max_retries} retries")
                    raise

                wait_time = backoff_factor ** attempt
                logger.warning(
                    f"Rate limit hit (attempt {attempt + 1}/{self.max_retries}), "
                    f"retrying in {wait_time}s"
                )
                time.sleep(wait_time)

            except APIError as e:
                logger.error(f"API error: {e}", exc_info=True)
                raise

    async def generate_async(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Async version of generate().

        Args:
            prompt: User message/prompt
            system: System prompt (optional)
            max_tokens: Override default max_tokens

        Returns:
            Generated text response
        """
        messages = [{"role": "user", "content": prompt}]

        try:
            response = await self.async_client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=self.temperature,
                system=system,
                messages=messages
            )

            # Track usage
            self.metrics.add_request(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Async generation error: {e}", exc_info=True)
            raise

    def get_usage_summary(self) -> Dict[str, Any]:
        """
        Get usage metrics summary.

        Returns:
            Dictionary with usage statistics and costs
        """
        return self.metrics.summary()

    def reset_metrics(self):
        """Reset usage metrics."""
        self.metrics = UsageMetrics()
        logger.info("Metrics reset")


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Initialize client
    client = ClaudeClient()

    # Simple generation
    print("=== Simple Generation ===")
    response = client.generate("What is the capital of France?")
    print(response)

    # With system prompt
    print("\n=== With System Prompt ===")
    response = client.generate(
        "Write a haiku about coding",
        system="You are a poetic programming expert"
    )
    print(response)

    # Streaming
    print("\n=== Streaming ===")
    for chunk in client.generate_stream("Count from 1 to 5"):
        print(chunk, end="", flush=True)
    print()

    # Multi-turn conversation
    print("\n=== Conversation ===")
    messages = [
        {"role": "user", "content": "My name is Alice"},
        {"role": "assistant", "content": "Nice to meet you, Alice!"},
        {"role": "user", "content": "What's my name?"}
    ]
    response = client.chat(messages)
    print(response)

    # Usage summary
    print("\n=== Usage Summary ===")
    print(client.get_usage_summary())
