from typing import Callable
from pydantic import BaseModel
from typing import Type

from .utils import PydanticConverter, LLMConfig
from .models.handlers import Task, TaskHandler


class HighLevelTask(BaseModel):
    identifier: str
    description: str
    upstreams: list[str]


class ProjectProperties(BaseModel):
    general_objective: str  # create recipy for dinner
    heuristics: str
    precautions: list[str]
    success_criteria: list[str]
    # contraint on budget (this dinner cost, within 400)
    # time whole cooking process, within 1 hour

    high_level_workflow: list[HighLevelTask] # paragraph or bullet points
    # as a reference for runner

    things_to_inlude_in_output: list[str]

    input_description: str
    # how does your project user state his specific needs
    # more for tooltips
    # pls describe what you want to eat, what left in your frigde, what appliances you have
    # any market near by, so the project runs better

    # ...
    resources: list["Resource"]


class TreeStructure:
    ...

    def pretty_print(self) -> None: ...


class ConvergenceManager: ...


class Situation: ...


class Streamer:
    def stream(self, message: str) -> None:
        print(message)


def run_project(
    project_properties: ProjectProperties,
    orchestration_task_handler: TaskHandler,  # how to do it (the planner)
    task_assignment_handler: TaskHandler,  # how to assign tasks to resources (the router)
    initial_task: Task,  # what to do, the goal
    task_handlers: list[TaskHandler],  # what resources can be used
    convergence_manager: ConvergenceManager,  # how to stop
    streamer: Streamer,  # how to stream the stuff out
    pydantic_converter: PydanticConverter,
) -> TreeStructure:
    r = orchestration_task_handler.handle(initial_task)
    tasks: list[Task] = pydantic_converter.convert_into_pydantic_model_list(r, Task)
    streamer.stream(f"Tasks: {tasks}")

    total_tasks_generated = len(tasks)
    total_tasks_completed = 0

    while tasks:
        task = tasks.pop(0)
        # choose a handler
        task_handler = task_assignment_handler.handle(task)
        result = task_handler.handle(task)

        # update situation
        convergence_manager.update_situation(result)
        total_tasks_completed += 1        
        # see if we add new tasks to the queue, based on the goal
        task_of_generating_new_tasks = Task(
            objective="Generate new tasks",
            description="Generate new tasks based on the goal",
        )
        new_tasks = orchestration_task_handler.handle(task_of_generating_new_tasks)
        new_tasks = pydantic_converter.convert_into_pydantic_model_list(new_tasks, Task)
        tasks.extend(new_tasks)
        total_tasks_generated += len(new_tasks)
        





