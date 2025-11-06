# Testing Strategy: BFS/DFS Problem Solving System

This document provides a roadmap for testing the keep-agent-running system with real-world use cases.

## Quick Links

- **[USE_CASES.md](USE_CASES.md)** - 7 detailed real-world use cases with task decomposition
- **[examples/support_ticket_example.py](examples/support_ticket_example.py)** - Runnable example implementation

## Available Handlers (All Implemented)

| Handler | Purpose | Speed | Cost | Best For |
|---------|---------|-------|------|----------|
| **LLMTaskHandler** | Complex reasoning & synthesis | Slow | High | Strategic decisions, analysis |
| **SmolModelTaskHandler** | Fast specialized tasks | Fast | Low | Classification, simple extraction |
| **WebSearchTaskHandler** | Real-time information | Medium | Low | Facts, current events, research |
| **HumanTaskHandler** | Expert judgment | Very Slow | High | High-stakes decisions, reviews |
| **ToolCallTaskHandler** | Deterministic execution | Very Fast | Very Low | APIs, databases, calculations |

## Recommended Testing Sequence

### Phase 1: Proof of Concept (Week 1-2)
**Goal**: Validate core BFS/DFS orchestration works

**Use Case**: Customer Support Tickets (Use Case 6)
- ✅ Well-defined problem
- ✅ Clear success criteria (ticket resolved or escalated)
- ✅ Uses multiple handler types
- ✅ Demonstrates both BFS (triage) and DFS (investigation)

**Handlers Needed**: SmolModel, LLM, Tool, Human (optional)

**Success Metrics**:
- 80%+ of tickets classified correctly
- Simple tickets resolved in <5 minutes
- Complex tickets escalated appropriately
- Zero infinite loops

**Implementation**:
```bash
cd /Users/xuyijun/projects/keep-agent-running
python examples/support_ticket_example.py
```

---

### Phase 2: Information Synthesis (Week 3-4)
**Goal**: Test wide BFS search and synthesis capabilities

**Use Case**: Competitive Market Analysis (Use Case 2)
- Tests web search integration
- Requires synthesizing diverse sources
- BFS for broad coverage, DFS for key competitors

**Handlers Needed**: WebSearch (heavy), LLM, SmolModel, Tool

**Success Metrics**:
- Finds 90%+ of relevant competitors
- Identifies key differentiators
- Stays within token budget
- Generates actionable insights

---

### Phase 3: Deep Investigation (Week 5-6)
**Goal**: Test DFS with backtracking and hypothesis testing

**Use Case**: Bug Investigation (Use Case 3)
- Tests deep DFS paths
- Requires backtracking when hypotheses fail
- Tool-heavy (logs, metrics, traces)

**Handlers Needed**: Tool (heavy), SmolModel, LLM, Human

**Success Metrics**:
- Correct root cause identified 70%+ of time
- Efficient backtracking (max 3 failed hypotheses)
- Human escalation works smoothly
- Post-mortem generated

---

### Phase 4: Complex Multi-Modal (Week 7-10)
**Goal**: Test full system with all handlers

**Use Case**: Technical Due Diligence (Use Case 1)
- Uses all 5 handler types
- Long-running (multi-day)
- High-stakes decisions
- Complex convergence criteria

**Handlers Needed**: All

**Success Metrics**:
- Comprehensive coverage of assessment areas
- Human experts consulted at right times
- Final report meets professional standards
- Completed within time/budget constraints

---

## Key Questions to Answer Through Testing

### 1. BFS vs DFS Strategy Selection
- **Question**: When should the orchestrator choose BFS vs DFS?
- **Test**: Compare outcomes on same problem with forced BFS vs forced DFS
- **Expected Learning**: BFS better for unknown problems, DFS better when confident

### 2. Handler Selection Accuracy
- **Question**: Does the system route tasks to appropriate handlers?
- **Test**: Manual review of 100 task assignments
- **Expected Learning**: 80%+ correct assignments, identify common mistakes

### 3. Convergence Effectiveness
- **Question**: Does the system know when to stop?
- **Test**: Track termination reasons (quality threshold, timeout, human approval, etc.)
- **Expected Learning**: Natural convergence 60%+, forced termination 40%-

### 4. Human Integration Quality
- **Question**: Are humans brought in at the right time with the right context?
- **Test**: Survey human participants on clarity and timeliness of requests
- **Expected Learning**: Identify friction points in human handoffs

### 5. Cost Optimization
- **Question**: Can we reduce costs while maintaining quality?
- **Test**: Vary mix of SmolModel vs LLM, measure cost vs quality tradeoff
- **Expected Learning**: SmolModel suitable for 60-70% of subtasks

### 6. Parallelism Benefits
- **Question**: Does BFS parallelism improve time-to-solution?
- **Test**: Compare serial execution vs parallel (up to 10 concurrent tasks)
- **Expected Learning**: 3-5x speedup on information gathering tasks

### 7. Loop Detection Necessity
- **Question**: How often do loops occur without loop detection?
- **Test**: Disable loop detector, measure loop frequency
- **Expected Learning**: Loops occur in 10-20% of complex tasks

---

## Metrics Dashboard

### Quantitative Metrics

