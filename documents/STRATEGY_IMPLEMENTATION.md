# Strategy Implementation Guide

How to add new traversal strategies to `run_project()`.

## Current Implementation (BFS/DFS)

```python
def run_project(..., strategy: str = "bfs"):
    while tasks:
        if strategy == "dfs":
            task = tasks.pop()   # LIFO
        else:
            task = tasks.pop(0)  # FIFO
        
        result = execute(task)
```

**Simple**: Just change how you pop from queue!

---

## Adding Best-First Search

### Step 1: Add Priority to Task

```python
# In models/handlers.py
class Task(BaseModel):
    objective: str
    description: str
    priority: float = 0.5  # NEW: 0.0 (low) to 1.0 (high)
```

### Step 2: Add Scoring Handler

```python
# In project_runtime.py or new file
priority_scorer = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Score task priority/importance",
    specialty="scoring",
    system_prompt="""Score this task's priority from 0.0 to 1.0:
    - 1.0 = Critical, blocking, high-impact
    - 0.5 = Normal priority
    - 0.0 = Low priority, can defer
    
    Return just the number, e.g., "0.8"
    """
)
```

### Step 3: Update run_project

```python
def run_project(..., strategy: str = "bfs"):
    while tasks:
        # NEW: Score tasks if using best-first
        if strategy == "best_first":
            # Score all unscored tasks
            for task in tasks:
                if task.priority == 0.5:  # Default, not scored yet
                    score_str = priority_scorer.handle(task)
                    task.priority = float(score_str)
            
            # Sort by priority
            tasks.sort(key=lambda t: t.priority, reverse=True)
            task = tasks.pop(0)  # Highest priority
        
        elif strategy == "dfs":
            task = tasks.pop()   # LIFO
        else:
            task = tasks.pop(0)  # FIFO (BFS)
        
        result = execute(task)
```

**That's it!** Now you can do:

```python
run_project(..., strategy="best_first")
```

---

## Adding Beam Search

### Step 1: Add beam_width parameter

```python
def run_project(..., 
                strategy: str = "bfs",
                beam_width: int = 3):
    
    # Track depth
    depth = 0
    max_depth = 10
    
    while tasks and depth < max_depth:
        # Execute current level
        level_tasks = tasks[:beam_width]  # Only keep top-k
        tasks = tasks[beam_width:]  # Rest discarded
        
        # Execute and expand beam
        for task in level_tasks:
            result = execute(task)
            new_tasks = decompose_if_needed(task, result)
            tasks.extend(new_tasks)
        
        # Score and keep only top beam_width for next level
        if strategy == "beam_search":
            tasks = score_and_prune(tasks, beam_width)
        
        depth += 1
```

**Usage**:
```python
run_project(..., strategy="beam_search", beam_width=5)
```

---

## Adding Hybrid BFS→DFS

### Simple Version:

```python
def run_project(..., 
                strategy: str = "bfs",
                bfs_depth: int = 2):  # NEW parameter
    
    depth = 0
    
    while tasks:
        # First N levels: BFS
        if depth < bfs_depth:
            task = tasks.pop(0)  # FIFO = BFS
        # After N levels: DFS
        else:
            task = tasks.pop()   # LIFO = DFS
        
        result = execute(task)
        depth = calculate_depth(task)  # Track depth
```

**Usage**:
```python
# Explore broadly for 2 levels, then go deep
run_project(..., strategy="hybrid", bfs_depth=2)
```

### Smart Version:

```python
def run_project(..., strategy: str = "bfs"):
    while tasks:
        if strategy == "hybrid":
            # Let LLM decide when to switch!
            decision = orchestrator.handle(Task(
                objective="Decide strategy",
                description=f"""
                We've explored {completed_tasks} tasks.
                Current task queue: {[t.objective for t in tasks]}
                
                Should we:
                A) Continue BFS (explore more options)
                B) Switch to DFS (go deep on best option)
                
                Return just 'A' or 'B'.
                """
            ))
            
            if decision == "B":
                strategy = "dfs"  # Permanently switch
                task = tasks.pop()  # LIFO
            else:
                task = tasks.pop(0)  # FIFO
        else:
            # ... normal logic
```

**Smart!** The orchestrator decides when to switch based on progress.

---

## Adding A* Search

### Step 1: Add cost tracking

```python
class Task(BaseModel):
    objective: str
    description: str
    cost_so_far: float = 0.0  # g(n)
    estimated_remaining: float = 0.0  # h(n)
    
    @property
    def total_cost(self) -> float:
        return self.cost_so_far + self.estimated_remaining
```

### Step 2: Cost estimator

```python
cost_estimator = LLMTaskHandler(
    llm_config=llm_config,
    description="Estimate task costs",
    system_prompt="""Estimate costs for this task:
    1. cost_so_far: How much work to get here (in LLM calls)
    2. estimated_remaining: How much more to reach goal
    
    Return JSON: {"cost_so_far": 5.0, "estimated_remaining": 3.0}
    """
)
```

