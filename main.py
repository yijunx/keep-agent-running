"""
Main entry point for the Keep Agent Running project runtime engine
Demonstrates the complete flow using mock implementations
"""

import asyncio
from datetime import datetime

from src.keep_agent_running.config import settings
from src.keep_agent_running.mock_implementations import (
    MockProjectRuntime, MockVE, MockUser, MockConvergenceManager,
    MockLoopDetector, MockSharedContext
)


async def create_demo_runtime() -> MockProjectRuntime:
    """Create a demo runtime with mock components"""

    print("🔧 Setting up demo runtime components...")

    # Create Virtual Environments
    ves = [
        MockVE(name="GPT-4-Advanced", model_type="gpt-4", capabilities=["reasoning", "coding", "analysis"]),
        MockVE(name="Claude-3.5-Sonnet", model_type="claude-3.5", capabilities=["reasoning", "writing", "coding"]),
        MockVE(name="Code-Specialist", model_type="code-llm", capabilities=["coding", "debugging", "refactoring"])
    ]

    # Create Human Experts
    experts = [
        MockUser(id="expert-1", name="Senior Architect", expertise=["architecture", "distributed-systems"]),
        MockUser(id="expert-2", name="ML Specialist", expertise=["machine-learning", "data-science"]),
        MockUser(id="expert-3", name="DevOps Engineer", expertise=["deployment", "monitoring", "infrastructure"])
    ]

    # Create supporting components
    convergence_manager = MockConvergenceManager()
    loop_detector = MockLoopDetector()
    shared_context = MockSharedContext()

    print(f"   🤖 Created {len(ves)} virtual environments")
    print(f"   👥 Created {len(experts)} human experts")
    print(f"   🎯 Configured convergence management")

    # Create runtime with configuration
    runtime = MockProjectRuntime(
        orchestration_models=settings.default_orchestration_model,
        object_or_query="Build a scalable real-time data processing system with monitoring",
        ves_models=ves,
        expert_allowed=experts,
        stop_criteria={
            "token_limit": settings.resources.max_token_budget,
            "time_limit": settings.resources.max_session_timeout,
            "max_iterations": settings.resources.max_iterations,
            "quality_threshold": settings.convergence.goal_satisfaction_threshold
        },
        convergence_manager=convergence_manager,
        loop_prevention=loop_detector,
        context_manager=shared_context
    )

    return runtime


async def demonstrate_configuration():
    """Show current configuration"""

    print("\n" + "="*60)
    print("📋 CURRENT CONFIGURATION")
    print("="*60)

    print(f"🚀 Project: {settings.project_name}")
    print(f"🌍 Environment: {settings.environment}")
    print(f"🐛 Debug: {settings.debug}")
    print()

    print("🎯 Convergence Settings:")
    print(f"   Enabled: {settings.convergence.enabled}")
    print(f"   Loop Detection: {settings.convergence.loop_detection_enabled}")
    print(f"   Watchdog: {settings.convergence.watchdog_enabled}")
    print(f"   Consensus Threshold: {settings.convergence.consensus_threshold}")
    print(f"   Goal Satisfaction: {settings.convergence.goal_satisfaction_threshold}")
    print()

    print("📊 Resource Limits:")
    print(f"   Token Budget: {settings.resources.max_token_budget:,}")
    print(f"   Max Parallel Agents: {settings.resources.max_parallel_agents}")
    print(f"   Session Timeout: {settings.resources.max_session_timeout}s")
    print(f"   Max Iterations: {settings.resources.max_iterations}")
    print()

    print("⚙️ Execution Strategy:")
    print(f"   Strategy: {settings.execution.strategy}")
    print(f"   Max Tree Depth: {settings.execution.max_tree_depth}")
    print(f"   Context Sharing: {settings.execution.context_sharing_mode}")
    print()


async def run_demo_scenarios():
    """Run different demo scenarios"""

    print("\n" + "="*60)
    print("🎬 DEMO SCENARIOS")
    print("="*60)

    scenarios = [
        {
            "name": "Simple Query",
            "query": "Create a hello world application",
            "description": "Basic linear task execution"
        },
        {
            "name": "Complex Project",
            "query": "Build a distributed microservices system with real-time monitoring",
            "description": "Multi-level task decomposition with branching"
        },
        {
            "name": "Critical Review Task",
            "query": "Review and approve the security architecture for production deployment",
            "description": "Human expert involvement scenario"
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🎯 Scenario {i}: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        print(f"Query: '{scenario['query']}'")
        print("-" * 40)

        # Create runtime for this scenario
        runtime = await create_demo_runtime()
        runtime.object_or_query = scenario["query"]

        # Run the scenario
        try:
            start_time = datetime.now()
            results = await runtime.start()
            end_time = datetime.now()

            print(f"\n📊 Scenario {i} Results:")
            print(f"   Duration: {(end_time - start_time).total_seconds():.2f}s")
            print(f"   Success: {results['success']}")
            print(f"   Tasks: {results['total_tasks']} total, {results['completed_tasks']} completed")
            print(f"   Artifacts: {results['artifacts_generated']}")

        except Exception as e:
            print(f"❌ Scenario {i} failed: {e}")

        print("\n" + "-"*40)
        await asyncio.sleep(0.5)  # Brief pause between scenarios


async def test_configuration_overrides():
    """Test configuration override functionality"""

    print("\n" + "="*60)
    print("🔧 CONFIGURATION OVERRIDE TEST")
    print("="*60)

    print("Original settings:")
    print(f"   Max Parallel Agents: {settings.resources.max_parallel_agents}")
    print(f"   Execution Strategy: {settings.execution.strategy}")
    print(f"   Consensus Threshold: {settings.convergence.consensus_threshold}")
    print()

    print("💡 To override settings, use environment variables:")
    print("   export MAX_PARALLEL_AGENTS=15")
    print("   export EXECUTION_STRATEGY=dfs")
    print("   export CONVERGENCE_CONSENSUS_THRESHOLD=0.9")
    print()

    print("Or modify the .env file and restart")


async def main():
    """Main execution function"""

    print("🚀 Keep Agent Running - Project Runtime Engine Demo")
    print("=" * 60)

    try:
        # Show configuration
        await demonstrate_configuration()

        # Test configuration overrides
        await test_configuration_overrides()

        # Run demo scenarios
        await run_demo_scenarios()

        print("\n" + "="*60)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("="*60)

        print("\n🎯 What was demonstrated:")
        print("   ✅ Protocol-based architecture with clear interfaces")
        print("   ✅ Mock implementations that can be swapped with real ones")
        print("   ✅ DFS/BFS task execution with branching")
        print("   ✅ Multi-agent orchestration (VE + Human)")
        print("   ✅ Convergence management and loop detection")
        print("   ✅ Configuration management with .env")
        print("   ✅ Hierarchical task decomposition")
        print("   ✅ Industry-inspired patterns from research")

        print("\n🔧 Next steps for implementation:")
        print("   1. Replace MockVE with real AI model integrations")
        print("   2. Implement actual human workflow systems")
        print("   3. Add persistent storage for execution graphs")
        print("   4. Build real convergence algorithms")
        print("   5. Add monitoring and observability")
        print("   6. Implement advanced routing strategies")

    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        raise


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
