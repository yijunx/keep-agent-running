"""
Task Handlers Module

Contains all task handler implementations for the keep-agent-running project.
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from openai import OpenAI
from typing import Optional, Any, Callable, Dict
import time
from datetime import datetime

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


class HumanTaskHandlerConfig(BaseModel):
    """Configuration for human task handler."""
    timeout_seconds: int = Field(default=3600, description="How long to wait for human response")
    notification_enabled: bool = Field(default=True, description="Whether to send notifications")
    escalation_enabled: bool = Field(default=True, description="Whether to escalate on timeout")


class HumanTaskHandler(TaskHandler):
    """Handler that reaches out to humans and waits for their response."""

    def __init__(
        self,
        config: HumanTaskHandlerConfig,
        description: str,
        human_id: str,
        notification_callback: Optional[Callable[[str, Task], None]] = None,
        response_poll_callback: Optional[Callable[[str], Optional[str]]] = None,
    ):
        """
        Initialize the human task handler.

        Args:
            config: Configuration for the handler
            description: Description of what this handler does
            human_id: Identifier for the human expert
            notification_callback: Function to send notification to human
            response_poll_callback: Function to check for human response
        """
        self.config = config
        self.description = description
        self.human_id = human_id
        self.notification_callback = notification_callback
        self.response_poll_callback = response_poll_callback

    def handle(self, task: Task) -> str:
        """
        Handle a task by reaching out to a human and waiting for response.

        Args:
            task: The task to handle

        Returns:
            The human's response

        Raises:
            TimeoutError: If human doesn't respond within timeout period
        """
        # Send notification to human
        if self.notification_callback:
            self.notification_callback(self.human_id, task)

        # Poll for response
        start_time = time.time()
        while time.time() - start_time < self.config.timeout_seconds:
            if self.response_poll_callback:
                response = self.response_poll_callback(self.human_id)
                if response:
                    return response

            # Wait before polling again
            time.sleep(5)

        # Timeout handling
        if self.config.escalation_enabled:
            return f"TIMEOUT: Human {self.human_id} did not respond within {self.config.timeout_seconds}s. Task: {task.objective}"
        else:
            raise TimeoutError(f"Human {self.human_id} did not respond within timeout period")

    def provide_description(self) -> str:
        """Return the handler description."""
        return self.description


class ToolCallConfig(BaseModel):
    """Configuration for tool call handler."""
    available_tools: Dict[str, str] = Field(default_factory=dict, description="Map of tool name to description")
    timeout_seconds: int = Field(default=60, description="Timeout for tool execution")
    retry_attempts: int = Field(default=3, description="Number of retry attempts on failure")


class ToolCallTaskHandler(TaskHandler):
    """Handler that executes tool calls to process tasks."""

    def __init__(
        self,
        config: ToolCallConfig,
        description: str,
        tool_executor: Callable[[str, Dict[str, Any]], Any],
    ):
        """
        Initialize the tool call task handler.

        Args:
            config: Configuration for the handler
            description: Description of what this handler does
            tool_executor: Function that executes the tool call
        """
        self.config = config
        self.description = description
        self.tool_executor = tool_executor

    def handle(self, task: Task) -> str:
        """
        Handle a task by executing appropriate tool calls.

        Args:
            task: The task to handle

        Returns:
            Tool execution result as a string

        Raises:
            RuntimeError: If tool execution fails after all retries
        """
        # Extract tool name and parameters from task
        # In a real implementation, you'd parse the task description
        # or use an LLM to determine which tool to call
        tool_name = self._determine_tool(task)
        params = self._extract_parameters(task)

        # Execute tool with retries
        for attempt in range(self.config.retry_attempts):
            try:
                result = self.tool_executor(tool_name, params)
                return str(result)
            except Exception as e:
                if attempt == self.config.retry_attempts - 1:
                    raise RuntimeError(f"Tool execution failed after {self.config.retry_attempts} attempts: {e}")
                time.sleep(2 ** attempt)  # Exponential backoff

        raise RuntimeError("Tool execution failed")

    def _determine_tool(self, task: Task) -> str:
        """Determine which tool to use for the task."""
        # Simple implementation - in production, use LLM or rules
        return list(self.config.available_tools.keys())[0] if self.config.available_tools else "default"

    def _extract_parameters(self, task: Task) -> Dict[str, Any]:
        """Extract parameters from task description."""
        # Simple implementation - in production, parse task description
        return {"query": task.description}

    def provide_description(self) -> str:
        """Return the handler description."""
        return self.description


class SmolModelTaskHandler(TaskHandler):
    """Handler that uses smaller, specialized models for specific tasks."""

    def __init__(
        self,
        llm_config: LLMConfig,
        description: str,
        specialty: str,
        system_prompt: str,
    ):
        """
        Initialize the small model task handler.

        Args:
            llm_config: Configuration for the smaller model
            description: Description of what this handler does
            specialty: The specialty of this model (e.g., "code", "math", "translation")
            system_prompt: System prompt optimized for this model's specialty
        """
        self.llm_config = llm_config
        self.description = description
        self.specialty = specialty
        self.system_prompt = system_prompt

    def handle(self, task: Task) -> str:
        """
        Handle a task using a specialized small model.

        Args:
            task: The task to handle

        Returns:
            The model's response

        Note:
            Small models are faster and cheaper but may be less capable.
            Use them for well-defined, narrow tasks.
        """
        llm = OpenAI(
            base_url=self.llm_config.base_url,
            api_key=self.llm_config.api_key
        )

        # Add specialty context to the task
        enhanced_prompt = f"[Specialty: {self.specialty}]\n\n{task.description}"

        response = llm.chat.completions.create(
            model=self.llm_config.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": enhanced_prompt},
            ],
            temperature=self.llm_config.temperature,
            max_tokens=self.llm_config.max_tokens,
        )
        return response.choices[0].message.content

    def provide_description(self) -> str:
        """Return the handler description."""
        return f"{self.description} (Specialty: {self.specialty})"

