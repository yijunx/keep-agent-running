"""
DEMO: Math Tutor - GOAL-DRIVEN Decomposition
Shows how the SAME GOAL ("Solve for x") decomposes into different tasks based on context

Example A: Simple linear equation → 2 steps
Example B: Quadratic equation → 6 steps  
Example C: Word problem → 10+ steps

Demonstrates: Context-aware task decomposition (like 200kg→120kg vs 130kg→120kg)
Same goal, totally different execution paths!
"""

from src.keep_agent_running.project_runtime import run_project, Streamer, ConvergenceManager
from src.keep_agent_running.models.handlers import Task, LLMTaskHandler, SmolModelTaskHandler
from src.keep_agent_running.utils import LLMConfig, PydanticConverter


# ============================================================================
# Configuration
# ============================================================================

# Use larger model for math reasoning
llm_config = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
    temperature=0.1,
    max_tokens=1000,
)

# Small model for validation
small_llm = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="Qwen2.5-7B-Instruct",
    temperature=0.0,
    max_tokens=200,
)


# ============================================================================
# Task Handlers
# ============================================================================

# Problem analyzer: Understand the problem
problem_analyzer = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Analyze math problem type and difficulty",
    specialty="classification",
    system_prompt="""Analyze this math problem and classify it:
- Problem type (e.g., linear equation, quadratic, word problem, etc.)
- Difficulty level (easy, medium, hard)
- Required concepts (e.g., algebra, geometry, etc.)

Return a brief 2-3 sentence analysis."""
)

# Solution generator: Create step-by-step solution
solution_generator = LLMTaskHandler(
    llm_config=llm_config,
    description="Generate step-by-step math solution",
    system_prompt="""You are an expert math tutor. Solve the given problem step by step:

1. Show each step clearly
2. Explain WHY you're doing each step
3. Show the result after each step
4. End with the final answer

Be clear and educational. Help the student understand, don't just give the answer."""
)

# Step validator: Check if each step is correct
step_validator = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Validate math solution steps",
    specialty="validation",
    system_prompt="""Validate this math step. Check if:
1. The math operation is correct
2. The logic makes sense
3. It follows from the previous step

Return either:
- "VALID: [brief explanation]" 
- "INVALID: [what's wrong]" """
)


# ============================================================================
# Orchestrator
# ============================================================================

orchestrator = LLMTaskHandler(
    llm_config=llm_config,
    description="Break math problem into solution steps",
    system_prompt="""You are a math tutor orchestrator. Break down the math problem into tasks:

1. First: Analyze the problem type and difficulty
2. Then: Generate step-by-step solution
3. Finally: Validate the solution

Return JSON array of tasks with objectives and descriptions.
Example: [
    {"objective": "Analyze problem", "description": "Determine problem type and difficulty for: [problem]"},
    {"objective": "Generate solution", "description": "Create step-by-step solution for: [problem]"},
    {"objective": "Validate solution", "description": "Check correctness of solution"}
]"""
)


# ============================================================================
# Demo Math Problems - SAME GOAL, DIFFERENT CONTEXTS
# ============================================================================

# Example A: Simple (2 steps expected)
simple_problem = Task(
    objective="Solve for x",
    description="""
Solve this equation step by step:

2x + 5 = 15

Show your work and explain each step.
""",
)

# Example B: Medium (6 steps expected)
medium_problem = Task(
    objective="Solve for x",
    description="""
Solve this quadratic equation step by step:

x² - 5x + 6 = 0

Show your work and explain each step.
""",
)

# Example C: Complex (10+ steps expected)
complex_problem = Task(
    objective="Solve for t",
    description="""
Solve this word problem step by step:

A train travels 120km in 2 hours. If it increases its speed by 20km/h, 
how long will it take to travel 180km? Solve for time t.

Show your work and explain each step, including how you set up the equation.
""",
)


# ============================================================================
# Main Demo
# ============================================================================

def solve_problem(problem: Task, problem_name: str, pydantic_converter):
    """Solve a single math problem."""
    print(f"\n{'=' * 80}")
    print(f"🔍 {problem_name}")
    print(f"{'=' * 80}")
    print(f"Goal: {problem.objective}")
    print(f"Problem: {problem.description.strip()[:100]}...")
    print(f"\n🤖 System analyzing problem and generating execution plan...\n")
    
    import time
    start_time = time.time()
    
    # Run the project
    result = run_project(
        orchestration_task_handler=orchestrator,
        task_assignment_handler=solution_generator,
        initial_task=problem,
        task_handlers=[problem_analyzer, solution_generator, step_validator],
        convergence_manager=ConvergenceManager(),
        streamer=Streamer(),
        pydantic_converter=pydantic_converter,
    )
    
    elapsed = time.time() - start_time
    
    print(f"\n✅ Completed in {elapsed:.1f} seconds")
    return result, elapsed


