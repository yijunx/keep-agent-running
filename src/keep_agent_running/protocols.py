"""
Protocol definitions for the Keep Agent Running system
Defines the contracts that implementations must follow
"""

from abc import ABC, abstractmethod
from typing import Protocol, Any, Dict, List, Optional, Union, AsyncGenerator
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class TaskStatus(Enum):
    """Task execution status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class ExecutionStrategy(Enum):
    """Execution strategy for task traversal"""

    DFS = "dfs"
    BFS = "bfs"
    HYBRID = "hybrid"


@dataclass
class TaskResult:
    """Result of task execution"""

    success: bool
    artifacts: List[Any]
    new_tasks: List["Task"]
    messages: List[str]
    metadata: Dict[str, Any]
    execution_time: float
    error: Optional[str] = None


@dataclass
class Situation:
    """Current situation/context of the runtime"""

    current_task_count: int
    completed_tasks: int
    failed_tasks: int
    total_tokens_used: int
    memory_usage: str
    execution_time: float
    active_agents: int
    last_update: datetime
    status_summary: str


class Task(Protocol):
    """Protocol defining the Task interface"""

    id: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    parent_task_id: Optional[str]
    dependencies: List[str]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

    def can_execute(self) -> bool:
        """Check if task can be executed (dependencies satisfied)"""
        ...

    def get_context(self) -> Dict[str, Any]:
        """Get task execution context"""
        ...

    def update_status(self, status: TaskStatus, message: Optional[str] = None) -> None:
        """Update task status"""
        ...


class VirtualEnvironment(Protocol):
    """Protocol defining the Virtual Environment interface"""

    name: str
    model_type: str
    capabilities: List[str]
    is_available: bool
    load_factor: float

    async def execute_task(self, task: Task) -> TaskResult:
        """Execute a task in this virtual environment"""
        ...

    def get_status(self) -> Dict[str, Any]:
        """Get current VE status"""
        ...

    def can_handle_task(self, task: Task) -> bool:
        """Check if this VE can handle the given task"""
        ...


class User(Protocol):
    """Protocol defining the User/Expert interface"""

    id: str
    name: str
    expertise: List[str]
    is_available: bool
    response_time_avg: float

    async def handle_task(self, task: Task) -> TaskResult:
        """Handle a task that requires human input"""
        ...

    def can_handle_task(self, task: Task) -> bool:
        """Check if this user can handle the given task"""
        ...


class ConvergenceManager(Protocol):
    """Protocol for managing task convergence and termination"""

    def should_terminate(
        self, situation: Situation, runtime_config: Dict[str, Any]
    ) -> bool:
        """Determine if execution should terminate"""
        ...

    def detect_infinite_loop(self, execution_history: List[Dict[str, Any]]) -> bool:
        """Detect if we're in an infinite loop"""
        ...

    def calculate_progress_score(self, situation: Situation) -> float:
        """Calculate overall progress towards goal"""
        ...

    def suggest_intervention(self, situation: Situation) -> Optional[str]:
        """Suggest human intervention if needed"""
        ...


class LoopDetector(Protocol):
    """Protocol for detecting and preventing infinite loops"""

    def record_state(self, state_snapshot: Dict[str, Any]) -> None:
        """Record current state for loop detection"""
        ...

    def is_loop_detected(self) -> bool:
        """Check if a loop is detected"""
        ...

    def reset(self) -> None:
        """Reset loop detection state"""
        ...


class SharedContext(Protocol):
    """Protocol for managing shared context across agents"""

    def get_shared_knowledge(self) -> Dict[str, Any]:
        """Get shared knowledge base"""
        ...

    def update_shared_knowledge(self, key: str, value: Any) -> None:
        """Update shared knowledge"""
        ...

    def get_project_conventions(self) -> Dict[str, Any]:
        """Get project conventions (CLAUDE.md style)"""
        ...


