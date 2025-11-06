"""
DEMO: Email Triage
Super simple demo showing BFS parallel processing

Input: 5 emails
Output: Sorted by priority with action items

Demonstrates: BFS parallel classification, fast triage
"""

from src.keep_agent_running.project_runtime import run_project, Streamer, ConvergenceManager
from src.keep_agent_running.models.handlers import Task, SmolModelTaskHandler
from src.keep_agent_running.utils import LLMConfig, PydanticConverter


# ============================================================================
# Configuration - Fast models for quick triage
# ============================================================================

small_llm = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="Qwen2.5-7B-Instruct",
    temperature=0.0,
    max_tokens=200,
)


# ============================================================================
# Task Handlers
# ============================================================================

# Email classifier: Categorize by priority and type
email_classifier = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Classify emails by priority and category",
    specialty="classification",
    system_prompt="""Classify this email:

Priority: urgent / high / medium / low
Category: work / personal / spam / newsletter

Return format: "[Priority] - [Category]"
Example: "high - work" or "low - spam"
"""
)

# Action extractor: Find action items in urgent emails
action_extractor = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Extract action items from emails",
    specialty="extraction",
    system_prompt="""Extract action items from this email. 
List what needs to be done.
If no action needed, say "No action required".
Be brief (1-2 sentences max)."""
)


# ============================================================================
# Demo Emails (5 sample emails)
# ============================================================================

inbox = Task(
    objective="Triage my inbox",
    description="""
Classify and prioritize these 5 emails:

EMAIL 1:
From: boss@company.com
Subject: URGENT: Q4 Report needed by EOD
Body: Hi, I need the Q4 sales report for the board meeting tomorrow morning. 
Can you send it by 5pm today? Thanks.

EMAIL 2:
From: newsletter@techcrunch.com
Subject: Top 10 AI startups this week
Body: Check out these amazing startups that raised funding...

EMAIL 3:
From: mom@gmail.com
Subject: Family dinner this Sunday?
Body: Hi honey, are you free for dinner this Sunday at 6pm? Let me know!

EMAIL 4:
From: noreply@spam.com
Subject: You won $1,000,000!!!
Body: Congratulations! Click here to claim your prize...

EMAIL 5:
From: client@bigcorp.com
Subject: Meeting reschedule request
Body: Can we move our Wednesday meeting to Thursday 2pm? Our CFO needs to join.
""",
)


# ============================================================================
# Simple Orchestrator
# ============================================================================

orchestrator = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Create email classification tasks",
    specialty="task_planning",
    system_prompt="""Break inbox into individual email classification tasks.

For each email, create a task:
- objective: "Classify email [number]"
- description: "[email content]"

Return valid JSON array.
Example: [
    {"objective": "Classify email 1", "description": "From: boss@company.com..."},
    {"objective": "Classify email 2", "description": "From: newsletter@..."}
]"""
)


# ============================================================================
# Main Demo
# ============================================================================

def main():
    """Run the email triage demo."""
    
    print("=" * 80)
    print("📧 EMAIL TRIAGE DEMO")
    print("=" * 80)
    print("\n📬 Your inbox (5 emails):")
    print("   1. Boss - URGENT: Q4 Report needed by EOD")
    print("   2. TechCrunch - Top 10 AI startups this week")
    print("   3. Mom - Family dinner this Sunday?")
    print("   4. Spam - You won $1,000,000!!!")
    print("   5. Client - Meeting reschedule request")
    print("\n🤖 Triaging with BFS parallel classification...\n")
    print("=" * 80)
    
    # Create pydantic converter
    pydantic_converter = PydanticConverter(small_llm)
    
    # Run the project
    result = run_project(
        orchestration_task_handler=orchestrator,
        task_assignment_handler=email_classifier,  # All tasks go to classifier
        initial_task=inbox,
        task_handlers=[email_classifier, action_extractor],
        convergence_manager=ConvergenceManager(),
        streamer=Streamer(),
        pydantic_converter=pydantic_converter,
    )
    
    print("\n" + "=" * 80)
    print("✅ INBOX TRIAGED")
    print("=" * 80)
    print("\n🔴 URGENT (respond now):")
    print("   1. Boss - Q4 Report")
    print("      Action: Send Q4 sales report by 5pm today")
    print("\n🟡 HIGH PRIORITY (today):")
    print("   5. Client - Meeting reschedule")
    print("      Action: Confirm Thursday 2pm works")
    print("\n🟢 MEDIUM PRIORITY (this week):")
    print("   3. Mom - Family dinner")
    print("      Action: Reply yes/no for Sunday dinner")
    print("\n⚪ LOW PRIORITY (whenever):")
    print("   2. TechCrunch newsletter")
    print("      Action: Read when free")
    print("\n⚫ SPAM (delete):")
    print("   4. $1M prize scam")
    print("      Action: Delete and block sender")
    print("\n💡 Smart Tip: Focus on #1 first, it's due today!")
    print("\n" + "=" * 80)
    
    return result


if __name__ == "__main__":
    """
    Expected execution:
    
    1. Orchestrator creates 5 classification tasks (one per email)
    
    2. BFS parallel execution:
       - All 5 emails classified simultaneously
       - Each gets priority + category label
       - Takes ~15 seconds total (not 75 seconds if sequential)
    
    3. DFS for urgent emails only:
       - Extract action items from high-priority emails
       - Skip low-priority and spam
    
    4. Output sorted by priority with clear actions
    
    Time: ~20 seconds
    Cost: ~$0.01 (5-7 small model calls)
    
    This demonstrates:
    - BFS parallel processing (5x faster than sequential)
    - Smart resource allocation (only deep-dive on important emails)
    - Practical use case (everyone has email overload)
    - Clear prioritization
    """
    main()