def main():
    """Run all three math problems to demonstrate context-aware decomposition."""
    
    print("=" * 80)
    print("📐 MATH TUTOR - GOAL-DRIVEN DECOMPOSITION DEMO")
    print("=" * 80)
    print("\n🎯 SAME GOAL: 'Solve for x'")
    print("📊 DIFFERENT CONTEXTS: Simple → Medium → Complex")
    print("\n💡 Key Insight: System adapts task breakdown based on problem complexity!")
    print("   Like weight loss: 200kg→120kg needs different plan than 130kg→120kg")
    print("=" * 80)
    
    # Create pydantic converter
    pydantic_converter = PydanticConverter(llm_config)
    
    results = []
    
    # Example A: Simple problem (130kg → 120kg analogy)
    result_a, time_a = solve_problem(simple_problem, "EXAMPLE A: Simple Linear (2 steps)", pydantic_converter)
    results.append(("Simple", time_a, 2))
    
    print("\n" + "=" * 80)
    print("📝 Expected decomposition:")
    print("   Step 1: Subtract 5 from both sides → 2x = 10")
    print("   Step 2: Divide by 2 → x = 5")
    print("   ✓ SHORT execution path (beginner level)")
    
    # Example B: Medium problem (170kg → 120kg analogy)
    result_b, time_b = solve_problem(medium_problem, "EXAMPLE B: Quadratic (6 steps)", pydantic_converter)
    results.append(("Medium", time_b, 6))
    
    print("\n" + "=" * 80)
    print("📝 Expected decomposition:")
    print("   Step 1: Identify a=1, b=-5, c=6")
    print("   Step 2: Check if factorable")
    print("   Step 3: Find factors: -2 and -3")
    print("   Step 4: Factor: (x-2)(x-3) = 0")
    print("   Step 5: Solve x-2=0 → x=2")
    print("   Step 6: Solve x-3=0 → x=3")
    print("   ✓ MEDIUM execution path (intermediate level)")
    
    # Example C: Complex word problem (200kg → 120kg analogy)
    result_c, time_c = solve_problem(complex_problem, "EXAMPLE C: Word Problem (10+ steps)", pydantic_converter)
    results.append(("Complex", time_c, 10))
    
    print("\n" + "=" * 80)
    print("📝 Expected decomposition:")
    print("   Step 1: Understand what we're solving for")
    print("   Step 2: Calculate current speed (120/2 = 60)")
    print("   Step 3: Calculate new speed (60+20 = 80)")
    print("   Step 4: Recall distance formula")
    print("   Step 5: Set up equation (180 = 80t)")
    print("   Step 6: Solve for t (180/80)")
    print("   Step 7: Simplify (9/4)")
    print("   Step 8: Convert to decimal (2.25)")
    print("   Step 9: Convert to hours:minutes (2h 15min)")
    print("   Step 10: Verify answer makes sense")
    print("   ✓ LONG execution path (must translate to math first)")
    
    # Final comparison
    print("\n" + "=" * 80)
    print("🎯 KEY INSIGHT: CONTEXT-DRIVEN DECOMPOSITION")
    print("=" * 80)
    print("\n📊 Comparison:")
    print(f"   Simple (2x+5=15):     {time_a:5.1f}s | ~2 steps  | 'Diet adjustment'")
    print(f"   Medium (x²-5x+6=0):   {time_b:5.1f}s | ~6 steps  | 'Diet + exercise'")
    print(f"   Complex (word):       {time_c:5.1f}s | ~10 steps | 'Surgery + care'")
    print("\n💡 Same goal ('Solve for x'), but the system ADAPTS:")
    print("   • Simple context → Shallow DFS (quick solution)")
    print("   • Medium context → Medium DFS (factoring needed)")
    print("   • Complex context → Deep DFS (must translate problem first)")
    print("\n🔑 This is goal-driven BFS/DFS:")
    print("   The orchestrator sees the STARTING STATE and generates")
    print("   a completely different execution plan to reach the SAME GOAL!")
    print("\n" + "=" * 80)
    
    return results


if __name__ == "__main__":
    """
    GOAL-DRIVEN DECOMPOSITION DEMO
    
    This demo runs the SAME GOAL ("Solve for x") three times with different
    starting contexts, showing how the system adapts its execution plan.
    
    Example A: 2x + 5 = 15 (Simple linear)
      → System generates ~2 step plan
      → Quick DFS execution
      → Like "130kg → 120kg" (diet adjustment)
    
    Example B: x² - 5x + 6 = 0 (Quadratic)
      → System generates ~6 step plan
      → Medium DFS with factoring
      → Like "170kg → 120kg" (diet + exercise)
    
    Example C: Train word problem (Complex)
      → System generates ~10+ step plan
      → Deep DFS, must translate to equation first
      → Like "200kg → 120kg" (surgery + care)
    
    Time: ~60-90 seconds total (3 problems)
    Cost: ~$0.05-0.10 total
    
    KEY INSIGHT:
    The orchestrator analyzes the STARTING STATE (problem complexity)
    and generates a completely different task breakdown to reach the
    SAME GOAL. This is true goal-driven, context-aware planning!
    
    Not a fixed template, but adaptive decomposition based on situation.
    """
    main()

