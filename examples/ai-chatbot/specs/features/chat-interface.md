# Feature: CLI Chat Interface

**Status**: Implemented
**Owner**: AI Chatbot Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Provide an interactive command-line interface for chatting with Claude AI that is intuitive, user-friendly, and provides clear visual feedback during conversations.

## Requirements

- [x] Interactive prompt for user input
- [x] Visual distinction between user and assistant messages
- [x] Support for special commands (quit, exit, clear, stats)
- [x] Rich formatting with colors and icons
- [x] Graceful handling of Ctrl+C interruption
- [x] Welcome message showing model information
- [x] Command hints for new users
- [x] Empty input validation

## User Stories

**As a** user
**I want** to interact with the chatbot through a clean CLI interface
**So that** I can have natural conversations with Claude AI

**As a** user
**I want** special commands like 'clear' and 'stats'
**So that** I can control my conversation session

## Acceptance Criteria

1. **Given** I start the chatbot
   **When** the application launches
   **Then** I see a welcome message with the model name and usage hints

2. **Given** I'm in a conversation
   **When** I type a message and press Enter
   **Then** my message is sent and the assistant's response appears with clear visual distinction

3. **Given** I want to start fresh
   **When** I type "clear"
   **Then** the conversation history is reset and I see a confirmation message

4. **Given** I want to see statistics
   **When** I type "stats"
   **Then** I see token usage and cost information for the current session

5. **Given** I want to exit
   **When** I type "quit" or "exit" or press Ctrl+D
   **Then** the application exits gracefully and shows final statistics

6. **Given** I press Ctrl+C during a response
   **When** the assistant is generating a response
   **Then** the response is cancelled without crashing the application

7. **Given** I press Enter without typing anything
   **When** the input is empty
   **Then** the prompt reappears without making an API call

## Technical Details

### Implementation

The CLI interface is implemented in [src/main.py](../../src/main.py) with the `ChatBot` class and [src/utils/ui.py](../../src/utils/ui.py) with the `UI` class for formatting.

### Commands

| Command | Description |
|---------|-------------|
| `quit` or `exit` | Exit the chatbot and show final statistics |
| `clear` | Reset conversation history |
| `stats` | Show current session statistics |
| Ctrl+D | Exit the chatbot (EOF) |
| Ctrl+C | Cancel current response or exit if idle |

### Visual Design

- **User messages**: Prefixed with "You:"
- **Assistant messages**: Prefixed with "🤖:"
- **Errors**: Red with ✗ symbol
- **Warnings**: Yellow with ⚠ symbol
- **Info**: Blue with ℹ symbol
- **Success**: Green with ✓ symbol

### Error Handling

1. **Empty input**: Silently ignored, prompt reappears
2. **Keyboard interrupt during response**: Response cancelled, user message removed from history
3. **EOF (Ctrl+D)**: Graceful exit with statistics
4. **Unexpected errors**: Error message displayed, debug mode shows traceback

## Verification

### Manual Testing

```bash
# Start the chatbot
cd examples/ai-chatbot
python src/main.py

# Test commands:
# 1. Type a message and verify it appears correctly
# 2. Type "clear" and verify conversation resets
# 3. Type "stats" and verify statistics appear
# 4. Press Ctrl+C during a response and verify it cancels
# 5. Type "quit" and verify it exits with statistics
```

### Expected Output

```
🤖 AI Chatbot (claude-sonnet-4-5-20250929)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type 'quit' to exit, 'clear' to reset conversation, 'stats' for usage info

You: Hello!

🤖: Hello! How can I help you today?

You: quit

📊 Session Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Messages sent: 1
  Total tokens: 45 (input: 12, output: 33)
  Estimated cost: $0.0005
```

## Edge Cases

1. **Very long input**: Accepted up to reasonable limits (validated by conversation manager)
2. **Special characters**: Handled properly in all inputs
3. **Multiple consecutive empty inputs**: All ignored without issue
4. **Rapid Ctrl+C presses**: Handled gracefully without crashes

## Dependencies

- **Requires**: [src/utils/ui.py](../../src/utils/ui.py) for formatting
- **Requires**: [src/chat/conversation.py](../../src/chat/conversation.py) for conversation management
- **Requires**: [src/utils/cost_tracker.py](../../src/utils/cost_tracker.py) for statistics

## Related Specifications

- [streaming-responses.md](streaming-responses.md) - How responses are displayed
- [conversation-context.md](conversation-context.md) - How history is managed
- [cost-tracking.md](cost-tracking.md) - Statistics calculation

---

**Implementation**: [src/main.py:17-203](../../src/main.py#L17-L203)
**Tests**: [tests/test_config.py](../../tests/test_config.py)
**Template Version**: 1.0
