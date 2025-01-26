import json
import requests
from typing_extensions import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph

from github_assistant.configuration import Configuration
from github_assistant.state import GitHubTrendingState, GitHubTrendingStateInput, GitHubTrendingStateOutput
from github_assistant.prompts import repo_analyzer_instructions, summarizer_instructions

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com/search/repositories"
TRENDING_PARAMS = {
    "q": "created:>2024-01-18",  # Last week
    "sort": "stars",
    "order": "desc",
    "per_page": 10  # Request more than we need in case some are invalid
}

def fetch_repositories(state: GitHubTrendingState, config: RunnableConfig):
    """Fetch repositories from GitHub API and initialize state"""
    print("\nFetching repositories...")
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(GITHUB_API_URL, params=TRENDING_PARAMS, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code}")
    
    # Get valid repos (those with required fields)
    valid_repos = []
    for repo in response.json()["items"]:
        if all(key in repo for key in ["full_name", "html_url"]):
            valid_repos.append(repo)
        if len(valid_repos) >= 3:
            break
    
    if len(valid_repos) < 3:
        raise Exception(f"Could not find 3 valid repositories, only found {len(valid_repos)}")
    
    # Take exactly 3 repos and store in state
    repos_to_analyze = valid_repos[:3]
    print(f"Fetched repositories to analyze:")
    for i, repo in enumerate(repos_to_analyze, 1):
        print(f"{i}. {repo['full_name']}")
    
    # Initialize state with all fields
    return {
        "trending_query": state.trending_query,  # Keep existing query
        "original_repos": repos_to_analyze,
        "current_repo_index": 0,
        "repositories_summarized": [],
        "running_summary": "",
        "next_step": "continue"
    }

def analyze_repository(state: GitHubTrendingState, config: RunnableConfig):
    """Analyze current repository"""
    print(f"\nAnalyzing repository {state.current_repo_index + 1} of {len(state.original_repos)}")
    
    # Check if we've analyzed all repositories
    if state.current_repo_index >= 3:
        print("All repositories analyzed")
        return {
            "trending_query": state.trending_query,
            "next_step": "finalize"
        }
    
    # Get current repository
    current_repo = state.original_repos[state.current_repo_index]
    print(f"Repository: {current_repo['full_name']}")
    
    repo_info = {
        "name": current_repo["full_name"],
        "description": current_repo.get("description", "No description available"),
        "stars": current_repo.get("stargazers_count", 0),
        "forks": current_repo.get("forks_count", 0),
        "language": current_repo.get("language", "Not specified"),
        "url": current_repo["html_url"]
    }
    
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOllama(model=configurable.local_llm, temperature=0)
    llm.num_ctx = 16384
    result = llm.invoke(
        [SystemMessage(content=repo_analyzer_instructions),
         HumanMessage(content=f"Analyze this repository: {json.dumps(repo_info)}")]
    )
    
    # Create new summary
    new_summary = result.content
    if state.running_summary:
        new_summary = state.running_summary + f"\n\n{result.content}"
    
    # Move to next repository
    next_index = state.current_repo_index + 1
    next_step = "finalize" if next_index >= 3 else "continue"
    
    # Return updated state
    return {
        "trending_query": state.trending_query,
        "current_repo_index": next_index,
        "repositories_summarized": state.repositories_summarized + [current_repo],
        "running_summary": new_summary,
        "next_step": next_step
    }

def finalize_summary(state: GitHubTrendingState, config: RunnableConfig):
    """Create final summary of all analyzed repositories"""
    print("\nFinalizing summary...")
    print(f"Total repos analyzed: {len(state.repositories_summarized)}")
    
    # First create a comprehensive summary using the LLM
    configurable = Configuration.from_runnable_config(config)
    llm = ChatOllama(model=configurable.local_llm, temperature=0)
    llm.num_ctx = 16384
    result = llm.invoke(
        [SystemMessage(content=summarizer_instructions),
         HumanMessage(content=f"Create a comprehensive summary of these repository analyses:\n\n{state.running_summary}")]
    )
    
    # Then format with repository links
    repo_links = "\n".join(
        f"- [{repo['full_name']}]({repo['html_url']})" 
        for repo in state.repositories_summarized
    )
    
    final_summary = f"## Trending GitHub Repositories Summary\n\n{result.content}\n\n### Repositories:\n{repo_links}"
    return {"running_summary": final_summary}

def next_step(state: GitHubTrendingState) -> Literal["analyze_repository", "finalize_summary"]:
    """Determine the next step in the workflow"""
    print(f"\nDeciding next step...")
    print(f"Current index: {state.current_repo_index}")
    print(f"Total repos: {len(state.original_repos)}")
    print(f"Next step: {state.next_step}")
    
    if state.next_step == "finalize":
        print("Moving to finalize_summary")
        return "finalize_summary"
    print("Continuing with analyze_repository")
    return "analyze_repository"

# Build the graph
builder = StateGraph(
    GitHubTrendingState,
    input=GitHubTrendingStateInput,
    output=GitHubTrendingStateOutput,
    config_schema=Configuration
)

# Add nodes
builder.add_node("fetch_repositories", fetch_repositories)
builder.add_node("analyze_repository", analyze_repository)
builder.add_node("finalize_summary", finalize_summary)

# Build flow with loop
builder.add_edge(START, "fetch_repositories")
builder.add_edge("fetch_repositories", "analyze_repository")

# Add conditional edges from analyze_repository
builder.add_conditional_edges(
    "analyze_repository",
    next_step,
    {
        "analyze_repository": "analyze_repository",  # Loop back to analyze next repo
        "finalize_summary": "finalize_summary"      # Move to final summary when done
    }
)

builder.add_edge("finalize_summary", END)

graph = builder.compile()
