# Feature: AI Chatbot Example

**Status**: Draft
**Owner**: spec-kit development team
**Last Updated**: 2026-01-17
**Priority**: High

## Purpose

Create a complete AI chatbot example using the Claude API that demonstrates spec-kit's ai-app plugin and spec-driven development for LLM-powered applications. This example shows best practices for streaming responses, conversation management, and cost tracking.

## Requirements

- [ ] CLI chatbot interface with interactive conversation
- [ ] Integration with Anthropic Claude API (streaming responses)
- [ ] Multi-turn conversation support with context management
- [ ] Token usage and cost tracking
- [ ] Follows spec-kit directory structure with CLAUDE.md, .claude/skills/, specs/
- [ ] Feature specifications for chat interface, streaming, and cost tracking
- [ ] Comprehensive pytest test suite with mocked LLM responses
- [ ] README with setup instructions and API key configuration
- [ ] Environment variable management (.env support)
- [ ] Error handling for API failures and rate limits

## User Stories

**As a** developer building an AI application
**I want** a reference implementation using the ai-app plugin
**So that** I can see best practices for LLM integration

**As a** new spec-kit user
**I want** to see how specs work for AI features
**So that** I can apply spec-driven development to my AI projects

**As a** chatbot user
**I want** an interactive CLI experience with streaming responses
**So that** I can see the AI's response in real-time

## Acceptance Criteria

1. **Given** I have an Anthropic API key configured
   **When** I run the chatbot
   **Then** I can send messages and receive streaming responses

2. **Given** I'm in a conversation
   **When** I send multiple messages
   **Then** the chatbot maintains context across turns

3. **Given** I use the chatbot
   **When** I send messages
   **Then** token usage and costs are tracked and displayed

4. **Given** I examine the specs/features/ directory
   **When** I read the specifications
   **Then** each spec clearly describes an AI feature with acceptance criteria

5. **Given** I run the test suite
   **When** I execute pytest
   **Then** all tests pass using mocked LLM responses

6. **Given** the API fails or rate limits are hit
   **When** I send a message
   **Then** I receive a clear error message and guidance

## Technical Details

### Architecture

**CLI Chatbot with Anthropic Claude API:**

```
examples/ai-chatbot/
├── CLAUDE.md                      # Spec-kit constitution
├── README.md                      # Example documentation
├── .claude/
│   └── skills/
│       └── ai-app/                # AI app plugin (copied from spec-kit)
│           ├── SKILL.md
│           └── references/
│               ├── anthropic-client.py
│               └── prompt-patterns.md
├── specs/
│   ├── features/
│   │   ├── chat-interface.md      # Spec for CLI chat interface
│   │   ├── streaming-responses.md # Spec for streaming implementation
│   │   ├── conversation-context.md # Spec for multi-turn conversations
│   │   └── cost-tracking.md       # Spec for usage/cost tracking
│   └── architecture.md            # High-level architecture doc
├── src/
│   ├── __init__.py
│   ├── main.py                    # CLI entry point
│   ├── config.py                  # Configuration management
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── client.py              # Anthropic API client
│   │   ├── conversation.py        # Conversation manager
│   │   └── streaming.py           # Streaming response handler
│   └── utils/
│       ├── __init__.py
│       ├── cost_tracker.py        # Token/cost tracking
│       └── ui.py                  # CLI formatting/colors
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures (mocked API)
│   ├── test_client.py             # Test API client
│   ├── test_conversation.py      # Test conversation manager
│   ├── test_streaming.py         # Test streaming
│   └── test_cost_tracking.py     # Test cost calculations
├── .env.example                   # Environment variables template
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
└── .gitignore
```

### Features

**Core Capabilities:**

| Feature | Description |
|---------|-------------|
| Interactive Chat | CLI interface with prompt input and streaming output |
| Streaming | Real-time token-by-token response display |
| Context Management | Multi-turn conversations with message history |
| Cost Tracking | Track tokens (input/output) and estimated costs |
| Error Handling | Graceful handling of API errors, rate limits, network issues |
| Configuration | API key via environment variables |

### Technology Stack

- **LLM Provider**: Anthropic Claude (claude-sonnet-4-5-20250929)
- **SDK**: anthropic Python SDK 0.39+
- **CLI**: Rich library for formatted output
- **Config**: python-dotenv for environment variables
- **Testing**: pytest with unittest.mock for API mocking
- **Async**: asyncio for streaming responses

