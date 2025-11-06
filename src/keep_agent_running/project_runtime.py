from typing import Callable
from pydantic import BaseModel
from typing import Type

from .utils import PydanticConverter, LLMConfig
from .models.handlers import Task, TaskHandler



class TreeStructure:
    ...

    def pretty_print(self) -> None: ...


class ConvergenceManager: ...


class Situation: ...


class Streamer:
    def stream(self, message: str) -> None:
        print(message)


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




