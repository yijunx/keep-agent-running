"""
Task Handlers Module

Contains all task handler implementations for the keep-agent-running project.
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import Optional

from ..utils import LLMConfig


class Task(BaseModel):
    """Represents a task with an objective and description."""
    objective: str
    description: str


class TaskHandler(ABC):
    """Abstract base class for all task handlers."""

    @abstractmethod
    def handle(self, task: Task) -> str:
        """Handle a task and return the result as a string."""
        pass

    @abstractmethod
    def provide_description(self) -> str:
        """Provide a description of what this handler does."""
        pass


class LLMTaskHandler(TaskHandler):
    """Handler that uses an LLM to process tasks."""

    def __init__(
        self,
        llm_config: LLMConfig,
        description: str,
        system_prompt: str
    ):
        """
        Initialize the LLM task handler.

        Args:
            llm_config: Configuration for the vLLM-hosted LLM
            description: Description of what this handler does
            system_prompt: System prompt to use for the LLM
        """
        self.llm_config = llm_config
        self.description = description
        self.system_prompt = system_prompt

    def handle(self, task: Task) -> str:
        """
        Handle a task using the LLM.

        Args:
            task: The task to handle

        Returns:
            The LLM's response as a string
        """
        llm = OpenAI(
            base_url=self.llm_config.base_url,
            api_key=self.llm_config.api_key
        )
        response = llm.chat.completions.create(
            model=self.llm_config.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": task.description},
            ],
            temperature=self.llm_config.temperature,
            max_tokens=self.llm_config.max_tokens,
        )
        return response.choices[0].message.content

    def provide_description(self) -> str:
        """Return the handler description."""
        return self.description


class WebSearchConfig(BaseModel):
    """Configuration for web search functionality."""
    api_key: Optional[str] = Field(default=None, description="API key for web search service")
    search_engine: str = Field(default="google", description="Search engine to use")
    max_results: int = Field(default=10, description="Maximum number of search results")


class WebSearchTaskHandler(TaskHandler):
    """Handler that performs web searches to process tasks."""

    def __init__(
        self,
        web_search_config: WebSearchConfig,
        description: str,
    ):
        """
        Initialize the web search task handler.

        Args:
            web_search_config: Configuration for web search
            description: Description of what this handler does
        """
        self.web_search_config = web_search_config
        self.description = description

    def handle(self, task: Task) -> str:
        """
        Handle a task using web search.

        Args:
            task: The task to handle

        Returns:
            Search results as a string
        """
        # TODO: Implement web search functionality
        raise NotImplementedError("Web search handler not yet implemented")

    def provide_description(self) -> str:
        """Return the handler description."""
        return self.description