### Data Flow

```
User Input → CLI
    ↓
Conversation Manager (adds to history)
    ↓
Anthropic Client (API call with streaming)
    ↓
Streaming Handler (yields tokens)
    ↓
CLI Display (real-time output)
    ↓
Cost Tracker (calculate usage)
    ↓
Display summary
```

### Conversation Context

**Message History Format:**

```python
[
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help you today?"},
    {"role": "user", "content": "Tell me about Python"},
    {"role": "assistant", "content": "Python is..."}
]
```

**Context Management:**
- Keep last N turns (configurable, default: 10)
- Trim old messages when context limit approached
- Preserve system message across turns

### Cost Tracking

**Pricing (Claude Sonnet 4.5 - Jan 2026):**
- Input tokens: $3.00 per million tokens
- Output tokens: $15.00 per million tokens

**Tracking:**
```python
{
    "session": {
        "input_tokens": 1250,
        "output_tokens": 850,
        "total_cost": 0.016,  # $0.016
        "message_count": 5
    }
}
```

### Feature Specifications

**Example Spec: Streaming Responses**

```markdown
# Feature: Streaming Responses

**Status**: Implemented
**Owner**: Example Team
**Last Updated**: 2026-01-17

## Purpose
Display AI responses in real-time as tokens are generated, providing better UX than waiting for complete response.

## Requirements
- [ ] Use Anthropic streaming API
- [ ] Display tokens as they arrive
- [ ] Show typing indicator while waiting
- [ ] Handle stream interruptions gracefully
- [ ] Support cancellation (Ctrl+C)

## Acceptance Criteria
1. Given I send a message
   When Claude generates a response
   Then I see tokens appear in real-time

2. Given streaming is in progress
   When I press Ctrl+C
   Then stream stops gracefully without error

3. Given the API connection drops
   When stream is interrupted
   Then I see error message and can retry
```

### README Content

The example README should include:

1. **Overview** - AI chatbot with Claude API using spec-kit
2. **Prerequisites** - Python 3.11+, Anthropic API key
3. **Setup** - API key configuration, install dependencies
4. **Usage** - How to run chatbot, example conversation
5. **Features** - Streaming, context, cost tracking
6. **Testing** - How to run tests with mocked API
7. **Spec-Driven Workflow** - How specs guided development
8. **Cost Information** - Pricing and usage tracking
9. **Extending** - How to add new features

### Security Considerations

- [ ] API key stored in .env file (not committed)
- [ ] .env.example provided without actual keys
- [ ] Input sanitization before sending to API
- [ ] Rate limiting recommendations
- [ ] No logging of API keys
- [ ] User prompts validated for length

## Edge Cases & Error Handling

1. **Edge case**: API key missing or invalid
   - **Message**: "Error: ANTHROPIC_API_KEY not set. See README for setup instructions."
   - **Recovery**: User adds API key to .env file

2. **Edge case**: Rate limit exceeded
   - **Message**: "Rate limit exceeded. Please wait {retry_after} seconds."
   - **Recovery**: Automatic retry with exponential backoff

3. **Error**: Network connection lost during streaming
   - **Message**: "Connection lost. Partial response: [show what was received]"
   - **Recovery**: Offer to retry message

4. **Edge case**: Very long conversation exceeds context limit
   - **Handling**: Automatically trim oldest messages, warn user "Trimmed old messages to fit context window"

5. **Edge case**: User sends empty message
   - **Handling**: Display "Please enter a message" without API call

6. **Error**: API returns error response
   - **Message**: "API Error: {error_type} - {error_message}"
   - **Recovery**: Log full error, show user-friendly message

## Testing Strategy

### Unit Tests

- [ ] Test ConversationManager adds messages correctly
- [ ] Test cost calculator with known token counts
- [ ] Test streaming handler processes chunks
- [ ] Test error handling for each error type

### Integration Tests

- [ ] Test full conversation flow with mocked API
- [ ] Test streaming with mocked chunks
- [ ] Test context trimming with long conversations
- [ ] Test cost tracking across multiple messages

### Mocking Strategy

```python
# Mock Anthropic API responses
@pytest.fixture
def mock_anthropic_client():
    with patch('anthropic.Anthropic') as mock:
        # Mock streaming response
        mock_stream = [
            {"type": "content_block_delta", "delta": {"text": "Hello"}},
            {"type": "content_block_delta", "delta": {"text": " there"}},
            {"type": "message_stop"}
        ]
        mock.return_value.messages.create.return_value = mock_stream
        yield mock
```

