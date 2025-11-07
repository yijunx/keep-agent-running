# Keep Agent Running - Project Runtime Engine

A DFS/BFS-based project runtime engine that orchestrates complex problem-solving through task decomposition, virtual environments, and collaborative execution.

## Architecture Overview

The system operates as a single engine that can run multiple projects, using a tree-based approach to break down complex queries into manageable tasks and execute them through various Virtual Environments (VEs) and human collaboration.

## Core Components

### ProjectRuntime

The main orchestration engine with the following key components:

```python
class ProjectRuntime:
    orchestration_models: str           # Key differentiator for performance across projects
    object_or_query: str               # Initial problem/query to solve
    tasks: list[Task]                  # Task queue (DFS/BFS execution)
    current_situation: Situation       # Current state of execution
    verifier: Verifier                 # Validation and verification logic
    things_to_respect: list[Any]       # Constraints and requirements

    # Resources
    ves_models: list[VE]               # Virtual Environments/Models available
    expert_allowed: list[User]         # Human experts that can be involved

    # Control & Monitoring
    stop_criteria: dict                # {token: 1000000, memory: xxx, queue_length: xxx}
    artifacts_generated: list[Artifacts] # Generated outputs
    configuration: PlanRuntimeConfig   # Runtime configuration
    execution_graph: TreeStructure    # Execution tree for tracking

    # Convergence Management (Industry-Inspired)
    convergence_manager: ConvergenceManager  # Multi-layered convergence control
    loop_prevention: LoopDetector      # Infinite loop detection and prevention
    context_manager: SharedContext     # Cross-agent knowledge sharing
```

### Execution Flow

#### 1. Initialization Phase
```
1. Engine starts with empty task queue
2. Analyzes object_or_query + things_to_respect
3. Selects appropriate VE (Virtual Environment)
4. Decomposes query into initial steps/tasks
5. Populates task queue
```

#### 2. Task Execution Phase (DFS/BFS Loop)
```
while tasks_queue is not empty and stop_criteria not met:
    1. Pick first task from queue
    2. Route to appropriate handler:
       - handle_task(Task, VE) for automated processing
       - handle_task(Task, Human) for human involvement
    3. Process task and generate artifacts
    4. Add new subtasks to queue (branching)
    5. Update execution graph
    6. Stream progress to users
```

### Task Handlers

#### Automated Task Handler
```python
def handle_task(task: Task, ve: VE) -> TaskResult:
    """
    Processes task through Virtual Environment

    Returns:
    - create_artifacts: Generated outputs
    - push_task_to_queue: New subtasks (branching)
    - stream_to_user: Progress updates
    """
```

#### Human Task Handler
```python
def handle_task(task: Task, human: User) -> TaskResult:
    """
    Handles tasks requiring human expertise

    Process:
    - Polls for human input/decisions
    - Manages timeouts and escalation
    - Integrates human feedback into workflow
    """
    while awaiting_human_input:
        try:
            result = poll_human_response()
            return process_human_input(result)
        except TimeoutException:
            handle_escalation()
```

## Task Convergence & Orchestration

*Inspired by industry leaders: OpenAI Swarm, Google ADK, Microsoft AutoGen, Cursor AI, and Claude Code*

### Multi-Layered Convergence Strategy

Based on research from leading AI companies, our system implements multiple convergence mechanisms:

```python
class ConvergenceManager:
    """Industry-inspired convergence control (OpenAI, Google, Microsoft patterns)"""

    # Termination Criteria (Multiple Exit Strategies)
    termination_conditions = {
        "resource_bounds": {"max_iterations": 100, "time_limit": 3600, "token_limit": 1000000},
        "quality_thresholds": {"goal_satisfaction": 0.95, "improvement_delta": 0.01},
        "consensus_based": {"checker_agent_approval": True, "stakeholder_signoff": False},
        "domain_constraints": {"natural_boundaries": [], "validation_rules": []}
    }

    # Loop Prevention (Cursor/Claude Code Pattern)
    loop_detection = {
        "state_revisit_limit": 3,
        "conversation_turn_cap": 50,
        "watchdog_timeouts": {"idle": 300, "stuck": 600},
        "escalation_triggers": ["resource_quota_exceeded", "infinite_recursion"]
    }
```

### Orchestration Patterns

#### 1. Hierarchical Control (Google ADK Style)
- **Parent-Child Chains**: Clear authority structure prevents chaos
- **Vertical Hand-offs**: Replace peer chatter with structured delegation
- **Goal Decomposition**: Maintain consistency through hierarchical task breakdown

#### 2. Context Sharing (Claude Code Pattern)
- **Shared Knowledge Base**: PROJECT.md equivalent for cross-agent standards
- **Incremental Context**: Each agent builds on previous work
- **Context Compression**: Aggressive state management for long sessions

