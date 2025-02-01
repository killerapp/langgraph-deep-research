---
name: Ollama Deep Researcher
type: project
description: A Python-based research assistant leveraging Ollama for deep contextual analysis and research tasks.
style: graph-based
---

# Ollama Deep Researcher

A Python-based research assistant leveraging Ollama for deep contextual analysis and research tasks.

## Overview

This project implements an AI-powered research assistant using LangGraph and Ollama to perform deep research tasks. It utilizes a directed graph workflow to manage research processes, combining web search capabilities with LLM-based analysis and summarization.

## Architecture

The system is built on a graph-based workflow architecture with the following key components:

### Core Components

1. **Graph System** (`graph.py`)
   - Implements a directed graph workflow using LangGraph
   - Manages state transitions between research phases
   - Handles the research loop with configurable iterations

2. **Configuration** (`configuration.py`)
   - Manages system settings including:
     - Maximum research loop iterations
     - Local LLM model selection (default: deepseek-r1:32b)
   - Supports environment variable overrides

3. **MCP Integration** (`langgraph-mcp/`)
   - Implements an MCP server for programmatic access to the research system
   - Requires a running LangGraph instance on port 2024
   - Current capabilities:
     - Assistant discovery and retrieval
     - Assistant metadata access
   - Planned capabilities:
     - Direct research graph execution
     - Topic-based research initiation
     - Research progress monitoring

### Research Workflow

The system follows a structured research process:

1. **Query Generation**
   - Generates focused search queries based on the research topic
   - Uses JSON-formatted LLM outputs for structured query generation

2. **Web Research**
   - Performs web searches using Tavily API
   - Processes and formats search results
   - Deduplicates and manages source references

3. **Source Summarization**
   - Incrementally builds research summaries
   - Integrates new information with existing summaries
   - Maintains source attribution

4. **Reflection and Iteration**
   - Analyzes current knowledge state
   - Identifies knowledge gaps
   - Generates follow-up queries for deeper research

## Dependencies

- LangGraph (≥0.2.55)
- LangChain Community (≥0.3.9)
- Tavily Python (≥0.5.0)
- LangChain Ollama (≥0.2.1)

## Development Tools

- Mypy for type checking
- Ruff for linting with comprehensive rule sets
- Google-style docstring convention

## Project Structure

```
.
├── src/
│   ├── assistant/
│   │   ├── __init__.py
│   │   ├── configuration.py  # System configuration
│   │   ├── graph.py         # Core workflow implementation
│   │   ├── prompts.py       # LLM prompts
│   │   ├── state.py         # State management
│   │   └── utils.py         # Utility functions
│   └── github_assistant/    # GitHub-specific implementation
└── langgraph-mcp/          # MCP server implementation
    ├── src/
    │   └── langgraph_mcp/
    │       ├── __init__.py
    │       ├── client.py    # LangGraph API client
    │       └── types.py     # Type definitions
    └── example.py          # Usage examples
