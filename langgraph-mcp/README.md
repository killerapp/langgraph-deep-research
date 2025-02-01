# LangGraph MCP Client

A Python client library for interacting with the LangGraph API, designed to be used as an MCP server.

## Installation

From the project directory:

```bash
uv pip install -e .
```

## Usage

The client provides a simple async interface for finding and interacting with LangGraph assistants:

```python
from langgraph_mcp import LangGraphClient

async def main():
    client = LangGraphClient()
    
    # Find the first available assistant
    assistant = await client.find_assistant()
    print(f"Found assistant: {assistant.name}")
    
    # Find a specific assistant by ID
    assistant = await client.find_assistant("assistant-id-here")
    print(f"Found assistant: {assistant.name}")

```

See `example.py` for a complete usage example.

## Development

The project uses:
- `httpx` for async HTTP requests
- `pydantic` for data validation and serialization
- `ruff` for linting

## Project Structure

```
langgraph-mcp/
├── src/
│   └── langgraph_mcp/
│       ├── __init__.py
│       ├── client.py    # Main client implementation
│       └── types.py     # Pydantic models
├── example.py           # Usage example
└── pyproject.toml       # Project configuration
```

## Future Development

This client will be expanded into a full MCP server to provide standardized tools for interacting with the LangGraph API.
