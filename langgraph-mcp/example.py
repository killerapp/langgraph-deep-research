"""Example usage of the LangGraph client."""

import asyncio
import sys
from langgraph_mcp import LangGraphClient, Assistant


async def main():
    """Demonstrate finding a LangGraph assistant."""
    print("Starting LangGraph client test...")
    client = LangGraphClient()
    
    try:
        print("Searching for available assistants...")
        # List all available assistants
        assistants = await client.list_assistants()
        print("\nFound assistants:")
        for assistant in assistants:
            print(f"\nID: {assistant.assistant_id}")
            print(f"Name: {assistant.name}")
            print(f"Graph: {assistant.graph_id}")
            print(f"Version: {assistant.version}")
            print(f"Created: {assistant.created_at}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        print(f"Error type: {type(e)}", file=sys.stderr)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)
