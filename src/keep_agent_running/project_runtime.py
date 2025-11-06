from typing import Callable

class Model:
    ...

class TaskHandler:
    ...


class TreeStructure:
    ...

    def pretty_print(self) -> None:
        ...


class ConvergenceManager:
    ...


def printing_callback(message: str) -> None:
    print(message)



def run_project(
    orchestration_model: Model,              # how to do it
    object_or_query: str,                    # what to do
    task_handlers: list[TaskHandler],        # what resources can be used
    convergence_manager: ConvergenceManager, # how to stop
    streaming_callback: Callable[[str], None], # how to stream the results
) -> TreeStructure:
    ...




if __name__ == "__main__":
    t = run_project(
        orchestration_model=Model(),
        object_or_query="",
        task_handlers=[],
        convergence_manager=ConvergenceManager(),
        streaming_callback=printing_callback,
    )
    t.pretty_print()