class Verifier(Protocol):
    """Protocol for task and result verification"""

    def verify_task_completion(self, task: Task, result: TaskResult) -> bool:
        """Verify if a task was completed successfully"""
        ...

    def validate_result_quality(self, result: TaskResult) -> float:
        """Validate result quality (0.0 to 1.0)"""
        ...

    def check_goal_satisfaction(
        self, original_query: str, current_artifacts: List[Any]
    ) -> float:
        """Check how well current artifacts satisfy the original goal"""
        ...


class TreeStructure(Protocol):
    """Protocol for execution graph/tree management"""

    def add_task(self, task: Task) -> None:
        """Add a task to the execution tree"""
        ...

    def get_execution_path(self) -> List[str]:
        """Get the current execution path"""
        ...

    def get_tree_depth(self) -> int:
        """Get current tree depth"""
        ...

    def visualize_tree(self) -> str:
        """Get a string representation of the tree"""
        ...


class TaskRouter(Protocol):
    """Protocol for routing tasks to appropriate handlers"""

    def route_task(
        self,
        task: Task,
        available_ves: List[VirtualEnvironment],
        available_users: List[User],
    ) -> Union[VirtualEnvironment, User]:
        """Route a task to the most appropriate handler"""
        ...

    def get_routing_strategy(self) -> str:
        """Get current routing strategy"""
        ...


class RuntimeEngine(ABC):
    """Abstract base class for the main runtime engine"""

    def __init__(
        self,
        orchestration_models: str,
        object_or_query: str,
        ves_models: List[VirtualEnvironment],
        expert_allowed: List[User],
        stop_criteria: Dict[str, Any],
        convergence_manager: ConvergenceManager,
        loop_prevention: LoopDetector,
        context_manager: SharedContext,
    ):

        self.orchestration_models = orchestration_models
        self.object_or_query = object_or_query
        self.ves_models = ves_models
        self.expert_allowed = expert_allowed
        self.stop_criteria = stop_criteria
        self.convergence_manager = convergence_manager
        self.loop_prevention = loop_prevention
        self.context_manager = context_manager

        # Runtime state
        self.tasks: List[Task] = []
        self.current_situation: Optional[Situation] = None
        self.artifacts_generated: List[Any] = []
        self.execution_graph: Optional[TreeStructure] = None
        self.verifier: Optional[Verifier] = None
        self.task_router: Optional[TaskRouter] = None

        # Status
        self.is_running = False
        self.start_time: Optional[datetime] = None

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the runtime engine"""
        pass

    @abstractmethod
    async def decompose_initial_query(self) -> List[Task]:
        """Decompose the initial query into tasks"""
        pass

    @abstractmethod
    async def execute_task_loop(self) -> None:
        """Main task execution loop (DFS/BFS)"""
        pass

    @abstractmethod
    async def handle_task_automated(
        self, task: Task, ve: VirtualEnvironment
    ) -> TaskResult:
        """Handle a task through automated VE"""
        pass

    @abstractmethod
    async def handle_task_human(self, task: Task, user: User) -> TaskResult:
        """Handle a task through human expert"""
        pass

    @abstractmethod
    def update_situation(self) -> None:
        """Update current situation"""
        pass

    @abstractmethod
    def should_continue(self) -> bool:
        """Check if execution should continue"""
        pass

    @abstractmethod
    async def finalize(self) -> Dict[str, Any]:
        """Finalize execution and return results"""
        pass

    async def start(self) -> Dict[str, Any]:
        """Start the runtime execution"""
        print(f"🚀 Starting runtime engine...")
        print(f"📝 Query: {self.object_or_query}")
        print(f"🤖 Available VEs: {len(self.ves_models)}")
        print(f"👥 Available experts: {len(self.expert_allowed)}")

        self.is_running = True
        self.start_time = datetime.now()

        try:
            await self.initialize()
            initial_tasks = await self.decompose_initial_query()
            self.tasks.extend(initial_tasks)

            print(f"📋 Initial tasks created: {len(initial_tasks)}")

            await self.execute_task_loop()

            return await self.finalize()

        finally:
            self.is_running = False
            print(f"⏹️ Runtime engine stopped")


# Type aliases for convenience
TaskHandler = Union[VirtualEnvironment, User]
ExecutionResult = Dict[str, Any]
