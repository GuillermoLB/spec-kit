# AI Chatbot Example

An interactive CLI chatbot powered by Anthropic's Claude API, demonstrating spec-kit's AI app plugin and spec-driven development methodology.

## Features

- **Streaming Responses**: Real-time token-by-token response display
- **Context Management**: Multi-turn conversations with automatic history trimming
- **Cost Tracking**: Track token usage and estimated costs per session
- **Error Handling**: Graceful handling of API errors, rate limits, and network issues
- **Rich CLI Interface**: Formatted output with colors and panels using Rich library

## Prerequisites

- Python 3.11 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Setup

### 1. Install Dependencies

```bash
cd examples/ai-chatbot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run the Chatbot

```bash
python src/main.py
```

## Usage

### Basic Commands

- **Type your message**: Just type and press Enter
- **quit** or **exit**: Exit the chatbot
- **clear**: Reset the conversation history
- **stats**: Show current session statistics

### Command Line Options

```bash
# Run with debug mode
python src/main.py --debug

# Use a different model
python src/main.py --model claude-opus-4-5-20251101

# Don't show stats on exit
python src/main.py --no-stats
```

### Example Session

```
$ python src/main.py

AI Chatbot (claude-sonnet-4-5-20250929)
Type 'quit' to exit, 'clear' to reset conversation, 'stats' to show session stats

You: Hello! Can you help me understand async Python?