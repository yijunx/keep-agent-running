"""
Mock implementations for testing the protocol interfaces
These are print-based implementations that demonstrate the flow
"""

from typing import Dict, Any, List, Optional, AsyncGenerator
from datetime import datetime
import asyncio
import uuid
from dataclasses import dataclass, field

from .protocols import (
    Task,
    TaskStatus,
    TaskPriority,
    TaskResult,
    Situation,
    VirtualEnvironment,
    User,
    ConvergenceManager,
    LoopDetector,
    SharedContext,
    Verifier,
    TreeStructure,
    TaskRouter,
    RuntimeEngine,
)


@dataclass
class MockTask:
    """Mock implementation of Task protocol"""

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.NORMAL
    parent_task_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def can_execute(self) -> bool:
        print(f"📋 Checking if task {self.id} can execute...")
        return self.status == TaskStatus.PENDING and not self.dependencies

    def get_context(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "metadata": self.metadata,
        }

    def update_status(self, status: TaskStatus, message: Optional[str] = None) -> None:
        old_status = self.status
        self.status = status
        self.updated_at = datetime.now()
        print(f"📋 Task {self.id}: {old_status.value} → {status.value}")
        if message:
            print(f"   Message: {message}")


@dataclass
class MockVE:
    """Mock implementation of VirtualEnvironment protocol"""

    name: str
    model_type: str = "mock-model"
    capabilities: List[str] = field(default_factory=lambda: ["reasoning", "coding"])
    is_available: bool = True
    load_factor: float = 0.5

    async def execute_task(self, task: Task) -> TaskResult:
        print(f"🤖 VE '{self.name}' executing task: {task.description}")

        # Simulate processing time
        await asyncio.sleep(0.1)

        # Mock result generation
        artifacts = [f"Result artifact from {self.name} for task {task.id}"]
        new_tasks = []

        # Sometimes create subtasks (simulate branching)
        if "complex" in task.description.lower():
            subtask = MockTask(
                description=f"Subtask of {task.description}", parent_task_id=task.id
            )
            new_tasks.append(subtask)
            print(f"   📋 Created subtask: {subtask.id}")

        result = TaskResult(
            success=True,
            artifacts=artifacts,
            new_tasks=new_tasks,
            messages=[f"Completed by {self.name}"],
            metadata={"handler": self.name, "model": self.model_type},
            execution_time=0.1,
        )

        print(f"   ✅ Task completed successfully")
        return result

    def get_status(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "available": self.is_available,
            "load": self.load_factor,
        }

    def can_handle_task(self, task: Task) -> bool:
        # Simple logic: can handle most tasks if available
        can_handle = self.is_available and self.load_factor < 0.9
        if can_handle:
            print(f"🤖 VE '{self.name}' can handle task {task.id}")
        return can_handle


@dataclass
class MockUser:
    """Mock implementation of User protocol"""

    id: str
    name: str
    expertise: List[str] = field(default_factory=lambda: ["general"])
    is_available: bool = True
    response_time_avg: float = 30.0

    async def handle_task(self, task: Task) -> TaskResult:
        print(f"👤 Human expert '{self.name}' handling task: {task.description}")

        # Simulate human response time
        await asyncio.sleep(0.2)

        result = TaskResult(
            success=True,
            artifacts=[f"Human-reviewed result for task {task.id}"],
            new_tasks=[],
            messages=[f"Reviewed and approved by {self.name}"],
            metadata={"handler": self.name, "type": "human"},
            execution_time=0.2,
        )

        print(f"   ✅ Human review completed")
        return result

    def can_handle_task(self, task: Task) -> bool:
        # Humans can handle tasks requiring their expertise
        task_needs_human = (
            "review" in task.description.lower()
            or "critical" in task.description.lower()
        )
        can_handle = self.is_available and task_needs_human
        if can_handle:
            print(f"👤 Human '{self.name}' can handle task {task.id}")
        return can_handle


