from src.keep_agent_running.project_runtime import run_project, Task, TaskHandler, LLMConfig, PydanticConverter, Streamer, ConvergenceManager
from src.keep_agent_running.utils import LLMConfig, PydanticConverter


if __name__ == "__main__":
    initial_task = Task(
        objective="Learn how to play bass in a week",
        description="Learn how to play bass in a week, i want need to be able play root notes for my band",
    )
    t = run_project(
        initial_task=initial_task,
        orchestration_task_handler=TaskHandler(
            llm_config=LLMConfig(
                base_url="http://10.4.33.17:80/v1",
                model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
                temperature=0.1,
                max_tokens=2000,
            ),
            description="Orchestrate the project",
            system_prompt="You are an orchestrator. You are given a task and you need to orchestrate the project to complete the task.",
        ),
        task_assignment_handler=TaskHandler(
            llm_config=LLMConfig(
                base_url="http://10.4.33.17:80/v1",
                model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
                temperature=0.1,
                max_tokens=2000,
            ),
            description="Assign tasks to resources",
            system_prompt="You are a task assigner. You are given a task and you need to assign it to a resource.",
        ),
        task_handlers=[],
        convergence_manager=ConvergenceManager(),
        streamer=Streamer(),
        pydantic_converter=PydanticConverter(
            llm_config=LLMConfig(
                base_url="http://10.4.33.17:80/v1",
                model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
                temperature=0.1,
                max_tokens=2000,
            ),
        ),
    )