```python
{
    # Efficiency
    "avg_time_to_resolution": "15 minutes",
    "tasks_per_second": 5.2,
    "parallel_utilization": "65%",
    
    # Cost
    "avg_cost_per_task": "$0.15",
    "llm_tokens_used": 125000,
    "human_hours_saved": 8.5,
    
    # Quality
    "task_completion_rate": "92%",
    "human_escalation_rate": "12%",
    "solution_accuracy": "87%",
    
    # Reliability
    "timeout_rate": "5%",
    "loop_detection_triggers": 3,
    "handler_failures": "2%",
}
```

### Qualitative Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **Output Quality** | 8/10 | Good structure, occasionally verbose |
| **Handler Selection** | 7/10 | Sometimes uses LLM when SmolModel would suffice |
| **Convergence** | 6/10 | Tends to over-explore, timeout too common |
| **Human Experience** | 9/10 | Clear handoffs, good context provided |

---

## Known Challenges & Mitigations

### Challenge 1: Context Explosion
**Problem**: Long-running tasks accumulate massive context
**Mitigation**: 
- Implement aggressive context pruning
- Use shared knowledge base (PROJECT.md pattern)
- Periodic context summarization with SmolModel

### Challenge 2: Handler Selection Ambiguity
**Problem**: Sometimes unclear which handler to use
**Mitigation**:
- Provide handler capability descriptions to orchestrator
- Allow handlers to reject tasks and suggest alternatives
- Learn from human override patterns

### Challenge 3: Premature Convergence
**Problem**: System stops before finding optimal solution
**Mitigation**:
- Multi-criteria convergence (not just one condition)
- Quality gates at each milestone
- Human checkpoint before final termination

### Challenge 4: Human Availability
**Problem**: Humans are slow, asynchronous, sometimes unavailable
**Mitigation**:
- Graceful timeout handling
- Queue for human review (process async)
- Escalation chains (L1 → L2 → L3)

### Challenge 5: Tool Failures
**Problem**: External tools/APIs fail frequently
**Mitigation**:
- Retry logic with exponential backoff
- Circuit breaker pattern
- Fallback to alternative handlers

---

## Production Readiness Checklist

### Core Functionality
- [x] Task decomposition (orchestration)
- [x] Handler routing (task assignment)
- [x] All 5 handler types implemented
- [ ] Web search implementation (currently stub)
- [ ] Convergence manager implementation
- [ ] Loop detector implementation

### Reliability
- [ ] Error handling for all handlers
- [ ] Retry logic with backoff
- [ ] Circuit breaker for external services
- [ ] Graceful degradation
- [ ] Dead letter queue for failed tasks

### Observability
- [ ] Structured logging for all operations
- [ ] Metrics collection (Prometheus/Datadog)
- [ ] Execution graph visualization
- [ ] Cost tracking per task
- [ ] Performance profiling

### Human Integration
- [ ] Notification system (email/Slack/PagerDuty)
- [ ] Human response queue/dashboard
- [ ] Escalation workflow
- [ ] Feedback collection
- [ ] Human-in-the-loop training data

### Cost & Performance
- [ ] Token usage optimization
- [ ] Smart model selection (Smol vs LLM)
- [ ] Parallel execution (up to 10 concurrent)
- [ ] Request batching where possible
- [ ] Caching for repeated queries

### Security & Compliance
- [ ] API key management (vault/secrets)
- [ ] Input validation and sanitization
- [ ] Output filtering (PII, secrets)
- [ ] Audit logging
- [ ] Access control for handlers

---

## Next Steps

### Immediate (This Week)
1. ✅ Implement all handler types
2. ✅ Create USE_CASES.md with 7 detailed scenarios
3. ✅ Build support ticket example
4. ⏳ Implement WebSearchTaskHandler (connect to real API)
5. ⏳ Test support ticket example end-to-end

### Short Term (Next 2 Weeks)
1. Implement ConvergenceManager with multi-criteria termination
2. Build LoopDetector for infinite loop prevention
3. Add execution graph visualization
4. Implement proper error handling and retries
5. Run support ticket use case with 100 test tickets

### Medium Term (Next Month)
1. Implement SharedContext for cross-task knowledge sharing
2. Build competitive analysis use case (Use Case 2)
3. Add metrics collection and dashboard
4. Cost optimization: tune SmolModel vs LLM usage
5. Human escalation workflow with real notifications

### Long Term (Next Quarter)
1. Full technical due diligence system (Use Case 1)
2. Production deployment with monitoring
3. A/B testing of BFS vs DFS vs Hybrid strategies
4. Machine learning for handler selection
5. Self-improving system (learn from human corrections)

---

## Resources

### Documentation
- [README.md](README.md) - Architecture overview
- [USE_CASES.md](USE_CASES.md) - Detailed use cases
- [handlers.py](src/keep_agent_running/models/handlers.py) - Handler implementations

### Examples
- [support_ticket_example.py](examples/support_ticket_example.py) - Full working example
- [main2.py](main2.py) - Simple orchestration example

### Configuration
- [config.py](src/keep_agent_running/config.py) - System configuration
- [pyproject.toml](pyproject.toml) - Dependencies

### References
- OpenAI Swarm - Single-agent control loop patterns
- Google ADK - Hierarchical multi-agent composition
- Microsoft AutoGen - Conversation-based orchestration
- Cursor AI - 10+ parallel agents, background processing
- Claude Code - Subagent specialization, context sharing

---

## Getting Help

For questions or issues:
1. Review the USE_CASES.md for inspiration
2. Check examples/ directory for working code
3. Read handler implementations in models/handlers.py
4. Experiment with main2.py or support_ticket_example.py

Remember: Start simple (support tickets), validate the approach, then scale to complex use cases (due diligence, research reports).

