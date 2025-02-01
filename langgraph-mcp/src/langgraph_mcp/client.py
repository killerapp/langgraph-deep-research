"""LangGraph API client implementation."""

import logging
from typing import Optional, List
import httpx
from .types import Assistant


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LangGraphError(Exception):
    """Base exception for LangGraph client errors."""
    pass


class LangGraphClient:
    """Client for interacting with the LangGraph API."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:2024"):
        """Initialize the LangGraph client.
        
        Args:
            base_url: Base URL of the LangGraph API server
        """
        self.base_url = base_url.rstrip('/')
        
    async def list_assistants(self) -> List[Assistant]:
        """List all available LangGraph assistants.
        
        Returns:
            List of Assistant objects
            
        Raises:
            LangGraphError: If an error occurs while fetching assistants
        """
        logger.debug("Listing all available assistants")
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/assistants/search"
                logger.debug("Making POST request to: %s", url)
                response = await client.post(url, json={})
                response.raise_for_status()
                assistants_data = response.json()
                logger.debug("Received assistants: %s", assistants_data)
                
                if not assistants_data:
                    return []
                
                return [Assistant.model_validate(data) for data in assistants_data]
                    
        except httpx.HTTPError as e:
            raise LangGraphError(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            raise LangGraphError(f"Error listing assistants: {str(e)}")

    async def find_assistant(self, assistant_id: Optional[str] = None) -> Assistant:
        """Find a LangGraph assistant.
        
        Args:
            assistant_id: Optional specific assistant ID to find.
                        If not provided, returns the first available assistant.
        
        Returns:
            Assistant object with the assistant's information
            
        Raises:
            LangGraphError: If the assistant cannot be found or other API errors occur
        """
        logger.debug("Finding assistant with ID: %s", assistant_id if assistant_id else "None (searching for first available)")
        try:
            async with httpx.AsyncClient() as client:
                if assistant_id:
                    # Get specific assistant
                    url = f"{self.base_url}/assistants/{assistant_id}"
                    logger.debug("Making GET request to: %s", url)
                    response = await client.get(url)
                    if response.status_code == 404:
                        raise LangGraphError(f"Assistant {assistant_id} not found")
                    response.raise_for_status()
                    data = response.json()
                    logger.debug("Received response data: %s", data)
                    return Assistant.model_validate(data)
                else:
                    # Search for assistants
                    url = f"{self.base_url}/assistants/search"
                    logger.debug("Making POST request to: %s with limit=1", url)
                    response = await client.post(url, json={"limit": 1})
                    response.raise_for_status()
                    assistants = response.json()
                    logger.debug("Received assistants: %s", assistants)
                    
                    if not assistants:
                        raise LangGraphError("No assistants found")
                    
                    # Get full assistant details
                    assistant_id = assistants[0]["assistant_id"]
                    logger.debug("Found assistant ID: %s, fetching details", assistant_id)
                    return await self.find_assistant(assistant_id)
                    
        except httpx.HTTPError as e:
            raise LangGraphError(f"HTTP error occurred: {str(e)}")
        except Exception as e:
            raise LangGraphError(f"Error finding assistant: {str(e)}")