#### 3. Parallel Execution (Cursor Inspired)
- **Concurrent Processing**: Up to 10 parallel agents with intelligent queuing
- **Background Tasks**: Push long-running tasks to background with notifications
- **Dynamic Scaling**: Adjust parallelism based on system load

### Industry-Proven Convergence Techniques

#### From Code Editors (Cursor/Claude Code)
```python
class DomainConstrainedConvergence:
    """Natural convergence through domain boundaries"""
    validation_layers = [
        "syntax_check",      # Basic correctness
        "logic_validation",  # Functional correctness
        "quality_gates",     # Standard compliance
        "integration_test",  # System correctness
        "stakeholder_review" # Human approval
    ]
```

#### From Multi-Agent Frameworks (AutoGen/CrewAI)
```python
class WorkflowOrchestration:
    patterns = {
        "sequential": "Linear dependencies with clear hand-offs",
        "maker_checker": "Iterative refinement loops with validation",
        "group_chat": "Limited to 3 agents for control",
        "hierarchical": "Orchestrator delegates to specialized agents"
    }
```

## Key Design Principles

### 1. Tree-Based Execution with Convergence Control
- **DFS/BFS Traversal**: Tasks executed with configurable search strategy
- **Dynamic Branching**: Controlled subtask creation with depth limits
- **State Tracking**: Full execution graph with loop detection
- **Bounded Search**: Resource limits prevent infinite expansion

### 2. Multi-Modal Processing with Context Isolation
- **Virtual Environments**: Specialized processing through various AI models
- **Human Integration**: Seamless escalation with timeout management
- **Hybrid Workflows**: Automated + human collaboration patterns
- **Context Boundaries**: Agent isolation prevents interference

### 3. Resource Management with Industry Best Practices
- **Multi-Level Stop Criteria**: Resource, quality, and consensus-based termination
- **Load Balancing**: Intelligent VE distribution with cost optimization
- **Expert Scheduling**: Human availability management with escalation paths
- **Watchdog Systems**: Proactive detection of stuck/looping agents

### 4. Artifact Generation with Version Control
- **Structured Outputs**: Typed artifacts with metadata tracking
- **Evolution Tracking**: Complete artifact lineage through execution tree
- **Export Capabilities**: Multiple output formats with quality validation
- **Rollback Support**: Safe recovery from failed convergence attempts

## Configuration

### PlanRuntimeConfig
```python
class PlanRuntimeConfig:
    # Core Execution Strategy
    execution_strategy: str        # "dfs" | "bfs" | "hybrid"
    max_depth: int                # Maximum tree depth
    parallelism_level: int        # Concurrent task execution (Cursor: up to 10)
    ve_selection_strategy: str    # How to choose VEs
    human_escalation_rules: dict  # When to involve humans

    # Convergence Control (Industry Best Practices)
    convergence_config: dict = {
        "termination_strategy": "multi_criteria",  # OpenAI/Google pattern
        "loop_prevention": True,                   # Cursor/Claude Code style
        "consensus_threshold": 0.8,               # AutoGen inspired
        "quality_gates": ["syntax", "logic", "integration"],  # Code editor pattern
        "watchdog_enabled": True,                 # Production safety
        "context_sharing_mode": "hierarchical"    # Google ADK style
    }

    # Resource Optimization (Based on Production Data)
    resource_limits: dict = {
        "token_budget": 1000000,     # Enterprise average
        "parallel_agents": 5,        # Optimal cost/performance
        "session_timeout": 3600,     # 1 hour limit
        "memory_threshold": "8GB"    # System resource cap
    }
```

## Getting Started

```python
# Initialize runtime with industry-proven patterns
runtime = ProjectRuntime(
    orchestration_models="gpt-4-advanced",
    object_or_query="Build a distributed system for real-time data processing",
    ves_models=[GPTModel(), ClaudeModel(), CodeModel()],
    expert_allowed=[senior_architect, ml_expert],

    # Multi-layered stop criteria (OpenAI/Google inspired)
    stop_criteria={
        "resource_bounds": {"token": 1000000, "memory": "8GB", "queue_length": 100},
        "quality_gates": {"goal_satisfaction": 0.95, "stakeholder_approval": True},
        "safety_limits": {"max_iterations": 200, "time_limit": 7200}
    },

    # Convergence management (Cursor/Claude Code pattern)
    convergence_manager=ConvergenceManager(
        loop_detection=True,
        context_sharing=True,
        hierarchical_control=True
    )
)

# Start execution with convergence monitoring
runtime.start(monitor_convergence=True)
```

## Quick Start - Demo Examples

Want to see it in action? Start with these simple demos:

