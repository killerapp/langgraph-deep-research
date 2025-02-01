"""Type definitions for LangGraph MCP client."""

from datetime import datetime
from typing import Dict, Optional, Any, AsyncIterator, List

from pydantic import BaseModel


class Assistant(BaseModel):
    """Model representing a LangGraph assistant."""
    
    assistant_id: str
    graph_id: str
    name: str
    config: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    version: int


class ResearchStep(BaseModel):
    """Model representing a step in the research process."""
    
    step_id: str
    type: str  # e.g., "query_generation", "web_research", "summarization", "reflection"
    content: Dict[str, Any]
    timestamp: datetime


class ResearchResponse(BaseModel):
    """Model representing a research response."""
    
    research_id: str
    topic: str
    status: str  # "in_progress", "completed", "error"
    steps: List[ResearchStep]
    summary: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