### Test Coverage Goals

- Minimum 85% code coverage
- 100% coverage on API client wrapper
- All error paths tested
- Streaming edge cases covered

### Manual Testing Checklist

- [ ] Run chatbot and have multi-turn conversation
- [ ] Verify streaming shows tokens in real-time
- [ ] Check cost tracking is accurate
- [ ] Test with missing API key (should show clear error)
- [ ] Test Ctrl+C cancellation during response
- [ ] Verify context is maintained across turns
- [ ] Test with very long messages
- [ ] Test error handling by invalidating API key mid-session

## Dependencies

- **Blocked by**: documentation-improvements (README template)
- **Blocks**: None
- **Related**: example-fastapi-todo (shows different plugin usage), testing-infrastructure (provides testing patterns)

## Implementation Notes

### Decisions Made

- 2026-01-17 - Use Claude Sonnet 4.5 (good balance of capability and cost)
- 2026-01-17 - CLI interface (not web) for simplicity in example
- 2026-01-17 - Rich library for better CLI formatting
- 2026-01-17 - Keep last 10 turns by default (configurable)
- 2026-01-17 - Async implementation for streaming
- 2026-01-17 - Mock API in tests (no actual API calls during testing)

### Environment Variables

```bash
# .env.example
ANTHROPIC_API_KEY=your_api_key_here
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_CONTEXT_TURNS=10
TEMPERATURE=1.0
MAX_TOKENS=4096
```

### CLI Commands

```bash
# Start chatbot
python src/main.py

# Start with debug logging
python src/main.py --debug

# Use specific model
python src/main.py --model claude-opus-4-5-20251101

# Show usage stats after session
python src/main.py --show-stats
```

### Example Conversation Flow

```
$ python src/main.py

🤖 AI Chatbot (Claude Sonnet 4.5)
Type 'quit' to exit, 'clear' to reset conversation

You: Hello! Can you help me understand async Python?

🤖: Of course! Async Python allows you to write concurrent code using
the async/await syntax. Here are the key concepts:

1. async def - defines a coroutine function
2. await - suspends execution until awaitable completes
3. asyncio.run() - runs the main async function

Would you like me to show you an example?

You: Yes please!

🤖: Here's a simple example...

[Response continues with streaming...]

📊 Session Stats:
   Messages: 2
   Input tokens: 45
   Output tokens: 156
   Estimated cost: $0.0027
```

### Spec-Driven Development Example

Show in README how specs guided development:

```bash
# 1. Created specification
cat specs/features/streaming-responses.md

# 2. Used Claude Code with ai-app plugin
claude

# In Claude:
> "Implement streaming responses from specs/features/streaming-responses.md"

# 3. Claude read spec, implemented with best practices

# 4. Tested implementation
pytest tests/test_streaming.py -v

# 5. Updated spec status to "Implemented"
```

## Verification

### Setup Verification

```bash
cd examples/ai-chatbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Functionality Verification

```bash
# Run chatbot
python src/main.py

# Should show:
# - Welcome message
# - Prompt for input
# - Streaming responses when you type

# Test conversation context
# 1. Say "My name is Alice"
# 2. Later ask "What's my name?"
# 3. Should remember "Alice"
```

### Test Verification

```bash
pytest -v --cov=src --cov-report=term-missing

# Should show:
# - All tests passing
# - >85% coverage
# - No actual API calls (all mocked)
```

### Cost Tracking Verification

```bash
# After conversation, should see:
📊 Session Stats:
   Messages: X
   Input tokens: XXX
   Output tokens: XXX
   Estimated cost: $X.XXXX
```

## References

- AI app plugin: [plugins/ai-app/](../../plugins/ai-app/)
- Anthropic client template: [plugins/ai-app/templates/anthropic-client.py](../../plugins/ai-app/templates/anthropic-client.py)
- Prompt patterns: [plugins/ai-app/templates/prompt-patterns.md](../../plugins/ai-app/templates/prompt-patterns.md)
- Feature template: [templates/specs/feature.template.md](../../templates/specs/feature.template.md)
- Anthropic API docs: https://docs.anthropic.com/

---

**Template Version**: 1.0
**Last Updated**: 2026-01-17
