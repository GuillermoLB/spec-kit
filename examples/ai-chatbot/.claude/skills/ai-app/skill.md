---
name: ai-app
description: LLM integration patterns for building AI-powered applications with Anthropic Claude and OpenAI APIs. Use when integrating Claude or OpenAI APIs, implementing chat features, adding streaming responses, managing multi-turn conversations, implementing prompt engineering, tracking LLM costs, handling rate limits, or building AI-powered features. Includes client setup, error handling, and cost optimization.
---

# AI Application Plugin

This skill provides patterns and best practices for building AI-powered applications with LLM integration (Anthropic Claude, OpenAI).

## LLM Integration Patterns

### 1. Client Setup (Anthropic Claude)

```python
import os
from anthropic import Anthropic, AsyncAnthropic
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Wrapper for Anthropic Claude API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.client = Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)

        # Default configuration
        self.model = "claude-3-5-sonnet-20241022"
        self.max_tokens = 4096
        self.temperature = 1.0

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate a response from Claude.

        Args:
            prompt: User message
            system: System prompt (optional)
            max_tokens: Max tokens to generate
            temperature: Sampling temperature (0-1)

        Returns:
            Generated text response
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
                system=system,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error: {e}", exc_info=True)
            raise

    async def generate_async(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Async version of generate."""
        try:
            response = await self.async_client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                system=system,
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error: {e}", exc_info=True)
            raise
```

### 2. Streaming Responses

```python
def generate_stream(self, prompt: str, system: Optional[str] = None):
    """
    Stream response from Claude.

    Args:
        prompt: User message
        system: System prompt

    Yields:
        Text chunks as they arrive
    """
    try:
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                yield text

    except Exception as e:
        logger.error(f"Claude streaming error: {e}", exc_info=True)
        raise

# Usage example
for chunk in client.generate_stream("Write a poem"):
    print(chunk, end="", flush=True)
```

### 3. Multi-turn Conversations

```python
class ConversationManager:
    """Manages multi-turn conversations with Claude."""

    def __init__(self, client: ClaudeClient, system: Optional[str] = None):
        self.client = client
        self.system = system
        self.messages = []

    def add_user_message(self, content: str):
        """Add a user message to the conversation."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        """Add an assistant message to the conversation."""
        self.messages.append({"role": "assistant", "content": content})

    def generate_reply(self) -> str:
        """
        Generate a reply based on conversation history.

        Returns:
            Assistant's response
        """
        try:
            response = self.client.client.messages.create(
                model=self.client.model,
                max_tokens=self.client.max_tokens,
                system=self.system,
                messages=self.messages
            )

            reply = response.content[0].text
            self.add_assistant_message(reply)
            return reply

        except Exception as e:
            logger.error(f"Conversation error: {e}", exc_info=True)
            raise

# Usage
conversation = ConversationManager(client, system="You are a helpful assistant")
conversation.add_user_message("Hello!")
reply = conversation.generate_reply()
```

## Prompt Engineering Best Practices

### 1. System Prompts

```python
# Good: Clear, specific instructions
SYSTEM_PROMPT = """You are an expert Python developer.
Your responses should:
- Be concise and actionable
- Include code examples when relevant
- Follow PEP 8 style guidelines
- Prioritize readability over cleverness
"""

# Bad: Vague, generic
SYSTEM_PROMPT = "You are helpful."
```

### 2. Few-Shot Prompting

```python
def build_classification_prompt(text: str) -> str:
    """Build a few-shot classification prompt."""
    return f"""Classify the sentiment of the following text as positive, negative, or neutral.

Examples:
Text: "I love this product!"
Sentiment: positive

Text: "This is terrible and doesn't work."
Sentiment: negative

Text: "It arrived on time."
Sentiment: neutral

Text: "{text}"
Sentiment:"""
```

### 3. Structured Outputs

```python
import json
from pydantic import BaseModel

class ExtractedInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str]

def extract_contact_info(text: str) -> ExtractedInfo:
    """Extract contact information using structured output."""
    prompt = f"""Extract contact information from the following text.
Return a JSON object with fields: name, email, phone (optional).

Text: {text}

JSON:"""

    response = client.generate(prompt)

    # Parse JSON response
    try:
        data = json.loads(response)
        return ExtractedInfo(**data)
    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Failed to parse response: {e}")
        raise
```

## Error Handling

### 1. Rate Limiting

```python
import time
from anthropic import RateLimitError

def generate_with_retry(
    client: ClaudeClient,
    prompt: str,
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> str:
    """
    Generate with exponential backoff retry on rate limits.

    Args:
        client: Claude client
        prompt: User prompt
        max_retries: Maximum retry attempts
        backoff_factor: Backoff multiplier

    Returns:
        Generated response
    """
    for attempt in range(max_retries):
        try:
            return client.generate(prompt)

        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise

            wait_time = backoff_factor ** attempt
            logger.warning(f"Rate limit hit, retrying in {wait_time}s")
            time.sleep(wait_time)

        except Exception as e:
            logger.error(f"API error: {e}")
            raise
```

