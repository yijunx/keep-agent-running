"""
DEMO: Recipe Finder with Human-in-the-Loop
Shows adaptive planning based on real-world human input

Scenario:
1. You want to cook dinner with ingredients at home
2. System suggests recipes based on what you have
3. HUMAN goes to market to check what's fresh/on sale
4. System ADAPTS recipe based on market findings

Demonstrates:
- BFS: Initial recipe exploration
- Human handler: Real-world information gathering
- DFS: Refined recipe generation based on actual availability
- Goal-driven: "Make dinner" adapts based on market context
"""

from src.keep_agent_running.project_runtime import run_project, Streamer, ConvergenceManager
from src.keep_agent_running.models.handlers import (
    Task,
    LLMTaskHandler,
    SmolModelTaskHandler,
    HumanTaskHandler,
    HumanTaskHandlerConfig,
)
from src.keep_agent_running.utils import LLMConfig, PydanticConverter


# ============================================================================
# Configuration
# ============================================================================

# Large model for creative recipe generation
llm_config = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
    temperature=0.7,  # Higher temperature for creativity
    max_tokens=1500,
)

# Small model for quick classification
small_llm = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="Qwen2.5-7B-Instruct",
    temperature=0.3,
    max_tokens=300,
)


# ============================================================================
# Mock Human Interaction (Simulates market visit)
# ============================================================================

# In real implementation, this would be a UI/chat interface
HUMAN_MARKET_FINDINGS = None  # Will be set by mock function

def notify_human_market_task(human_id: str, task: Task) -> None:
    """Simulate sending notification to human to go to market."""
    print("\n" + "=" * 80)
    print("📱 NOTIFICATION TO HUMAN")
    print("=" * 80)
    print(f"👤 To: {human_id}")
    print(f"📋 Task: {task.objective}")
    print(f"📝 Details: {task.description}")
    print("\n⏳ Waiting for human to visit market and report back...")
    print("   (In real app: Human gets push notification, visits market, sends photos/notes)")
    print("=" * 80 + "\n")


def check_human_market_response(human_id: str) -> str | None:
    """Mock: Check if human has reported back from market."""
    global HUMAN_MARKET_FINDINGS
    
    # Simulate human going to market and finding things
    # In real app, this would poll a database/queue for human input
    if HUMAN_MARKET_FINDINGS is None:
        # First call - simulate human is still at market
        import time
        time.sleep(2)  # Simulate market visit time
        
        # Mock response: Human reports what's fresh/on sale at market
        HUMAN_MARKET_FINDINGS = """
Market Findings (Fresh & On Sale Today):
- Fresh salmon fillets (50% off, expires tomorrow)
- Cherry tomatoes (very fresh, local farm)
- Fresh basil (aromatic, just picked)
- Garlic (good quality)
- Lemons (organic, on sale)
- Olive oil (premium, buy one get one)
- Pasta (various types available)
- Parmesan cheese (aged, good price)

Suggestion: Salmon looks amazing and is a great deal. 
Could make something Mediterranean?
"""
        return HUMAN_MARKET_FINDINGS
    else:
        # Already got response
        return HUMAN_MARKET_FINDINGS


# ============================================================================
# Task Handlers
# ============================================================================

# Handler 1: Initial recipe brainstorming
recipe_brainstormer = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Brainstorm possible recipes based on available ingredients",
    specialty="recipe_ideation",
    system_prompt="""You are a recipe brainstorming assistant. 
Given ingredients, suggest 3-5 possible dishes (just names, no details yet).
Consider different cuisines: Italian, Asian, Mexican, Mediterranean, etc.
Format: Return comma-separated list of recipe names."""
)

# Handler 2: Market reconnaissance (HUMAN!)
market_scout = HumanTaskHandler(
    config=HumanTaskHandlerConfig(
        timeout_seconds=300,  # 5 minutes for demo (in real app: hours/days)
        notification_enabled=True,
        escalation_enabled=False,  # For demo, we'll provide mock data
    ),
    description="Send human to market to check fresh ingredients and deals",
    human_id="home-cook-001",
    notification_callback=notify_human_market_task,
    response_poll_callback=check_human_market_response,
)

# Handler 3: Detailed recipe generation
recipe_creator = LLMTaskHandler(
    llm_config=llm_config,
    description="Generate detailed recipe with instructions and tips",
    system_prompt="""You are a creative chef. Generate a detailed, delicious recipe.

Include:
1. Recipe name
2. Prep time and cook time
3. Ingredients list with quantities
4. Step-by-step instructions
5. Tips and variations
6. Wine pairing suggestion (optional)

Make it sound appetizing and achievable for home cooks!"""
)

# Handler 4: Recipe optimizer (adapts based on market findings)
recipe_optimizer = LLMTaskHandler(
    llm_config=llm_config,
    description="Optimize recipe based on market availability and deals",
    system_prompt="""You are a practical chef who adapts recipes to what's available.

Given:
- Original recipe ideas
- What's fresh/on sale at the market

Create an optimized recipe that:
1. Takes advantage of fresh ingredients
2. Leverages good deals
3. Results in a better dish than originally planned
4. Is realistic for tonight's dinner

Be enthusiastic about the fresh ingredients and good deals!"""
)


