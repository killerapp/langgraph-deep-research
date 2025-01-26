import operator
from dataclasses import dataclass, field
from typing_extensions import TypedDict, Annotated

@dataclass(kw_only=True)
class GitHubTrendingState:
    trending_query: str = field(default="top-3-trending-repos")  # Fixed query for trending repos
    original_repos: list = field(default_factory=list)  # Store original trending repos
    current_repo_index: int = field(default=0)  # Track which repo we're analyzing
    repositories_summarized: Annotated[list, operator.add] = field(default_factory=list)  # Processed repos
    running_summary: str = field(default="")  # Accumulated analyses
    next_step: str = field(default="continue")  # Control flow: "continue" or "finalize"

@dataclass(kw_only=True)
class GitHubTrendingStateInput(TypedDict):
    trending_query: str = field(default="top-3-trending-repos")  # Fixed input needed for state initialization

@dataclass(kw_only=True)
class GitHubTrendingStateOutput(TypedDict):
    running_summary: str  # Final summary