### 2. Token Management

```python
from anthropic import Anthropic

def count_tokens(text: str, client: Anthropic) -> int:
    """
    Count tokens in text (approximation).

    For accurate counting, use the tokenizer API when available.
    """
    # Rough approximation: 1 token ≈ 4 characters
    return len(text) // 4

def truncate_to_token_limit(text: str, max_tokens: int = 100000) -> str:
    """Truncate text to fit within token limit."""
    estimated_tokens = count_tokens(text, None)

    if estimated_tokens <= max_tokens:
        return text

    # Truncate (rough approximation)
    max_chars = max_tokens * 4
    return text[:max_chars]
```

## Cost Tracking

```python
from dataclasses import dataclass
from typing import Dict
import json

@dataclass
class UsageMetrics:
    """Track LLM API usage and costs."""
    input_tokens: int = 0
    output_tokens: int = 0
    requests: int = 0

    # Pricing (as of 2024, update as needed)
    INPUT_COST_PER_1K = 0.003  # Claude 3.5 Sonnet
    OUTPUT_COST_PER_1K = 0.015

    def add_request(self, input_tokens: int, output_tokens: int):
        """Record a single request."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.requests += 1

    @property
    def total_cost(self) -> float:
        """Calculate total cost in USD."""
        input_cost = (self.input_tokens / 1000) * self.INPUT_COST_PER_1K
        output_cost = (self.output_tokens / 1000) * self.OUTPUT_COST_PER_1K
        return input_cost + output_cost

    def to_dict(self) -> Dict:
        """Export metrics as dictionary."""
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "requests": self.requests,
            "total_cost_usd": round(self.total_cost, 4)
        }

# Usage
metrics = UsageMetrics()

response = client.client.messages.create(
    model=client.model,
    max_tokens=1000,
    messages=[{"role": "user", "content": "Hello"}]
)

metrics.add_request(
    input_tokens=response.usage.input_tokens,
    output_tokens=response.usage.output_tokens
)

print(f"Total cost: ${metrics.total_cost:.4f}")
```

## Environment Variables Pattern

```python
from pydantic_settings import BaseSettings

class AISettings(BaseSettings):
    """AI application settings."""

    # API Keys
    anthropic_api_key: str
    openai_api_key: Optional[str] = None

    # Model Configuration
    default_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4096
    temperature: float = 1.0

    # Rate Limiting
    requests_per_minute: int = 50
    max_retries: int = 3

    # Cost Controls
    max_cost_per_request_usd: float = 0.50
    enable_cost_tracking: bool = True

    class Config:
        env_file = ".env"
        env_prefix = "AI_"

# Usage
settings = AISettings()
client = ClaudeClient(api_key=settings.anthropic_api_key)
```

## Testing Patterns

### 1. Mocking LLM Responses

```python
from unittest.mock import Mock, patch
import pytest

@patch('anthropic.Anthropic')
def test_generate(mock_anthropic):
    """Test Claude client with mocked API."""
    # Setup mock
    mock_response = Mock()
    mock_response.content = [Mock(text="Mocked response")]
    mock_anthropic.return_value.messages.create.return_value = mock_response

    # Test
    client = ClaudeClient(api_key="test-key")
    result = client.generate("Test prompt")

    assert result == "Mocked response"
    mock_anthropic.return_value.messages.create.assert_called_once()
```

### 2. Prompt Testing

```python
def test_prompt_template():
    """Test that prompts are formatted correctly."""
    text = "Hello world"
    prompt = build_classification_prompt(text)

    assert "Hello world" in prompt
    assert "Sentiment:" in prompt
    assert "Examples:" in prompt
```

## Security Best Practices

1. **Never commit API keys**: Use environment variables
2. **Validate user input**: Sanitize before including in prompts
3. **Set token limits**: Prevent excessive costs
4. **Monitor usage**: Track costs and set alerts
5. **Implement timeouts**: Prevent hanging requests

```python
# Bad: API key in code
client = Anthropic(api_key="sk-ant-...")

# Good: From environment
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

## Common Patterns Checklist

When integrating LLMs:

- [ ] Store API keys in environment variables
- [ ] Implement error handling and retries
- [ ] Add logging for debugging
- [ ] Track token usage and costs
- [ ] Set appropriate timeouts
- [ ] Validate and sanitize inputs
- [ ] Use structured outputs when possible
- [ ] Test with mocked responses
- [ ] Document prompt templates
- [ ] Monitor for rate limits

---

*Use this skill to build robust, cost-effective AI applications with industry-standard LLM integration patterns.*