class MockConvergenceManager:
    """Mock implementation of ConvergenceManager protocol"""

    def should_terminate(
        self, situation: Situation, runtime_config: Dict[str, Any]
    ) -> bool:
        # Check various termination criteria
        token_limit = runtime_config.get("token_limit", 1000000)
        time_limit = runtime_config.get("time_limit", 3600)

        should_stop = (
            situation.total_tokens_used > token_limit
            or situation.execution_time > time_limit
            or (situation.current_task_count == 0 and situation.completed_tasks > 0)
        )

        if should_stop:
            print(f"⏹️ Convergence manager: Termination criteria met")
            print(f"   Tokens: {situation.total_tokens_used}/{token_limit}")
            print(f"   Time: {situation.execution_time:.1f}s/{time_limit}s")
            print(f"   Tasks: {situation.current_task_count} pending")

        return should_stop

    def detect_infinite_loop(self, execution_history: List[Dict[str, Any]]) -> bool:
        # Simple loop detection based on repeated states
        if len(execution_history) > 10:
            recent_states = execution_history[-5:]
            if len(set(str(state) for state in recent_states)) < 3:
                print(f"🔄 Infinite loop detected!")
                return True
        return False

    def calculate_progress_score(self, situation: Situation) -> float:
        if situation.completed_tasks == 0:
            return 0.0

        total_tasks = (
            situation.completed_tasks
            + situation.failed_tasks
            + situation.current_task_count
        )
        progress = situation.completed_tasks / total_tasks if total_tasks > 0 else 0.0

        print(f"📈 Progress score: {progress:.2f}")
        return progress

    def suggest_intervention(self, situation: Situation) -> Optional[str]:
        if situation.failed_tasks > situation.completed_tasks:
            return "High failure rate - consider human intervention"
        return None


class MockLoopDetector:
    """Mock implementation of LoopDetector protocol"""

    def __init__(self):
        self.state_history: List[str] = []
        self.max_history = 20

    def record_state(self, state_snapshot: Dict[str, Any]) -> None:
        state_str = str(sorted(state_snapshot.items()))
        self.state_history.append(state_str)

        # Keep only recent history
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)

    def is_loop_detected(self) -> bool:
        if len(self.state_history) < 3:
            return False

        # Check for repeated patterns
        current_state = self.state_history[-1]
        count = self.state_history.count(current_state)

        is_loop = count > 2
        if is_loop:
            print(f"🔄 Loop detector: Repeated state detected ({count} times)")

        return is_loop

    def reset(self) -> None:
        print(f"🔄 Loop detector: Resetting state history")
        self.state_history.clear()


class MockSharedContext:
    """Mock implementation of SharedContext protocol"""

    def __init__(self):
        self.knowledge_base: Dict[str, Any] = {}
        self.conventions: Dict[str, Any] = {
            "coding_style": "python-black",
            "test_framework": "pytest",
            "documentation": "google-style",
        }

    def get_shared_knowledge(self) -> Dict[str, Any]:
        print(f"📚 Accessing shared knowledge: {len(self.knowledge_base)} items")
        return self.knowledge_base.copy()

    def update_shared_knowledge(self, key: str, value: Any) -> None:
        self.knowledge_base[key] = value
        print(f"📚 Updated shared knowledge: {key} = {value}")

    def get_project_conventions(self) -> Dict[str, Any]:
        print(f"📋 Project conventions loaded")
        return self.conventions.copy()


class MockVerifier:
    """Mock implementation of Verifier protocol"""

    def verify_task_completion(self, task: Task, result: TaskResult) -> bool:
        verified = result.success and len(result.artifacts) > 0
        print(f"✅ Task {task.id} verification: {'PASS' if verified else 'FAIL'}")
        return verified

    def validate_result_quality(self, result: TaskResult) -> float:
        # Mock quality score based on artifacts and messages
        quality = 0.8 if result.success else 0.2
        print(f"⭐ Result quality score: {quality}")
        return quality

    def check_goal_satisfaction(
        self, original_query: str, current_artifacts: List[Any]
    ) -> float:
        # Mock satisfaction based on number of artifacts
        satisfaction = min(len(current_artifacts) * 0.3, 1.0)
        print(f"🎯 Goal satisfaction: {satisfaction:.2f}")
        return satisfaction


