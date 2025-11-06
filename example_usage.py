"""
Example usage of the Keep Agent Running configuration system
"""

from src.keep_agent_running.config import settings


def main():
    """Demonstrate configuration usage"""

    print(f"🚀 {settings.project_name} - {settings.environment.upper()} Environment")
    print(f"Debug mode: {settings.debug}")
    print()

    print("📊 Resource Configuration:")
    print(f"  Token budget: {settings.resources.max_token_budget:,}")
    print(f"  Max parallel agents: {settings.resources.max_parallel_agents}")
    print(f"  Session timeout: {settings.resources.max_session_timeout}s")
    print(f"  Memory threshold: {settings.resources.max_memory_threshold}")
    print()

    print("🎯 Convergence Settings:")
    print(f"  Convergence enabled: {settings.convergence.enabled}")
    print(f"  Loop detection: {settings.convergence.loop_detection_enabled}")
    print(f"  Watchdog enabled: {settings.convergence.watchdog_enabled}")
    print(f"  Consensus threshold: {settings.convergence.consensus_threshold}")
    print(f"  Goal satisfaction: {settings.convergence.goal_satisfaction_threshold}")
    print()

    print("🤖 Orchestration:")
    print(f"  Default model: {settings.default_orchestration_model}")
    print(f"  Available models: {', '.join(settings.available_models)}")
    print()

    print("⚙️ Execution Strategy:")
    print(f"  Strategy: {settings.execution.strategy}")
    print(f"  Max tree depth: {settings.execution.max_tree_depth}")
    print(f"  Context sharing: {settings.execution.context_sharing_mode}")
    print()

    print("👥 Human Integration:")
    print(f"  Escalation timeout: {settings.human.escalation_timeout}s")
    print(f"  Max wait time: {settings.human.max_wait_time}s")
    print(f"  Notifications: {settings.human.notification_enabled}")
    print()

    print("🖥️ Virtual Environments:")
    print(f"  Timeout: {settings.ve.timeout}s")
    print(f"  Retry attempts: {settings.ve.retry_attempts}")
    print(f"  Load balancing: {settings.ve.load_balancing}")
    print()

    print("📈 Monitoring:")
    print(f"  Logging level: {settings.monitoring.logging_level}")
    print(f"  Metrics enabled: {settings.monitoring.metrics_enabled}")
    print(f"  Dashboard enabled: {settings.monitoring.dashboard_enabled}")
    print()

    # Show API key status (without revealing actual keys)
    print("🔑 API Keys Status:")
    print(
        f"  OpenAI: {'✅ Configured' if settings.api.openai_api_key else '❌ Missing'}"
    )
    print(
        f"  Anthropic: {'✅ Configured' if settings.api.anthropic_api_key else '❌ Missing'}"
    )
    print(
        f"  Google: {'✅ Configured' if settings.api.google_api_key else '❌ Missing'}"
    )
    print()

    print("💾 Database:")
    print(f"  URL: {settings.database.url}")
    print(f"  Redis: {settings.database.redis_url}")
    print()

    # Demonstrate environment override
    print("💡 Example: Override settings with environment variables:")
    print("  export MAX_PARALLEL_AGENTS=10")
    print("  export CONVERGENCE_CONSENSUS_THRESHOLD=0.9")
    print("  export EXECUTION_STRATEGY=dfs")


if __name__ == "__main__":
    main()