### Step 3: Update run_project

```python
def run_project(..., strategy: str = "bfs"):
    while tasks:
        if strategy == "astar":
            # Estimate costs for all tasks
            for task in tasks:
                if task.estimated_remaining == 0.0:
                    costs = cost_estimator.handle(task)
                    cost_data = json.loads(costs)
                    task.cost_so_far = cost_data["cost_so_far"]
                    task.estimated_remaining = cost_data["estimated_remaining"]
            
            # Sort by total cost
            tasks.sort(key=lambda t: t.total_cost)
            task = tasks.pop(0)  # Lowest cost
        else:
            # ... normal logic
        
        result = execute(task)
        
        # Update children's cost_so_far
        for new_task in new_tasks:
            new_task.cost_so_far = task.cost_so_far + 1
```

---

## Complete Strategy Enum

```python
# In project_runtime.py
from enum import Enum

class TraversalStrategy(str, Enum):
    BFS = "bfs"
    DFS = "dfs"
    BEST_FIRST = "best_first"
    ASTAR = "astar"
    BEAM_SEARCH = "beam_search"
    HYBRID = "hybrid"
    ITERATIVE_DEEPENING = "iterative_deepening"

def run_project(..., strategy: TraversalStrategy = TraversalStrategy.BFS):
    # Now type-safe and autocomplete-friendly!
```

---

## Strategy Selection by Orchestrator

**Ultimate goal**: Let the orchestrator choose the strategy!

```python
strategy_selector = LLMTaskHandler(
    llm_config=llm_config,
    description="Select optimal traversal strategy",
    system_prompt="""Given this task, which strategy is best?

    Available strategies:
    - BFS: Explore broadly, parallel, finds shortest path
    - DFS: Go deep, sequential, memory efficient
    - Best-First: Greedy, prioritize important tasks
    - Beam Search: Bounded exploration, keep top-k
    - Hybrid: BFS then DFS, balanced
    
    Consider:
    - Task complexity
    - Time constraints
    - Resource availability
    - Solution requirements (optimal vs fast)
    
    Return just the strategy name, e.g., "best_first"
    """
)

def run_project(initial_task, ...):
    # Let orchestrator pick strategy!
    strategy_decision = strategy_selector.handle(initial_task)
    strategy = TraversalStrategy(strategy_decision)
    
    # Execute with chosen strategy
    ...
```

**Example**:
```
Task: "Fix critical production bug"
Orchestrator: "Use best_first - prioritize highest-impact checks"

Task: "Write research report"  
Orchestrator: "Use hybrid - broad survey (BFS), then deep dives (DFS)"

Task: "Organize shopping list"
Orchestrator: "Use BFS - simple parallel classification"
```

**This is true goal-driven planning!** The strategy itself adapts to the task.

---

## Recommended Implementation Order

### Phase 1: ✅ Done
- [x] BFS
- [x] DFS

### Phase 2: Easy Wins (1-2 days each)
1. **Best-First** - Just add priority scoring
2. **Hybrid BFS→DFS** - Simple depth threshold
3. **Strategy selector** - Let orchestrator choose

### Phase 3: Medium Complexity (3-5 days each)
4. **Beam Search** - Add pruning logic
5. **A* Search** - Add cost estimation
6. **Iterative Deepening** - Add depth looping

### Phase 4: Advanced (1-2 weeks each)
7. **MCTS** - Add UCB calculation, simulation
8. **Bidirectional** - Add backward reasoning
9. **Adaptive strategies** - Learn from experience

---

## Testing Strategies

For each new strategy, test with:

```python
# Test 1: Verify it works
result = run_project(..., strategy="best_first")
assert result is not None

# Test 2: Compare to baseline
result_bfs = run_project(..., strategy="bfs")
result_best = run_project(..., strategy="best_first")
# best_first should use fewer tasks for same result

# Test 3: Measure metrics
assert result_best.tasks_executed < result_bfs.tasks_executed
assert result_best.time_elapsed < result_bfs.time_elapsed
```

---

## Summary

### To add a new strategy:

1. **Add data to Task** (priority, cost, etc.)
2. **Add scoring handler** (LLM evaluates tasks)
3. **Update run_project** (change task selection logic)
4. **Test** (compare to BFS/DFS)

### Key insight:

**Most strategies just change HOW you pick the next task from the queue!**

```python
# BFS
task = tasks.pop(0)

# DFS
task = tasks.pop()

# Best-First
tasks.sort(key=lambda t: t.priority, reverse=True)
task = tasks.pop(0)

# A*
tasks.sort(key=lambda t: t.total_cost)
task = tasks.pop(0)
```

The rest of the system stays the same! 🎯