class MockTreeStructure:
    """Mock implementation of TreeStructure protocol"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.execution_path: List[str] = []
        self.parent_child: Dict[str, List[str]] = {}

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task
        self.execution_path.append(task.id)

        if task.parent_task_id:
            if task.parent_task_id not in self.parent_child:
                self.parent_child[task.parent_task_id] = []
            self.parent_child[task.parent_task_id].append(task.id)

        print(f"🌳 Added task {task.id} to execution tree")

    def get_execution_path(self) -> List[str]:
        return self.execution_path.copy()

    def get_tree_depth(self) -> int:
        # Calculate max depth
        def get_depth(task_id: str) -> int:
            children = self.parent_child.get(task_id, [])
            if not children:
                return 1
            return 1 + max(get_depth(child_id) for child_id in children)

        root_tasks = [
            tid for tid, task in self.tasks.items() if task.parent_task_id is None
        ]
        depth = max(get_depth(root_id) for root_id in root_tasks) if root_tasks else 0
        print(f"🌳 Tree depth: {depth}")
        return depth

    def visualize_tree(self) -> str:
        return f"Tree with {len(self.tasks)} tasks, depth {self.get_tree_depth()}"


class MockTaskRouter:
    """Mock implementation of TaskRouter protocol"""

    def route_task(
        self,
        task: Task,
        available_ves: List[VirtualEnvironment],
        available_users: List[User],
    ) -> Optional[Any]:
        print(f"🚦 Routing task {task.id}: {task.description}")

        # First try human experts for critical tasks
        for user in available_users:
            if user.can_handle_task(task):
                print(f"   → Routed to human: {user.name}")
                return user

        # Then try VEs
        for ve in available_ves:
            if ve.can_handle_task(task):
                print(f"   → Routed to VE: {ve.name}")
                return ve

        print(f"   ❌ No available handler found")
        return None

    def get_routing_strategy(self) -> str:
        return "priority-based (human-first for critical tasks)"


class MockProjectRuntime(RuntimeEngine):
    """Mock implementation of the main RuntimeEngine"""

    async def initialize(self) -> None:
        print(f"🔧 Initializing runtime components...")

        # Initialize components
        self.execution_graph = MockTreeStructure()
        self.verifier = MockVerifier()
        self.task_router = MockTaskRouter()

        # Initial situation
        self.current_situation = Situation(
            current_task_count=0,
            completed_tasks=0,
            failed_tasks=0,
            total_tokens_used=0,
            memory_usage="0MB",
            execution_time=0.0,
            active_agents=0,
            last_update=datetime.now(),
            status_summary="Initialized",
        )

        print(f"   ✅ Runtime initialized")

    async def decompose_initial_query(self) -> List[Task]:
        print(f"🧩 Decomposing query: '{self.object_or_query}'")

        # Mock decomposition - create a few initial tasks
        tasks = [
            MockTask(
                description=f"Analyze requirements for: {self.object_or_query}",
                priority=TaskPriority.HIGH,
            ),
            MockTask(
                description=f"Design solution architecture",
                priority=TaskPriority.NORMAL,
            ),
            MockTask(
                description=f"Create complex implementation plan",
                priority=TaskPriority.NORMAL,
            ),
        ]

        for task in tasks:
            self.execution_graph.add_task(task)
            print(f"   📋 Created task: {task.id} - {task.description}")

        return tasks

    async def execute_task_loop(self) -> None:
        print(f"🔄 Starting task execution loop...")

        iteration = 0
        max_iterations = 10  # Safety limit for demo

        while self.should_continue() and iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")

            if not self.tasks:
                print(f"📭 No tasks in queue")
                break

            # Get next task (DFS/BFS logic would go here)
            current_task = self.tasks.pop(0)  # Simple FIFO for demo
            current_task.update_status(TaskStatus.IN_PROGRESS)

            # Route task to handler
            handler = self.task_router.route_task(
                current_task, self.ves_models, self.expert_allowed
            )

            if not handler:
                print(f"❌ No handler available for task {current_task.id}")
                current_task.update_status(TaskStatus.FAILED, "No handler available")
                continue

            # Execute task
            try:
                if isinstance(handler, MockUser):
                    result = await self.handle_task_human(current_task, handler)
                else:
                    result = await self.handle_task_automated(current_task, handler)

                # Verify result
                if self.verifier.verify_task_completion(current_task, result):
                    current_task.update_status(TaskStatus.COMPLETED)
                    self.artifacts_generated.extend(result.artifacts)

                    # Add new tasks if any
                    if result.new_tasks:
                        self.tasks.extend(result.new_tasks)
                        for new_task in result.new_tasks:
                            self.execution_graph.add_task(new_task)
                else:
                    current_task.update_status(TaskStatus.FAILED, "Verification failed")

            except Exception as e:
                print(f"❌ Error executing task {current_task.id}: {e}")
                current_task.update_status(TaskStatus.FAILED, str(e))

            # Update situation and check convergence
            self.update_situation()

            # Record state for loop detection
            state_snapshot = {
                "task_count": len(self.tasks),
                "completed": self.current_situation.completed_tasks,
                "failed": self.current_situation.failed_tasks,
            }
            self.loop_prevention.record_state(state_snapshot)

            if self.loop_prevention.is_loop_detected():
                print(f"🛑 Loop detected - terminating")
                break

        print(f"\n🏁 Task execution loop completed after {iteration} iterations")

    async def handle_task_automated(
        self, task: Task, ve: VirtualEnvironment
    ) -> TaskResult:
        print(f"🤖 Handling task via automation...")
        return await ve.execute_task(task)

    async def handle_task_human(self, task: Task, user: User) -> TaskResult:
        print(f"👤 Handling task via human expert...")
        return await user.handle_task(task)

    def update_situation(self) -> None:
        if not self.current_situation:
            return

        # Count task statuses
        completed = len(
            [
                t
                for t in self.execution_graph.tasks.values()
                if t.status == TaskStatus.COMPLETED
            ]
        )
        failed = len(
            [
                t
                for t in self.execution_graph.tasks.values()
                if t.status == TaskStatus.FAILED
            ]
        )

        # Update situation
        self.current_situation.current_task_count = len(self.tasks)
        self.current_situation.completed_tasks = completed
        self.current_situation.failed_tasks = failed
        self.current_situation.total_tokens_used += 1000  # Mock token usage
        self.current_situation.execution_time = (
            (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        )
        self.current_situation.last_update = datetime.now()

        print(
            f"📊 Situation updated - Tasks: {len(self.tasks)} pending, "
            f"{completed} completed, {failed} failed"
        )

    def should_continue(self) -> bool:
        if not self.current_situation:
            return True

        # Check convergence criteria
        should_stop = self.convergence_manager.should_terminate(
            self.current_situation, self.stop_criteria
        )

        return not should_stop and len(self.tasks) > 0

    async def finalize(self) -> Dict[str, Any]:
        print(f"🎯 Finalizing runtime execution...")

        final_results = {
            "success": True,
            "total_tasks": len(self.execution_graph.tasks),
            "completed_tasks": self.current_situation.completed_tasks,
            "failed_tasks": self.current_situation.failed_tasks,
            "artifacts_generated": len(self.artifacts_generated),
            "execution_time": self.current_situation.execution_time,
            "tree_depth": self.execution_graph.get_tree_depth(),
            "final_situation": self.current_situation,
        }

        print(f"   ✅ Total tasks: {final_results['total_tasks']}")
        print(f"   ✅ Completed: {final_results['completed_tasks']}")
        print(f"   ❌ Failed: {final_results['failed_tasks']}")
        print(f"   📄 Artifacts: {final_results['artifacts_generated']}")
        print(f"   ⏱️ Execution time: {final_results['execution_time']:.1f}s")

        return final_results
