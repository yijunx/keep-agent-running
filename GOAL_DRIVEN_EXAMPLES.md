# Goal-Driven BFS/DFS: Same Goal, Different Paths

## The Core Insight

Your system is **goal-driven** and **context-aware**. The same high-level goal decomposes into completely different tasks based on the starting situation.

**Analogy**: Losing weight from 200kg→120kg vs 130kg→120kg
- Same goal: Get to 120kg
- Different starting states: 200kg vs 130kg
- Completely different approaches needed:
  - 200kg → Surgery + hospital care + long-term diet (10+ steps, high complexity)
  - 130kg → Just diet and exercise (3-4 steps, medium complexity)

## Demonstrated in Code

### Demo: Math Tutor

**File**: `examples/math_tutor_demo.py`

**Same Goal**: "Solve for x"

#### Context A: Simple Linear Equation
```
Problem: 2x + 5 = 15
Starting State: Easy problem, student knows basics

System generates: 2-step plan
├── Step 1: Subtract 5 → 2x = 10
└── Step 2: Divide by 2 → x = 5

Time: 20 seconds
Analogy: "130kg → 120kg" (diet adjustment)
```

#### Context B: Quadratic Equation
```
Problem: x² - 5x + 6 = 0
Starting State: Medium problem, needs factoring

System generates: 6-step plan
├── Step 1: Identify coefficients
├── Step 2: Check factorability
├── Step 3: Find factor pairs
├── Step 4: Factor to (x-2)(x-3)=0
├── Step 5: Solve x-2=0 → x=2
└── Step 6: Solve x-3=0 → x=3

Time: 45 seconds
Analogy: "170kg → 120kg" (diet + exercise)
```

#### Context C: Word Problem
```
Problem: Train speed calculation, solve for time
Starting State: Complex, must translate to math first

System generates: 10+ step plan
├── Step 1: Identify what we're solving for
├── Step 2: Calculate current speed (120/2)
├── Step 3: Calculate new speed (+20)
├── Step 4: Recall distance formula
├── Step 5: Set up equation
├── Step 6: Solve equation
├── Step 7: Simplify fraction
├── Step 8: Convert to decimal
├── Step 9: Convert to time format
└── Step 10: Verify reasonableness

Time: 90 seconds
Analogy: "200kg → 120kg" (surgery + care)
```

### Production Example: Bug Investigation

**File**: `USE_CASES.md` - Use Case 3

**Same Goal**: "Fix the bug"

#### Scenario A: Minor UI Bug
```
Context: Button text truncates on mobile
Severity: Low, cosmetic only

System generates: 5-task plan
├── Quick CSS check
├── Test on devices
├── Generate fix
├── Stage test
└── Quick review

Time: 30 minutes
Team: 1 developer
Analogy: "130kg → 120kg"
```

#### Scenario B: Intermittent Failure  
```
Context: 5% checkout failures, unclear pattern
Severity: Medium, $5K/day loss

System generates: 25-task plan
├── [BFS] 8 parallel triage checks
├── [DFS] Hypothesis testing
│   ├── Check DB connection pool
│   ├── Analyze logs
│   ├── Review configs
│   └── Senior engineer review
├── Reproduce issue
└── Deploy fix

Time: 2-3 hours
Team: 3-4 engineers
Analogy: "170kg → 120kg"
```

#### Scenario C: Critical Outage
```
Context: Payment system down, 0% success rate
Severity: CRITICAL, $200K/hour loss

System generates: 100+ task plan
├── [BFS] 20+ emergency parallel checks
├── [DFS] Multiple deep investigation paths
│   ├── Path 1: Payment gateway (6+ tasks)
│   ├── Path 2: Database failure (8+ tasks)
│   ├── Path 3: Code deployment (10+ tasks)
│   └── ... more paths
├── Human coordination (incident commander)
├── Executive updates
├── Emergency fixes/rollbacks
└── Post-incident review

Time: 4-8 hours
Team: All hands on deck
Analogy: "200kg → 120kg"
```

## Why This Matters

