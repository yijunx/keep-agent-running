"""
Example: Customer Support Ticket Resolution
Use Case 6 from USE_CASES.md

This demonstrates how to use the BFS/DFS system to automatically
diagnose and resolve customer support tickets.
"""

from src.keep_agent_running.project_runtime import run_project, Streamer, ConvergenceManager
from src.keep_agent_running.models.handlers import (
    Task,
    LLMTaskHandler,
    SmolModelTaskHandler,
    HumanTaskHandler,
    HumanTaskHandlerConfig,
    ToolCallTaskHandler,
    ToolCallConfig,
    WebSearchTaskHandler,
    WebSearchConfig,
)
from src.keep_agent_running.utils import LLMConfig, PydanticConverter


# ============================================================================
# Configuration
# ============================================================================

# Main orchestration LLM (larger model for task decomposition)
orchestrator_llm = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="inarikami/DeepSeek-R1-Distill-Qwen-32B-AWQ",
    temperature=0.1,
    max_tokens=2000,
)

# Small model for quick classification and simple tasks
small_llm = LLMConfig(
    base_url="http://10.4.33.17:80/v1",
    model_name="Qwen2.5-7B-Instruct",  # Smaller, faster model
    temperature=0.0,
    max_tokens=500,
)


# ============================================================================
# Mock Tool Functions (In production, these would be real implementations)
# ============================================================================

def check_system_status(tool_name: str, params: dict) -> dict:
    """Mock: Check if there are any known system issues."""
    return {
        "status": "operational",
        "known_issues": [],
        "last_deployment": "2024-01-10 14:30:00",
    }


def check_user_permissions(tool_name: str, params: dict) -> dict:
    """Mock: Verify user's account and permissions."""
    user_id = params.get("user_id", "unknown")
    return {
        "user_id": user_id,
        "account_status": "active",
        "subscription": "premium",
        "permissions": ["export_reports", "view_analytics", "manage_team"],
    }


def query_application_logs(tool_name: str, params: dict) -> str:
    """Mock: Query application logs for errors."""
    return """
    2024-01-15 10:23:45 [ERROR] ReportExporter - Failed to generate PDF
    Error: Timeout waiting for report generation service
    User: user_12345
    Report ID: rpt_abc123
    Stack trace: ...
    """


def send_notification(human_id: str, task: Task) -> None:
    """Mock: Send notification to human support agent."""
    print(f"\n📧 NOTIFICATION sent to {human_id}")
    print(f"   Task: {task.objective}")
    print(f"   Details: {task.description}")
    print(f"   Awaiting response...\n")


def check_human_response(human_id: str) -> str | None:
    """Mock: Check if human has responded (in real system, poll a queue/database)."""
    # For demo purposes, simulate no immediate response
    return None


# ============================================================================
# Task Handlers Setup
# ============================================================================

# Handler 1: Small model for ticket classification
ticket_classifier = SmolModelTaskHandler(
    llm_config=small_llm,
    description="Classify support tickets by severity and category",
    specialty="classification",
    system_prompt="""You are a support ticket classifier. Analyze the ticket and determine:
1. Severity (low/medium/high/critical)
2. Category (account, billing, technical, feature_request)
3. Likely root cause
4. Suggested handler (automated/human_l1/human_l2)

Return a brief classification in 2-3 sentences."""
)

# Handler 2: LLM for complex ticket analysis
ticket_analyzer = LLMTaskHandler(
    llm_config=orchestrator_llm,
    description="Analyze complex support tickets and generate solutions",
    system_prompt="""You are an expert support engineer. Analyze the ticket details,
logs, and context to diagnose the issue and propose solutions. Be specific and actionable.
If the issue is unclear, list the information needed to proceed."""
)

# Handler 3: Tool for system checks
system_checker = ToolCallTaskHandler(
    config=ToolCallConfig(
        available_tools={
            "check_system_status": "Check for known system issues",
            "check_user_permissions": "Verify user account and permissions",
            "query_logs": "Query application logs for errors",
        },
        timeout_seconds=30,
        retry_attempts=3,
    ),
    description="Execute system checks and queries",
    tool_executor=lambda tool, params: {
        "check_system_status": check_system_status,
        "check_user_permissions": check_user_permissions,
        "query_logs": query_application_logs,
    }.get(tool, lambda t, p: "Unknown tool")(tool, params),
)

# Handler 4: Web search for knowledge base
knowledge_base_searcher = WebSearchTaskHandler(
    web_search_config=WebSearchConfig(
        search_engine="internal_kb",
        max_results=5,
    ),
    description="Search knowledge base for similar issues and solutions",
)

