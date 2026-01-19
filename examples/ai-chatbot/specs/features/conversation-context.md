# Feature: Conversation Context Management

**Status**: Implemented
**Owner**: AI Chatbot Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Maintain conversation history across multiple turns so Claude can provide contextually relevant responses that reference previous messages. Implement automatic context window management to prevent exceeding API limits.

## Requirements

- [x] Store message history in Anthropic API format
- [x] Support multi-turn conversations
- [x] Maintain system prompt across turns
- [x] Automatic history trimming when approaching context limits
- [x] Track trimming state to inform users
- [x] Support clearing conversation history
- [x] Validate message content before adding
- [x] Provide message and turn count tracking

## User Stories

**As a** user
**I want** the chatbot to remember our conversation
**So that** I can ask follow-up questions without repeating context

**As a** user
**I want** the chatbot to handle long conversations
**So that** I don't get errors when the context gets large

**As a** developer
**I want** automatic context management
**So that** I don't have to manually trim message history

## Acceptance Criteria

1. **Given** I have a conversation
   **When** I send a follow-up question referencing earlier context
   **Then** Claude provides a contextually appropriate response

2. **Given** I ask "My name is Alice"
   **When** I later ask "What's my name?"
   **Then** Claude responds with "Alice"

3. **Given** I have 10+ conversation turns
   **When** I send a new message
   **Then** older messages are automatically trimmed if needed

4. **Given** my conversation was trimmed
   **When** trimming occurs
   **Then** I see a warning "Trimmed old messages to fit context window"

5. **Given** I type "clear"
   **When** the command is executed
   **Then** all conversation history is removed and I start fresh

6. **Given** I try to send an empty message
   **When** validation occurs
   **Then** a ValueError is raised preventing the empty message

## Technical Details

### Implementation

Conversation management is implemented in [src/chat/conversation.py](../../src/chat/conversation.py) with the `ConversationManager` class.

### Message Format

Messages follow the Anthropic API format:

```python
{
    "role": "user" | "assistant",
    "content": str
}
```

### Context Management Strategy

**Trimming Logic:**
- Maximum turns: 10 (configurable)
- 1 turn = 1 user message + 1 assistant message
- When limit reached: Remove oldest user+assistant pair
- System prompt: Always preserved
- Trimming flag: Set when trimming occurs

**Why Trim by Turns:**
- Maintains conversation coherence
- Prevents partial context
- Avoids breaking multi-turn logic
- Keeps related Q&A together

### System Prompt

Default system prompt:
```
You are a helpful AI assistant powered by Claude. Be concise,
accurate, and friendly in your responses.
```

System prompt is:
- Set during initialization
- Never included in message history
- Always sent with each API call
- Can be customized via configuration

### Data Structure

```python
class ConversationManager:
    messages: list[dict]          # Message history
    max_turns: int                # Maximum conversation turns
    system_prompt: str            # System instruction
    _last_trimmed: bool           # Trimming flag

    def add_user_message(msg)     # Add user message
    def add_assistant_message(msg) # Add assistant response
    def get_messages()            # Get all messages
    def get_message_count()       # Count messages
    def get_turn_count()          # Count conversation turns
    def clear()                   # Reset conversation
    def was_trimmed()             # Check if trimmed
```

### Validation Rules

- Messages must be non-empty strings
- Messages must contain non-whitespace characters
- Leading/trailing whitespace is preserved (might be intentional)
- Empty messages raise `ValueError`

## Verification

### Manual Testing

```bash
# Test context retention
cd examples/ai-chatbot
python src/main.py

# Conversation flow:
You: My name is Alice and I'm learning Python
🤖: Great to meet you, Alice! Python is excellent...

You: What programming language am I learning?
🤖: You're learning Python!

You: What's my name again?
🤖: Your name is Alice.

# Test trimming (send 11+ exchanges)
# Verify warning appears after 10 turns

# Test clear command
You: clear
ℹ Conversation cleared

You: What's my name?
🤖: I don't have that information...
```

### Automated Testing

Tests in [tests/test_conversation.py](../../tests/test_conversation.py) verify:

- [x] Adding user messages
- [x] Adding assistant messages
- [x] Empty message validation
- [x] Message counting
- [x] Turn counting (1 turn = user + assistant)
- [x] Automatic trimming at max turns
- [x] System prompt handling
- [x] Clear functionality
- [x] Trimming flag tracking

```bash
# Run conversation tests
pytest tests/test_conversation.py -v
```

## Edge Cases

1. **Long monologue**: User sends many messages before assistant responds
   - **Handling**: All user messages preserved until response

2. **First message very long**: Approaches token limit
   - **Handling**: Message accepted (API will handle token limits)

3. **Clear on empty conversation**:
   - **Handling**: No error, conversation remains empty

4. **Trimming with exactly max_turns**:
   - **Handling**: No trimming until max_turns + 1

5. **Multiple assistant messages without user response**:
   - **Handling**: Both assistant messages preserved

## Performance

- **Memory**: O(n) where n = number of messages (limited by max_turns)
- **Trimming**: O(1) - removes oldest pair only
- **Message access**: O(1) - direct list access
- **Turn counting**: O(n) - iterates messages

## Configuration

```python
# From src/chat/conversation.py
DEFAULT_MAX_TURNS = 10
DEFAULT_SYSTEM_PROMPT = """
You are a helpful AI assistant powered by Claude.
Be concise, accurate, and friendly in your responses.
"""

# Can be overridden during initialization
manager = ConversationManager(
    max_turns=20,
    system_prompt="Custom system prompt"
)
```

## Future Enhancements

Potential improvements (not currently implemented):

- [ ] Token-based trimming instead of turn-based
- [ ] Summarization of trimmed history
- [ ] Export/import conversation history
- [ ] Search conversation history
- [ ] Conversation branching
- [ ] Multiple conversation threads

## Dependencies

- **Requires**: Python 3.11+ for type hints
- **Used by**: [src/main.py](../../src/main.py) for conversation management
- **Used by**: [src/chat/client.py](../../src/chat/client.py) for API calls

## Related Specifications

- [chat-interface.md](chat-interface.md) - CLI commands (clear)
- [streaming-responses.md](streaming-responses.md) - How responses are added
- [cost-tracking.md](cost-tracking.md) - Token usage across turns

---

**Implementation**: [src/chat/conversation.py:1-137](../../src/chat/conversation.py#L1-L137)
**Tests**: [tests/test_conversation.py](../../tests/test_conversation.py)
**Template Version**: 1.0