### Traditional Approach (Bad)
```
Goal: Solve problem
→ Fixed template:
  1. Analyze
  2. Plan
  3. Execute
  4. Verify

Same 4 steps for EVERY problem, regardless of complexity!
```

### Goal-Driven BFS/DFS (Good)
```
Goal: Solve problem
→ Context: What's the starting state?
  ├── Simple context → 2-5 tasks (shallow BFS/DFS)
  ├── Medium context → 20-30 tasks (medium depth)
  └── Complex context → 100+ tasks (deep, parallel)

Task breakdown ADAPTS to situation!
```

## Key Characteristics

### 1. Context Analysis
The orchestrator first analyzes:
- **Complexity**: How hard is this?
- **Severity**: How urgent?
- **Resources**: What do we have?
- **Constraints**: What are the limits?

### 2. Adaptive Decomposition
Based on context, generates:
- **Different number of tasks**: 2 vs 6 vs 100+
- **Different depth**: Shallow vs deep investigation
- **Different breadth**: Few vs many parallel paths
- **Different handlers**: Tools vs LLM vs Human

### 3. Dynamic Execution
As execution progresses:
- **Backtrack** if hypothesis fails
- **Go deeper** if needed
- **Escalate** to humans when stuck
- **Terminate** when goal reached (or impossible)

## Running the Demos

### Math Tutor (Best demonstration)
```bash
python examples/math_tutor_demo.py
```

Output shows:
- 3 problems with same goal
- Different decompositions (2 vs 6 vs 10+ steps)
- Execution time scales with complexity
- Clear analogy to weight loss (130→120 vs 200→120)

### What You'll See
```
Problem A: 2x+5=15
  → 2 steps | 20 seconds | "Diet adjustment"

Problem B: x²-5x+6=0  
  → 6 steps | 45 seconds | "Diet + exercise"

Problem C: Word problem
  → 10+ steps | 90 seconds | "Surgery + care"
```

## Comparison to Other Approaches

### Fixed Workflow (Zapier, n8n)
```
Problem: Rigid paths
Cannot adapt to context
One size fits all
```

### Rule-Based (Traditional IF-THEN)
```
Problem: Exponential rules needed
Must pre-define all scenarios
Brittle when conditions change
```

### Goal-Driven BFS/DFS (This System)
```
✓ Analyzes context automatically
✓ Generates appropriate plan
✓ Adapts during execution
✓ Handles unknown situations
```

## Implementation Notes

### The Orchestrator's Job
```python
def orchestrate(goal: str, context: dict):
    # 1. Analyze context
    complexity = analyze_complexity(context)
    
    # 2. Generate appropriate plan
    if complexity == "simple":
        tasks = generate_shallow_plan(goal)  # 2-5 tasks
    elif complexity == "medium":
        tasks = generate_medium_plan(goal)   # 20-30 tasks
    else:
        tasks = generate_deep_plan(goal)     # 100+ tasks
    
    # 3. Execute with appropriate strategy
    if complexity == "simple":
        execute_dfs(tasks)  # Quick, sequential
    elif complexity == "medium":
        execute_hybrid(tasks)  # Some parallel, some deep
    else:
        execute_bfs_then_dfs(tasks)  # Wide search, then focus
```

### Key: Not Templates, But Reasoning
The orchestrator doesn't use templates. It **reasons about the problem**:
- "This is a simple linear equation → 2 steps needed"
- "This is quadratic → needs factoring → 6 steps"
- "This is a word problem → must translate first → 10+ steps"

The LLM itself does this reasoning, creating truly adaptive decomposition.

## Further Reading

- **[DEMO_USE_CASES.md](DEMO_USE_CASES.md)** - 8 simple demos
- **[USE_CASES.md](USE_CASES.md)** - 7 production scenarios
- **[examples/math_tutor_demo.py](examples/math_tutor_demo.py)** - Runnable code
- **[examples/README.md](examples/README.md)** - Demo guide

---

**Bottom Line**: Your BFS/DFS system isn't just a search algorithm. It's a **goal-driven planning system** that adapts its approach based on the starting situation, just like a doctor prescribing different treatments for 200kg vs 130kg patients trying to reach 120kg.

That's the power of LLM-orchestrated task decomposition! 🎯

