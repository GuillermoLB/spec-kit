# Feature: Streaming Responses

**Status**: Implemented
**Owner**: AI Chatbot Example Team
**Last Updated**: 2026-01-18
**Priority**: High

## Purpose

Display AI responses in real-time as tokens are generated, providing better user experience than waiting for the complete response. This creates a more natural, conversation-like feel.

## Requirements

- [x] Use Anthropic streaming API
- [x] Display tokens as they arrive
- [x] Track token usage from streaming metadata
- [x] Handle stream interruptions gracefully
- [x] Support cancellation (Ctrl+C)
- [x] Accumulate full response for conversation history
- [x] Process different streaming event types

## User Stories

**As a** user
**I want** to see the assistant's response appear in real-time
**So that** I know the system is working and can start reading before the full response is complete

**As a** user
**I want** to cancel a response if it's not what I need
**So that** I don't waste time and tokens waiting for an irrelevant response

## Acceptance Criteria

1. **Given** I send a message
   **When** Claude generates a response
   **Then** I see tokens appear in real-time without delay

2. **Given** streaming is in progress
   **When** I press Ctrl+C
   **Then** the stream stops gracefully and the incomplete response is discarded

3. **Given** the API connection drops
   **When** the stream is interrupted
   **Then** I see the partial response that was received and an error message

4. **Given** a response completes
   **When** streaming finishes
   **Then** the full response is added to conversation history

5. **Given** a response streams
   **When** token usage metadata is received
   **Then** usage statistics are tracked accurately

## Technical Details

### Implementation

The streaming functionality is implemented in [src/chat/streaming.py](../../src/chat/streaming.py) with the `StreamingHandler` class and [src/chat/client.py](../../src/chat/client.py) with the `AnthropicClient` class.

### Streaming Event Types

The handler processes these Anthropic streaming events:

| Event Type | Description | Action |
|------------|-------------|--------|
| `message_start` | Stream begins | Initialize tracking |
| `content_block_start` | Content block begins | Prepare for text |
| `content_block_delta` | Text token received | Yield token, accumulate |
| `content_block_stop` | Content block ends | Finalize block |
| `message_delta` | Usage data received | Track token counts |
| `message_stop` | Stream complete | Finalize response |

### Data Flow

```
API Stream → StreamingHandler.process_stream()
    ↓
  Extract text deltas
    ↓
  Yield to UI (real-time display)
    ↓
  Accumulate in internal buffer
    ↓
  Track usage metadata
    ↓
  Return full text when complete
```

### Error Handling

1. **KeyboardInterrupt (Ctrl+C)**:
   - Stream iteration stops immediately
   - Buffered text is discarded
   - User message removed from history
   - New prompt appears

2. **Network interruption**:
   - Partial response displayed
   - Error message shown
   - User can retry

3. **API error in stream**:
   - Error event processed
   - User-friendly error displayed
   - Conversation state restored

### Code Example

```python
# From src/main.py
stream = self.client.create_stream(
    messages=messages,
    system=system_prompt
)

# Process and display stream
for chunk in self.streaming.process_stream(stream):
    self.ui.show_streaming_text(chunk)

# Get full response after streaming
full_response = self.streaming.get_full_text()
usage = self.streaming.get_usage()
```

## Verification

### Manual Testing

```bash
# Test streaming
cd examples/ai-chatbot
python src/main.py

# 1. Send: "Write a haiku about programming"
#    Verify: Tokens appear one by one in real-time

# 2. Send: "Tell me a long story"
#    Press: Ctrl+C mid-response
#    Verify: Stream stops, message removed, no crash

# 3. (Simulate network issue by disconnecting)
#    Verify: Partial response shown with error
```

### Automated Testing

Tests in [tests/test_streaming.py](../../tests/test_streaming.py) verify:

- [x] Token accumulation from deltas
- [x] Usage tracking from message_delta events
- [x] Reset between messages
- [x] Empty stream handling
- [x] Multiple streams with proper reset

```bash
# Run streaming tests
pytest tests/test_streaming.py -v
```

### Expected Behavior

**Normal streaming:**
```
You: Write a haiku

🤖: Code
🤖: flows
🤖:  like
🤖:  a
🤖:  stream
...
```

**Cancelled streaming:**
```
You: Tell me a story

🤖: Once upon a time, there was
^C
⚠ Response cancelled
```

## Performance

- **Latency**: First token typically appears within 200-500ms
- **Throughput**: ~50-100 tokens per second
- **Memory**: Minimal, buffering only the current response

## Edge Cases

1. **Empty response**: Handler returns empty string, no error
2. **Stream with only metadata**: No text yielded, usage still tracked
3. **Multiple content blocks**: All blocks accumulated in order
4. **Interrupted stream**: Partial text available via `get_full_text()`
5. **Rapid successive streams**: Reset between streams prevents mixing

## Security Considerations

- No sensitive data logged during streaming
- API key never exposed in stream events
- User input validated before creating stream

## Dependencies

- **Requires**: `anthropic` SDK 0.39+ for streaming support
- **Requires**: [src/chat/client.py](../../src/chat/client.py) for API interaction
- **Requires**: [src/utils/ui.py](../../src/utils/ui.py) for display

## Related Specifications

- [chat-interface.md](chat-interface.md) - CLI integration
- [conversation-context.md](conversation-context.md) - How responses are stored
- [cost-tracking.md](cost-tracking.md) - Usage tracking from streams

---

**Implementation**: [src/chat/streaming.py:1-94](../../src/chat/streaming.py#L1-L94)
**Tests**: [tests/test_streaming.py](../../tests/test_streaming.py)
**Template Version**: 1.0