# Handler 5: Human escalation for complex cases
human_support = HumanTaskHandler(
    config=HumanTaskHandlerConfig(
        timeout_seconds=300,  # 5 minutes for demo
        notification_enabled=True,
        escalation_enabled=True,
    ),
    description="Escalate to human support agent",
    human_id="support-agent-001",
    notification_callback=send_notification,
    response_poll_callback=check_human_response,
)


# ============================================================================
# Example Support Ticket
# ============================================================================

support_ticket = Task(
    objective="Resolve customer ticket #12345: Unable to export reports",
    description="""
Customer Report:
- User: john.doe@company.com (ID: user_12345)
- Issue: "I'm trying to export my quarterly analytics report as PDF, but it keeps 
  failing with a timeout error. This is urgent as I need it for tomorrow's board meeting."
- Subscription: Premium
- Account status: Active
- Timestamp: 2024-01-15 10:23:00
- Previous tickets: None in the last 90 days
- Browser: Chrome 120.0

Steps to reproduce (according to customer):
1. Navigate to Analytics Dashboard
2. Select Q4 2024 report
3. Click "Export as PDF"
4. Wait for 2-3 minutes
5. Error appears: "Report generation timed out. Please try again."

Customer has tried:
- Refreshing the page
- Different browser (Safari)
- Clearing cache
- Waiting and trying again later
""",
)


# ============================================================================
# Task Assignment Handler
# ============================================================================

# This handler routes tasks to the appropriate specialist handler
task_router = LLMTaskHandler(
    llm_config=orchestrator_llm,
    description="Route tasks to appropriate handlers based on task requirements",
    system_prompt="""You are a task routing specialist. Given a task, determine which 
handler should process it:

Available handlers:
1. ticket_classifier - For initial ticket classification
2. ticket_analyzer - For complex ticket analysis and solution generation
3. system_checker - For checking system status, logs, and user permissions
4. knowledge_base_searcher - For searching documentation and known issues
5. human_support - For escalation to human agents (use as last resort)

Return the handler name that best matches the task requirements."""
)


# ============================================================================
# Orchestration Handler
# ============================================================================

orchestrator = LLMTaskHandler(
    llm_config=orchestrator_llm,
    description="Break down support tickets into diagnostic and resolution tasks",
    system_prompt="""You are a support ticket orchestrator. Break down the support ticket 
into a sequence of tasks to diagnose and resolve the issue. Use a BFS approach:

1. First, classify and triage (parallel quick checks)
2. Then, investigate based on triage results
3. Finally, propose and validate solution

For each subtask, specify:
- objective: What needs to be accomplished
- description: Detailed context and requirements

Return a list of tasks that will systematically resolve the ticket. Start with broad,
parallel investigations (BFS), then go deep based on findings (DFS).

Example format:
[
  {"objective": "Classify ticket severity", "description": "..."},
  {"objective": "Check system status", "description": "..."},
  ...
]

Return ONLY valid JSON array of task objects."""
)


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run the support ticket resolution system."""
    
    print("=" * 80)
    print("🎫 SUPPORT TICKET RESOLUTION SYSTEM")
    print("=" * 80)
    print(f"\nTicket: {support_ticket.objective}")
    print(f"\nCustomer Issue: {support_ticket.description[:200]}...\n")
    print("=" * 80)
    
    # Create pydantic converter for parsing LLM outputs
    pydantic_converter = PydanticConverter(orchestrator_llm)
    
    # Run the project with BFS strategy
    result = run_project(
        orchestration_task_handler=orchestrator,
        task_assignment_handler=task_router,
        initial_task=support_ticket,
        task_handlers=[
            ticket_classifier,
            ticket_analyzer,
            system_checker,
            # knowledge_base_searcher,  # Skip for now (not implemented)
            human_support,
        ],
        convergence_manager=ConvergenceManager(),
        streamer=Streamer(),
        pydantic_converter=pydantic_converter,
    )
    
    print("\n" + "=" * 80)
    print("✅ TICKET RESOLUTION COMPLETE")
    print("=" * 80)
    
    return result


if __name__ == "__main__":
    """
    Expected behavior:
    
    1. Orchestrator breaks ticket into tasks:
       - Classify severity/category
       - Check system status
       - Check user permissions  
       - Query application logs
       - Analyze logs and propose solution
       - (Possibly) Escalate to human if needed
    
    2. System executes tasks using appropriate handlers:
       - SmolModel for quick classification
       - Tool calls for system checks
       - LLM for analysis and solution generation
       - Human escalation if automation fails
    
    3. Convergence when:
       - Solution found and validated
       - Human takes over
       - Max iterations reached
       - Timeout occurs
    """
    main()

