# Documentation Index

All project documentation is organized here.

## 📚 Documentation Structure

### Quick Start
- **[../README.md](../README.md)** - Main project overview, quick start guide

### Use Cases & Examples

#### Demo Use Cases (Simple, Runnable)
- **[DEMO_USE_CASES.md](DEMO_USE_CASES.md)** - 8 simple demos (10s - 3min each)
  - Shopping List Organizer
  - Recipe Finder (Human-in-the-Loop)
  - Email Triage
  - Math Tutor (Goal-Driven)
  - Meeting Notes
  - Product Descriptions
  - Code Review
  - Trip Planner

#### Production Use Cases (Real-World)
- **[USE_CASES.md](USE_CASES.md)** - 7 production scenarios
  - Technical Due Diligence
  - Competitive Market Analysis
  - Bug Investigation (Context-Driven)
  - Research Report Generation
  - Infrastructure Migration
  - Customer Support Tickets
  - Content Creation Pipeline

### Core Concepts

#### Goal-Driven Decomposition
- **[GOAL_DRIVEN_EXAMPLES.md](GOAL_DRIVEN_EXAMPLES.md)** - Understanding context-aware planning
  - Same goal, different paths (200kg→120kg vs 130kg→120kg)
  - Math tutor examples
  - Bug investigation scenarios

#### Traversal Strategies
- **[STRATEGY_SUMMARY.md](STRATEGY_SUMMARY.md)** - Quick reference for all strategies
- **[TRAVERSAL_STRATEGIES.md](TRAVERSAL_STRATEGIES.md)** - Complete guide to BFS/DFS/A*/Beam Search/etc
  - 9+ strategies explained
  - When to use each
  - BFS vs DFS with unlimited resources
- **[STRATEGY_IMPLEMENTATION.md](STRATEGY_IMPLEMENTATION.md)** - How to add new strategies (with code)

### Development & Testing

#### Runtime
- **[RUNTIME_REVIEW.md](RUNTIME_REVIEW.md)** - Current `run_project` function analysis
  - What's fixed
  - What's sufficient for demos
  - What's missing for production
  - Phased development roadmap

#### Testing
- **[TESTING_STRATEGY.md](TESTING_STRATEGY.md)** - Complete testing roadmap
  - 4-phase testing sequence
  - Metrics and success criteria
  - Production readiness checklist

---

## 📖 Reading Paths

### For New Users (Start Here)
1. [../README.md](../README.md) - Overview
2. [DEMO_USE_CASES.md](DEMO_USE_CASES.md) - Simple examples
3. [../examples/README.md](../examples/README.md) - Run the demos
4. [GOAL_DRIVEN_EXAMPLES.md](GOAL_DRIVEN_EXAMPLES.md) - Understand the core concept

### For Developers
1. [RUNTIME_REVIEW.md](RUNTIME_REVIEW.md) - Understand current implementation
2. [STRATEGY_SUMMARY.md](STRATEGY_SUMMARY.md) - Learn traversal strategies
3. [STRATEGY_IMPLEMENTATION.md](STRATEGY_IMPLEMENTATION.md) - How to add features
4. [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Testing approach

### For Production Planning
1. [USE_CASES.md](USE_CASES.md) - Real-world scenarios
2. [RUNTIME_REVIEW.md](RUNTIME_REVIEW.md) - Feature roadmap
3. [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Production readiness
4. [TRAVERSAL_STRATEGIES.md](TRAVERSAL_STRATEGIES.md) - Advanced strategies

---

## 🎯 Quick Links by Topic

### Understanding the System
- [GOAL_DRIVEN_EXAMPLES.md](GOAL_DRIVEN_EXAMPLES.md) - Core insight: context-aware planning
- [STRATEGY_SUMMARY.md](STRATEGY_SUMMARY.md) - Why BFS/DFS/Hybrid matters

### Running Demos
- [DEMO_USE_CASES.md](DEMO_USE_CASES.md) - All demo descriptions
- [../examples/README.md](../examples/README.md) - How to run them
- [../examples/](../examples/) - Actual demo code

### Adding Features
- [STRATEGY_IMPLEMENTATION.md](STRATEGY_IMPLEMENTATION.md) - Add new strategies
- [RUNTIME_REVIEW.md](RUNTIME_REVIEW.md) - What to add next

### Production Deployment
- [USE_CASES.md](USE_CASES.md) - Real scenarios to solve
- [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - How to validate
- [RUNTIME_REVIEW.md](RUNTIME_REVIEW.md) - Production roadmap

---

## 📊 Document Stats

| Document | Size | Purpose | Audience |
|----------|------|---------|----------|
| DEMO_USE_CASES.md | ~500 lines | Simple examples | Everyone |
| USE_CASES.md | ~500 lines | Production scenarios | Product, Eng |
| GOAL_DRIVEN_EXAMPLES.md | ~280 lines | Core concept | Everyone |
| STRATEGY_SUMMARY.md | ~140 lines | Quick reference | Developers |
| TRAVERSAL_STRATEGIES.md | ~680 lines | Deep dive | Advanced developers |
| STRATEGY_IMPLEMENTATION.md | ~400 lines | Implementation guide | Developers |
| RUNTIME_REVIEW.md | ~485 lines | Current status + roadmap | Developers, PM |
| TESTING_STRATEGY.md | ~340 lines | Testing approach | QA, Developers |

**Total**: ~3,300 lines of documentation

---

## 🔄 Cross-References

Documents reference each other for deeper dives:

```
README.md
  ├─→ DEMO_USE_CASES.md ──→ examples/
  ├─→ USE_CASES.md
  └─→ STRATEGY_SUMMARY.md
      └─→ TRAVERSAL_STRATEGIES.md
          └─→ STRATEGY_IMPLEMENTATION.md

GOAL_DRIVEN_EXAMPLES.md
  ├─→ DEMO_USE_CASES.md
  └─→ USE_CASES.md

TESTING_STRATEGY.md
  ├─→ USE_CASES.md
  ├─→ DEMO_USE_CASES.md
  └─→ RUNTIME_REVIEW.md
```

---

## 💡 Pro Tips

1. **First time?** Start with README.md → DEMO_USE_CASES.md → Run examples
2. **Want to understand?** Read GOAL_DRIVEN_EXAMPLES.md - it's the key insight!
3. **Building features?** STRATEGY_IMPLEMENTATION.md has copy-paste code
4. **Planning production?** USE_CASES.md + RUNTIME_REVIEW.md + TESTING_STRATEGY.md
5. **Lost?** Come back to this INDEX.md for orientation

---

**Last Updated**: 2024-01-07  
**Maintained By**: keep-agent-running team

