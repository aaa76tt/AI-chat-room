# AI Multi-Agent Conversation System

A beautiful dark-themed GUI application that enables three AI agents to have continuous conversations with shared memory.

## Features

- **Three AI Agents**: A, B, and C
- **Shared Memory**: All agents can access the complete conversation history
- **Dark Theme UI**: Beautiful and modern interface with color-coded agents
- **Continuous Conversation**: Agents chat indefinitely until stopped
- **Real-time Statistics**: Track rounds and message count
- **Thread-safe**: Non-blocking UI with background conversation processing

## Requirements

```bash
pip install requests tkinter
```

## Configuration

Edit the API configuration in `main.py`:

```python
API_KEY = "your-api-key-here"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-V3"
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter an initial topic in the text field
3. Click "▶ Start" to begin the conversation
4. Click "⏸ Stop" to end the conversation at any time

## How It Works

1. **AI1 (Alice)** - Cyan color - Starts or continues the conversation based on shared memory
2. **AI2 (Bob)** - Orange color - Responds based on the complete conversation history
3. **AI3 (Charlie)** - Purple color - Adds to the conversation with full context awareness

Each AI agent:
- Has a unique identity and name
- Can read the last 10 messages from shared memory
- Contributes to the ongoing conversation
- Maintains context across multiple rounds

## File Structure

```
AI chat room/
├── main.py      # Main GUI application
├── AI1.py       # AI Agent 1 (Alice)
├── AI2.py       # AI Agent 2 (Bob)
├── AI3.py       # AI Agent 3 (Charlie)
└── README.md    # This file
```

## Color Scheme

- **Background**: Dark gray (#1e1e1e, #252526)
- **Text**: Light gray (#d4d4d4)
- **AI1 (Alice)**: Cyan (#4ec9b0)
- **AI2 (Bob)**: Orange (#ce9178)
- **AI3 (Charlie)**: Purple (#c586c0)
- **Accent**: Blue (#007acc)

## Notes

- The conversation runs in a separate thread to keep the UI responsive
- Shared memory is limited to the last 10 messages to prevent prompt overflow
- Each agent knows its identity and can reference previous messages
- Error handling is built-in for API failures

## License

Free to use and modify.