### 🛒 Shopping List Organizer (10 seconds)
```bash
python examples/shopping_list_demo.py
```
Demonstrates BFS parallel classification. Takes random items, organizes by store section.

### 🍳 Recipe Finder with Human (2-3 minutes) ⭐ NEW!
```bash
python examples/recipe_finder_demo.py
```
Demonstrates **human-in-the-loop** + adaptive planning. Plans dinner, sends human to market, adapts recipe based on what's fresh/on sale. Shows context-driven adaptation!

### 📧 Email Triage (20 seconds)
```bash
python examples/email_triage_demo.py
```
Demonstrates BFS parallel processing. Sorts 5 emails by priority with action items.

### 📐 Math Tutor (30 seconds)
```bash
python examples/math_tutor_demo.py
```
Demonstrates DFS step-by-step breakdown + goal-driven adaptation. Solves 3 problems showing how complexity changes task decomposition.

**More demos**: See [DEMO_USE_CASES.md](documents/DEMO_USE_CASES.md) for 8 simple, runnable examples.

**Production use cases**: See [USE_CASES.md](documents/USE_CASES.md) for 7 real-world scenarios.

**Traversal strategies**: See [STRATEGY_SUMMARY.md](documents/STRATEGY_SUMMARY.md) for BFS/DFS/Best-First/Beam Search/A* and more.

---

## Status

🚧 **Under Development** - Core handlers implemented, testing with demo use cases.

## Industry Research & References

This architecture incorporates convergence strategies learned from industry leaders:

### OpenAI (2024-2025)
- **Swarm Framework**: Single-agent control loop with specialized routing
- **O1 Reasoning Models**: Built-in planning and task decomposition
- **Memory Optimization**: O(√t log t) complexity scaling techniques

### Google (2025)
- **Agent Development Kit (ADK)**: Hierarchical multi-agent composition
- **A2A Protocol**: Agent-to-agent interoperability standards
- **Vertex AI Integration**: Enterprise-grade orchestration at scale

### Microsoft (2024-2025)
- **AutoGen Evolution**: Conversation-first orchestration patterns
- **Agent Framework**: Enterprise-ready with observability and compliance
- **Production Deployments**: Novo Nordisk pharmaceutical compliance standards

### Code Editors (2024-2025)
- **Cursor AI**: 10+ parallel agents, background processing, $10B valuation
- **Claude Code**: Subagent specialization, 72.5% SWE-bench, context sharing
- **Domain Constraints**: Natural convergence through file system boundaries

### Key Convergence Insights
1. **Multiple Exit Strategies**: Never rely on single termination condition
2. **Domain Constraints**: Bounded search spaces enable convergence
3. **Hierarchical Control**: Clear authority prevents chaotic peer communication
4. **Context Sharing**: Shared knowledge bases (CLAUDE.md pattern)
5. **Resource Bounds**: Hard limits on computation, time, iterations
6. **Quality Gates**: Multi-layered validation (syntax→logic→integration)

## Next Steps

1. **Implement ConvergenceManager** with multi-criteria termination
2. **Build LoopDetector** for infinite loop prevention
3. **Create SharedContext** system for agent knowledge sharing
4. **Develop hierarchical orchestration** patterns
5. **Add watchdog systems** for stuck agent detection
6. **Implement quality gates** for validation layers
7. **Build background processing** for long-running tasks


## interations

initial_task = Task(
    objective="Learn how to play bass in a week",
    description="Learn how to play bass in a week, i want need to be able play root notes for my band",
)

gives: 
Tasks: [
Task(objective='Learn the notes on each string of the bass', description='Start by memorizing the notes on each string of the bass. Use a tuner or your phone to find the correct notes. If your friend is playing guitar, you can play together to match the notes.'), 

Task(objective='Practice playing single notes in time', description="Use a metronome or play along with some backing tracks to get the feel right. Make sure you're holding the bass correctly and have the right posture to avoid any injuries."), 

Task(objective='Learn to play root notes for common chords', description='If the band plays a chord, you should play the root note of that chord on your bass. Practice playing root notes along with the chords your band is playing.'), 

Task(objective='Practice playing root notes with the rest of the band', description="Join the band to play root notes for their chord progressions. If you can't practice with the band, you can play along with their backing track."), 

Task(objective='Learn to play root notes in different positions', description='Practice playing root notes in different positions on the fretboard. This will help you become more comfortable with the fretboard and improve your knowledge of the strings.'), 

Task(objective='Learn to play root notes in different octaves', description='Practice playing root notes in different octaves. This will help you become more comfortable with the fretboard and improve your knowledge of the strings.'), 

Task(objective='Learn to play root notes in different scales', description='Learn to play root notes in different scales. This will help you become more comfortable with the fretboard and improve your knowledge of the strings.')
]
