from typing import Callable
from pydantic import BaseModel
from typing import Type

class Model:
    ...


class Task:
    ...




class TreeStructure:
    ...

    def pretty_print(self) -> None:
        ...


class ConvergenceManager:
    ...




class Situation:
    ...

def printing_callback(message: str) -> None:
    print(message)

def make_output_into_pydantic_models(output: str, pydantic_model: Type[BaseModel], llm: Model) -> BaseModel:
    response = llm.generate(
        system_prompt=system_prompt,
        user_prompt=output,
    )
    return pydantic_model.model_validate_json(output)

class TaskHandler:
    def __init__(self, model: Model, streaming_callback: Callable[[str], None], system_prompt: str):
        self.model = model
        self.streaming_callback = streaming_callback
        self.system_prompt = system_prompt


    def handle(self, task: Task) -> list[Task]:
        


def run_project(
    orchestration_task_handler: TaskHandler,              # how to do it
    initial_task: Task,                    # what to do
    task_handlers: list[TaskHandler],        # what resources can be used
    convergence_manager: ConvergenceManager, # how to stop
    streaming_callback: Callable[[str], None], # how to stream the results
) -> TreeStructure:



    tasks: list[Task] = orchestration_task_handler.handle(intial_task)




if __name__ == "__main__":
    t = run_project(
        orchestration_model=Model(),
        object_or_query="",
        task_handlers=[],
        convergence_manager=ConvergenceManager(),
        streaming_callback=printing_callback,
    )
    t.pretty_print()