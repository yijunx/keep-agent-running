from typing import Callable
from pydantic import BaseModel
from typing import Type
from openai import OpenAI

from src.keep_agent_running.utils import PydanticConverter, LLMConfig
from abc import ABC, abstractmethod



class Task(BaseModel):
    objective: str
    description: str



class TreeStructure:
    ...

    def pretty_print(self) -> None: ...


class ConvergenceManager: ...


class Situation: ...


class Streamer:
    def stream(self, message: str) -> None:
        print(message)



class TaskHandler(ABC):

    @abstractmethod
    def handle(self, task: Task) -> str:
        pass

    @abstractmethod
    def provide_description(self) -> str:
        pass

class LLMTaskHandler(TaskHandler):
    def __init__(
        self,
        llm_config: LLMConfig,
        description: str,
        system_prompt: str
    ):
        self.llm_config = llm_config
        self.description = description
        self.system_prompt = system_prompt

    def handle(self, task: Task) -> str:
        llm = OpenAI(base_url=self.llm_config.base_url, api_key=self.llm_config.api_key)
        response = llm.chat.completions.create(
            model=self.llm_config.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": task.description},
            ],
        )
        return response.choices[0].message.content

    def provide_description(self) -> str:
        return self.description


class WebSearchTaskHandler(TaskHandler):
    def __init__(
        self,
        web_search_config: WebSearchConfig,
        description: str,
        system_prompt: str
    ):
        self.web_search_config = web_search_config
        self.description = description


def run_project(
    orchestration_task_handler: TaskHandler,  # how to do it
    task_assignment_handler: TaskHandler,  # how to assign tasks to resources
    initial_task: Task,  # what to do, the goal
    task_handlers: list[TaskHandler],  # what resources can be used
    convergence_manager: ConvergenceManager,  # how to stop
    streamer: Streamer,  # how to stream the stuff out
    pydantic_converter: PydanticConverter,
) -> TreeStructure:
    r = orchestration_task_handler.handle(initial_task)
    tasks: list[Task] = pydantic_converter.convert_into_pydantic_model_list(r, Task)
    streamer.stream(f"Tasks: {tasks}")

    # while tasks:
    #     task = tasks.pop(0)
    #     task_handler = task_assignment_handler.handle(task)
    #     result = task_handler.handle(task)