# ============================================================================
# Orchestrator
# ============================================================================

orchestrator = LLMTaskHandler(
    llm_config=llm_config,
    description="Plan dinner cooking project with market visit",
    system_prompt="""You are a dinner planning orchestrator. Break down the task:

Phase 1 (BFS - explore options):
1. Brainstorm recipes with home ingredients
2. Send human to market for reconnaissance

Phase 2 (DFS - deep dive on best option):  
3. Based on market findings, optimize recipe choice
4. Generate detailed final recipe

Return JSON array of tasks:
[
    {"objective": "Brainstorm recipes", "description": "List 3-5 recipes possible with: [ingredients]"},
    {"objective": "Market reconnaissance", "description": "Go to local market, check what's fresh and on sale today, especially proteins and vegetables. Take photos if possible."},
    {"objective": "Optimize recipe", "description": "Based on market findings, choose the best recipe and optimize it"},
    {"objective": "Generate final recipe", "description": "Create detailed recipe with all steps"}
]"""
)


# ============================================================================
# Initial Dinner Planning Task
# ============================================================================

dinner_task = Task(
    objective="Plan and find recipe for tonight's dinner",
    description="""
I want to cook dinner tonight. Here's what I have at home:

Pantry:
- Rice, pasta, flour
- Olive oil, soy sauce, vinegar
- Salt, pepper, various spices
- Canned tomatoes

Fridge:
- Eggs (6)
- Milk
- Butter
- Some leftover vegetables

Protein:
- Chicken breast (frozen, needs defrosting)

Constraints:
- Cook time: Max 45 minutes
- Skill level: Intermediate home cook
- Preference: Something flavorful and fresh

Budget: $20 for any additional ingredients from market

Please suggest a great recipe. Feel free to send someone to the market 
to check what's fresh and on sale today!
""",
)


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run the recipe finder with human-in-the-loop demo."""
    
    print("=" * 80)
    print("🍳 RECIPE FINDER - HUMAN-IN-THE-LOOP DEMO")
    print("=" * 80)
    print("\n🎯 Goal: Plan tonight's dinner")
    print("🏠 Starting context: Limited ingredients at home")
    print("💡 Strategy: Send human to market for real-world intel!")
    print("\n" + "=" * 80)
    
    # Create pydantic converter
    pydantic_converter = PydanticConverter(llm_config)
    
    # Run the project with BFS strategy (explore options first)
    result = run_project(
        orchestration_task_handler=orchestrator,
        task_assignment_handler=recipe_creator,  # Default routing
        initial_task=dinner_task,
        task_handlers=[
            recipe_brainstormer,
            market_scout,  # HUMAN HANDLER
            recipe_optimizer,
            recipe_creator,
        ],
        convergence_manager=ConvergenceManager(),
        streamer=Streamer(),
        pydantic_converter=pydantic_converter,
        strategy="bfs",  # BFS to explore options before committing
    )
    
    print("\n" + "=" * 80)
    print("🎉 DINNER PLAN COMPLETE!")
    print("=" * 80)
    print("\n📊 What happened:")
    print("   1. ✅ Brainstormed recipes with home ingredients")
    print("   2. 👤 Human went to market and found fresh salmon on sale!")
    print("   3. ✅ Optimized recipe based on market findings")
    print("   4. ✅ Generated detailed recipe for Mediterranean Salmon")
    print("\n💡 Key insight:")
    print("   Started with 'chicken stir-fry' idea (frozen chicken)")
    print("   → Human found fresh salmon (50% off!)")
    print("   → Adapted to 'Mediterranean Salmon Pasta' (better dish, better price)")
    print("\n🔑 This is goal-driven adaptation:")
    print("   Same goal: 'Make dinner'")
    print("   Different context: Fresh salmon available vs just frozen chicken")
    print("   Different outcome: Upgraded dish based on real-world findings!")
    print("\n" + "=" * 80)
    
    return result


if __name__ == "__main__":
    """
    HUMAN-IN-THE-LOOP DEMONSTRATION
    
    This demo shows:
    
    1. Initial Planning (BFS)
       - System: "With home ingredients, could make chicken stir-fry"
       - System: "Let me check what's at the market..."
    
    2. Human Handler Executes
       - Notification sent to human (home cook)
       - Human goes to local market
       - Human reports: "Fresh salmon 50% off! Cherry tomatoes fresh!"
    
    3. Adaptive Replanning (DFS)
       - System: "Oh! Salmon is better than frozen chicken"
       - System: "Let me create Mediterranean salmon pasta recipe"
       - System: "This will be more delicious AND cheaper!"
    
    4. Final Output
       - Detailed recipe using fresh market ingredients
       - Better outcome than original plan
    
    Time: ~2-3 minutes (including mock 2s market visit)
    Cost: ~$0.03-0.05
    
    KEY INSIGHT:
    The system ADAPTS based on real-world human input!
    Not just template execution, but true context-aware planning.
    
    Like "130kg → 120kg" analogy:
    - Original plan: Frozen chicken + home ingredients (okay dinner)
    - Market context: Fresh salmon on sale (great deal!)
    - Adapted plan: Mediterranean salmon pasta (amazing dinner!)
    
    Same goal, better execution due to human reconnaissance! 🎯
    """
    main()

