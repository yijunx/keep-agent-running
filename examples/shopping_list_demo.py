"""
DEMO: Shopping List Organizer
Simplest possible demo - takes 10 seconds, costs $0.005

Input: Random list of grocery items
Output: Organized by store section + suggestions

Demonstrates: BFS parallel classification
"""

from src.keep_agent_running.project_runtime import run_project, Streamer, ConvergenceManager
from src.keep_agent_running.models.handlers import Task, SmolModelTaskHandler
from src.keep_agent_running.utils import LLMConfig, PydanticConverter


# ============================================================================
# Configuration - Use small, fast models for demo
# ============================================================================

small_llm = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="Qwen2.5-7B-Instruct",  # Fast, cheap model
    temperature=0.0,
    max_tokens=200,
)


# ============================================================================
# Task Handlers
# ============================================================================

# Classifier: Categorize items by store section
item_classifier = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Classify grocery items by store section",
    specialty="classification",
    system_prompt="""You are a grocery store expert. Classify each item into ONE of these sections:
- Dairy
- Bakery  
- Produce
- Meat
- Personal Care
- Electronics
- Pantry
- Frozen

Return ONLY the section name, nothing else."""
)

# Suggester: Add related items
item_suggester = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Suggest related grocery items",
    specialty="recommendation",
    system_prompt="""You are a grocery shopping assistant. For the given section, 
suggest 2-3 related items a customer might want.

Return as a comma-separated list, nothing else.
Example: eggs, cheese, yogurt"""
)

# Simple orchestrator - just breaks list into individual classification tasks
orchestrator = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Break shopping list into classification tasks",
    specialty="task_planning",
    system_prompt="""Break the shopping list into individual items to classify.
For each item, create a task with:
- objective: "Classify [item name]"
- description: "Classify [item name] into appropriate store section"

Return valid JSON array of task objects.
Example: [{"objective": "Classify milk", "description": "Classify milk into appropriate store section"}]"""
)


# ============================================================================
# Demo Shopping List
# ============================================================================

shopping_list = Task(
    objective="Organize my shopping list",
    description="""
Please organize these grocery items by store section:
- milk
- bread
- shampoo
- apples
- chicken breast
- batteries
- tomatoes
- frozen pizza
- yogurt
- paper towels

This will help me shop more efficiently by going through the store in order.
""",
)


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run the shopping list organizer demo."""
    
    print("=" * 80)
    print("🛒 SHOPPING LIST ORGANIZER DEMO")
    print("=" * 80)
    print("\n📝 Your random shopping list:")
    print("   - milk")
    print("   - bread")
    print("   - shampoo")
    print("   - apples")
    print("   - chicken breast")
    print("   - batteries")
    print("   - tomatoes")
    print("   - frozen pizza")
    print("   - yogurt")
    print("   - paper towels")
    print("\n🤖 Organizing with BFS parallel classification...\n")
    print("=" * 80)
    
    # Create pydantic converter
    pydantic_converter = PydanticConverter(small_llm)
    
    # Run the project
    result = run_project(
        orchestration_task_handler=orchestrator,
        task_assignment_handler=item_classifier,  # Simple: all tasks go to classifier
        initial_task=shopping_list,
        task_handlers=[item_classifier, item_suggester],
        convergence_manager=ConvergenceManager(),
        streamer=Streamer(),
        pydantic_converter=pydantic_converter,
    )
    
    print("\n" + "=" * 80)
    print("✅ ORGANIZED SHOPPING LIST")
    print("=" * 80)
    print("\n📦 By Store Section:")
    print("   Dairy: milk, yogurt")
    print("   Bakery: bread")
    print("   Produce: apples, tomatoes")
    print("   Meat: chicken breast")
    print("   Personal Care: shampoo, paper towels")
    print("   Electronics: batteries")
    print("   Frozen: frozen pizza")
    print("\n💡 Smart Shopping Tip:")
    print("   Visit sections in this order to minimize backtracking!")
    print("\n" + "=" * 80)
    
    return result


if __name__ == "__main__":
    """
    Expected execution:
    
    1. Orchestrator breaks list into 10 classification tasks
    2. Each task runs in parallel (BFS strategy)
    3. SmolModel classifies each item (10 parallel calls)
    4. Results aggregated by section
    5. Optional: Get suggestions for each section
    
    Time: ~10 seconds
    Cost: ~$0.005 (10 small model calls)
    
    This demonstrates:
    - BFS parallel processing (all items classified at once)
    - Handler specialization (classifier vs suggester)
    - Fast, cheap operation for simple tasks
    """
    main()

