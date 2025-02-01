# LangGraph DeepSeek Researcher

A sophisticated research assistant powered by LangGraph and DeepSeek, designed for deep contextual analysis and iterative research tasks. This project combines the power of LangGraph's directed workflow system with DeepSeek's advanced language model capabilities to create an intelligent, locally-run research assistant.

![research-rabbit](https://github.com/user-attachments/assets/4308ee9c-abf3-4abb-9d1e-83e7c2c3f187)

## 🌟 Key Features

- **LangGraph-Powered Workflow**: Implements a sophisticated directed graph system for managing research processes
- **DeepSeek Integration**: Leverages DeepSeek's R1 model (default: deepseek-r1:32b) for advanced language understanding
- **Iterative Research Process**: Conducts deep, multi-cycle research with automatic knowledge gap identification
- **Local Execution**: Runs completely locally using Ollama for model hosting
- **Interactive Visualization**: Full research process visualization through LangGraph Studio

## 🚀 Getting Started

### Prerequisites

1. Install Ollama and pull the DeepSeek model:
```powershell
ollama pull deepseek-r1:32b
```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Tavily API key (free tier: 1000 requests) to `.env`:
     ```
     TAVILY_API_KEY=your_tavily_api_key
     ```

### Installation

Clone and launch the assistant with LangGraph server:
```powershell
# Install UV package manager from https://docs.astral.sh/uv/getting-started/installation/

# Clone and setup project
git clone https://github.com/langchain-ai/ollama-deep-researcher.git
cd ollama-deep-researcher
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev
```

## 🔍 Research Architecture

The system implements an advanced research workflow based on LangGraph's directed graph architecture:

1. **Query Generation**
   - Uses DeepSeek to generate focused search queries
   - Structures outputs in JSON format for systematic processing

2. **Web Research**
   - Integrates with Tavily API for comprehensive web searches
   - Implements intelligent source deduplication and reference management

3. **Source Analysis**
   - Performs incremental summary building
   - Maintains detailed source attribution
   - Integrates new information with existing knowledge

4. **Iterative Refinement**
   - Automatically identifies knowledge gaps
   - Generates targeted follow-up queries
   - Improves research depth through multiple iterations

## 💻 Usage

1. Access the LangGraph Studio Web UI (http://127.0.0.1:2024)
2. Configure your settings in the `configuration` tab:
   - Model selection (default: deepseek-r1:32b)
   - Research iteration depth
   - Additional parameters

<img width="1621" alt="Configuration Interface" src="https://github.com/user-attachments/assets/7cfd0e04-28fd-4cfa-aee5-9a556d74ab21" />

3. Input your research topic and watch the system work:

<img width="1621" alt="Research Process" src="https://github.com/user-attachments/assets/4de6bd89-4f3b-424c-a9cb-70ebd3d45c5f" />

## 📊 Output Visualization

- **Research Summary**: Detailed markdown output with source citations
- **Source Tracking**: Complete source list in graph state
- **Process Visualization**: Full research workflow visible in LangGraph Studio

![Source Visualization](https://github.com/user-attachments/assets/e8ac1c0b-9acb-4a75-8c15-4e677e92f6cb)

## 🛠 Technical Details

### Core Dependencies
- LangGraph (≥0.2.55)
- LangChain Community (≥0.3.9)
- Tavily Python (≥0.5.0)
- LangChain Ollama (≥0.2.1)

### Project Structure
```
src/assistant/
├── configuration.py  # System configuration
├── graph.py         # Core workflow implementation
├── prompts.py       # LLM prompts
├── state.py         # State management
└── utils.py         # Utility functions
```

## 🚀 Deployment

For deployment options, refer to the [LangGraph documentation](https://langchain-ai.github.io/langgraph/concepts/#deployment-options) or explore [Module 6](https://github.com/langchain-ai/langchain-academy/tree/main/module-6) of LangChain Academy for detailed deployment walkthroughs.
