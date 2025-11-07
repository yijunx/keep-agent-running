# Real-World Use Cases for BFS/DFS Problem Solving

This document outlines practical use cases to test the keep-agent-running system's BFS/DFS task orchestration approach with multiple handler types.

## Handler Types Available

1. **LLMTaskHandler** - Large language models for reasoning and synthesis
2. **SmolModelTaskHandler** - Smaller, faster models for specific tasks
3. **WebSearchTaskHandler** - Web search for information gathering
4. **HumanTaskHandler** - Human expertise with timeout/escalation
5. **ToolCallTaskHandler** - Executable tools (APIs, scripts, databases)

---

## Use Case 1: Technical Due Diligence for Startup Acquisition

**Objective**: Evaluate a startup's technical infrastructure, codebase, and team for potential acquisition.

**Why This Tests BFS/DFS**:
- **Breadth**: Many parallel dimensions to evaluate (code quality, security, scalability, team, tech debt)
- **Depth**: Each dimension requires drilling down (e.g., security → vulnerabilities → remediation plans)
- **Multiple Handlers**: Needs all handler types working together
- **Real Value**: High-stakes decisions with $M implications

### Task Decomposition

```
Root Task: "Conduct technical due diligence on StartupXYZ"
├── [DFS] Code Quality Assessment
│   ├── [Tool] Clone and analyze repositories
│   ├── [SmolModel] Calculate code metrics (complexity, coverage, debt)
│   ├── [LLM] Identify architectural patterns and issues
│   └── [Human] Senior architect review and risk assessment
├── [BFS] Security Audit (parallel)
│   ├── [Tool] Run security scanners (Snyk, SonarQube)
│   ├── [WebSearch] Check for known vulnerabilities in dependencies
│   ├── [LLM] Analyze security architecture
│   └── [Human] Security expert sign-off
├── [BFS] Team Assessment (parallel)
│   ├── [WebSearch] Research team members' backgrounds
│   ├── [LLM] Analyze engineering culture from docs/commits
│   ├── [Human] Interview with CTO
│   └── [Human] Reference checks with previous employers
├── [BFS] Infrastructure Review (parallel)
│   ├── [Tool] Query cloud provider APIs for resource usage
│   ├── [LLM] Analyze cost efficiency and scaling patterns
│   ├── [WebSearch] Compare with industry benchmarks
│   └── [Human] Infrastructure architect review
└── [LLM] Final synthesis and recommendation report
```

**Handlers Used**: All 5
**BFS/DFS Strategy**: BFS for parallel investigations, DFS for deep dives
**Human Integration**: Critical decisions, expert reviews, interviews
**Convergence**: Time-boxed (2 weeks), quality gates at each stage

---

## Use Case 2: Competitive Market Analysis for Product Launch

**Objective**: Analyze competitive landscape before launching a new AI-powered project management tool.

**Why This Tests BFS/DFS**:
- **Wide Search Space**: Many competitors, features, markets
- **Deep Analysis**: Each competitor requires detailed breakdown
- **Time-Sensitive**: Need quick breadth-first overview, then selective depth
- **Synthesis**: Requires combining diverse data sources

### Task Decomposition

```
Root Task: "Analyze competitive landscape for AI PM tool launch in Q2"
├── [BFS] Identify Competitors
│   ├── [WebSearch] Top 20 project management tools
│   ├── [WebSearch] AI-powered PM tools specifically
│   ├── [Tool] Scrape G2/Capterra for competitor list
│   └── [SmolModel] Categorize by market segment
├── [DFS] Deep Dive on Top 5 Competitors (selected after BFS)
│   ├── For each competitor:
│   │   ├── [WebSearch] Feature list, pricing, reviews
│   │   ├── [Tool] Sign up and test product (API automation)
│   │   ├── [SmolModel] Extract and categorize features
│   │   ├── [LLM] Analyze strengths/weaknesses
│   │   └── [WebSearch] Financial data, funding, growth
├── [BFS] Market Trends (parallel)
│   ├── [WebSearch] Industry reports and analyst predictions
│   ├── [WebSearch] Customer pain points from forums/Reddit
│   ├── [Tool] Social media sentiment analysis
│   └── [LLM] Synthesize emerging patterns
├── [Human] Product team review and strategy session
└── [LLM] Generate competitive positioning document
```

**Handlers Used**: LLM, SmolModel, WebSearch, Tool, Human
**BFS/DFS Strategy**: BFS for breadth, then DFS on most relevant competitors
**Convergence**: Fixed timeline (1 week), diminishing returns on depth
**Output**: Actionable competitive positioning strategy

---

## Use Case 3: Bug Investigation - GOAL-DRIVEN Decomposition ⭐

**Objective**: Fix production bug (SAME GOAL, DIFFERENT PATHS based on severity/context)

**Why This Tests Goal-Driven BFS/DFS**:
- **Same Goal**: "Fix the bug"
- **Different Context**: Bug severity and symptoms determine completely different investigation paths
- **Adaptive Strategy**: System automatically chooses shallow vs deep investigation
- **Real Impact**: Like weight loss analogy - minor bug (130→120kg) vs critical outage (200→120kg) need different approaches

### Scenario A: Minor UI Bug (5-10 tasks, 30 minutes)

```
Context: "Button text sometimes truncates in mobile view"
Severity: Low, 0.1% users, cosmetic only
Starting State: "130kg → 120kg" (minor fix needed)

[BFS] Quick triage (3 parallel checks)
├── [Tool] Check CSS for mobile breakpoints → Found issue!
├── [Tool] Test on different screen sizes
└── [SmolModel] Review recent CSS changes

[DFS] Simple fix (shallow investigation)
├── [LLM] Generate CSS fix
├── [Tool] Test in staging
└── [Human] Quick code review (5 min)

Result: 5 tasks, 30 minutes, CSS one-liner fix
```

### Scenario B: Intermittent Failure (20-30 tasks, 2-3 hours)

```
Context: "Checkout fails for 5% of users, pattern unclear"
Severity: Medium, $5K/day loss, some users affected  
Starting State: "170kg → 120kg" (moderate investigation)

[BFS] Triage (8 parallel checks)
├── [Tool] Query error logs
├── [Tool] Check monitoring dashboards
├── [SmolModel] Analyze error patterns
├── [Tool] Check recent deployments
├── [Tool] Database metrics
├── [WebSearch] Known dependency issues
├── [Tool] Network latency checks
└── [Tool] Cache hit rates

[DFS] Follow strongest lead (medium depth)
├── Hypothesis: Database connection pool
│   ├── [Tool] Detailed DB metrics
│   ├── [SmolModel] Analyze connection code
│   ├── [LLM] Review pool configuration
│   └── [Human] Senior engineer review (30 min)
├── [Tool] Reproduce in staging
├── [LLM] Generate fix + tests
└── [Human] Engineering lead approval

Result: 25 tasks, 2-3 hours, config change + code fix
```

### Scenario C: Critical Outage (100+ tasks, 4-8 hours)

```
Context: "Payment system down, 0% success rate, revenue stopped"
Severity: CRITICAL, $200K/hour loss, all users impacted
Starting State: "200kg → 120kg" (major surgery needed)

[BFS] Emergency triage (20+ parallel checks)
├── [Tool] All system health checks
├── [Tool] Network, DB, cache, services status
├── [Tool] Recent deployments (last 24h)
├── [Tool] Third-party API status
├── [Tool] Infrastructure metrics
├── [WebSearch] Vendor status pages
├── [Human] Wake up on-call engineer IMMEDIATELY
├── [Human] Notify leadership
└── ... (15+ more parallel checks)

[DFS] Deep investigation (VERY deep, multiple paths)
├── Path 1: Payment gateway integration
│   ├── [Tool] Gateway API logs
│   ├── [Human] Contact payment vendor
│   ├── [Tool] Test API endpoints
│   ├── [LLM] Analyze API changes
│   └── [DFS] If vendor issue → escalate to their support
├── Path 2: Database failure
│   ├── [Tool] Full DB diagnostics
│   ├── [Human] DBA on call
│   ├── [Tool] Query slow queries
│   └── [DFS] If DB issue → failover to replica
├── Path 3: Code deployment issue
│   ├── [Tool] Git diff last deployment
│   ├── [Human] Original developer
│   ├── [Tool] Rollback script
│   └── [DFS] Emergency rollback if needed
├── [Human] Incident commander coordinates
├── [Human] Engineering manager briefing leadership
└── [Human] Post-incident review (after fix)

Result: 100+ tasks, 4-8 hours, may need rollback/hotfix/emergency patch
```

### Key Insight: SAME GOAL, RADICALLY DIFFERENT DECOMPOSITION

```
GOAL: "Fix the bug"

Scenario A (Minor UI bug):
  → 5 tasks, mostly tools
  → Shallow investigation
  → 30 minutes
  → One developer can handle it
  
Scenario B (Intermittent failure):  
  → 25 tasks, tools + some human
  → Medium-depth hypothesis testing
  → 2-3 hours
  → Small team involvement

Scenario C (Critical outage):
  → 100+ tasks, heavy human coordination
  → Very deep, multiple parallel investigation paths
  → 4-8 hours
  → All-hands emergency response
  → May need rollback (major intervention)

The orchestrator sees the CONTEXT (severity, impact, symptoms) and generates
a completely different task breakdown!

Just like weight loss:
- 130kg → 120kg: Diet adjustment (simple fix)
- 170kg → 120kg: Diet + exercise + monitoring (moderate)  
- 200kg → 120kg: Surgery + hospital + ongoing care (emergency)

Same goal, totally different execution plan based on starting state!
```

**Handlers Used**: Tool (dominant), SmolModel, LLM, Human (scales with severity)
**BFS/DFS Strategy**: BFS triage width scales with severity, DFS depth adapts to findings
**Convergence**: Production severity determines timeout and escalation rules
**Success Criteria**: Bug fixed, appropriate post-mortem depth

---

## Use Case 4: Research Report Generation

**Objective**: Create a comprehensive research report on "Impact of AI on Healthcare Diagnostics (2020-2025)".

**Why This Tests BFS/DFS**:
- **Large Information Space**: Thousands of papers, articles, studies
- **Quality vs Coverage**: Need to balance breadth and depth
- **Synthesis**: Combining disparate sources into coherent narrative
- **Expert Validation**: Human review of accuracy and insights

### Task Decomposition

```
Root Task: "Generate research report: AI in Healthcare Diagnostics 2020-2025"
├── [BFS] Literature Survey (wide net)
│   ├── [WebSearch] Academic papers (Google Scholar, PubMed)
│   ├── [WebSearch] Industry reports (Gartner, McKinsey)
│   ├── [WebSearch] News articles and case studies
│   ├── [SmolModel] Extract key findings from 100+ sources
│   └── [LLM] Identify major themes and trends
├── [DFS] Deep Dive on Key Themes (top 5 themes)
│   ├── Theme 1: Deep Learning for Medical Imaging
│   │   ├── [WebSearch] Find seminal papers
│   │   ├── [LLM] Analyze methodology and results
│   │   ├── [WebSearch] Real-world deployments
│   │   └── [Human] Medical expert review for accuracy
│   ├── Theme 2: FDA Approval Process Evolution
│   │   ├── [WebSearch] Regulatory documents
│   │   ├── [LLM] Summarize key changes
│   │   └── [Human] Healthcare lawyer validation
│   └── ... (repeat for other themes)
├── [BFS] Stakeholder Interviews (parallel)
│   ├── [Human] Interview 5 healthcare practitioners
│   ├── [Human] Interview 3 AI researchers
│   └── [LLM] Synthesize interview insights
├── [LLM] Draft report sections
├── [Human] Domain expert review and feedback
├── [LLM] Incorporate feedback and revise
└── [Human] Final sign-off by research director
```

**Handlers Used**: WebSearch (heavy), LLM (heavy), Human, SmolModel
**BFS/DFS Strategy**: BFS for coverage, DFS for important sub-topics
**Convergence**: Time-boxed, quality threshold, stakeholder approval
**Output**: Publication-ready research report (50-100 pages)

---

## Use Case 5: Infrastructure Migration Planning

**Objective**: Plan and execute migration from on-premise data center to AWS cloud.

**Why This Tests BFS/DFS**:
- **Complex Dependencies**: Applications, databases, networking, security
- **Risk Management**: Each service needs careful analysis
- **Parallel Planning**: Can work on multiple services simultaneously
- **Human Checkpoints**: Critical decisions require expert approval

### Task Decomposition

```
Root Task: "Plan migration of 50 services from on-prem to AWS"
├── [BFS] Service Discovery and Inventory
│   ├── [Tool] Scan network for all services and dependencies
│   ├── [Tool] Query configuration management database
│   ├── [SmolModel] Categorize services by type and complexity
│   └── [LLM] Identify dependency graph and risk factors
├── [BFS] Create Migration Waves (parallel analysis)
│   ├── Wave 1: Low-risk stateless services (20 services)
│   │   ├── [SmolModel] Estimate AWS costs
│   │   ├── [Tool] Generate Terraform templates
│   │   └── [LLM] Document migration procedures
│   ├── Wave 2: Databases and stateful services (15 services)
│   │   ├── [WebSearch] Best practices for database migration
│   │   ├── [LLM] Design migration strategy
│   │   └── [Human] DBA review and approval
│   └── Wave 3: Legacy applications (15 services)
│       ├── [LLM] Assess refactoring vs lift-and-shift
│       ├── [Human] Architecture review
│       └── [WebSearch] Research modernization patterns
├── [DFS] Detailed Planning for Each Wave
│   ├── For each service:
│   │   ├── [Tool] Analyze resource requirements
│   │   ├── [LLM] Generate migration runbook
│   │   ├── [Tool] Set up AWS infrastructure (Terraform)
│   │   ├── [SmolModel] Create testing checklist
│   │   └── [Human] DevOps team review
├── [Human] Executive approval for migration plan and budget
├── [Tool] Execute migrations with automated rollback
└── [Human] Post-migration validation and sign-off
```

**Handlers Used**: Tool (heavy), LLM, SmolModel, Human, WebSearch
**BFS/DFS Strategy**: BFS for inventory and wave planning, DFS per service
**Convergence**: Milestone-based, quality gates, risk assessment
**Success Criteria**: All services migrated, zero downtime, budget met

---

## Use Case 6: Customer Support Ticket Resolution

**Objective**: Automatically diagnose and resolve (or escalate) customer support tickets.

**Why This Tests BFS/DFS**:
- **Variable Complexity**: Some tickets are simple, others need deep investigation
- **Resource Optimization**: Use small models for common issues, humans for complex
- **Escalation Path**: Clear human handoff when automated resolution fails
- **High Volume**: Need efficient BFS for triage

### Task Decomposition

```
Root Task: "Resolve customer ticket #12345: 'Unable to export reports'"
├── [SmolModel] Classify ticket severity and category
├── [BFS] Quick Resolution Attempts (parallel)
│   ├── [Tool] Check system status and known issues
│   ├── [WebSearch] Search knowledge base for similar issues
│   ├── [Tool] Verify customer's account status and permissions
│   └── [SmolModel] Generate potential solutions from past tickets
├── IF no quick resolution → [DFS] Deep Investigation
│   ├── [Tool] Reproduce issue in test environment
│   ├── [Tool] Check application logs for user's actions
│   ├── [SmolModel] Analyze error patterns
│   ├── [LLM] Correlate with recent code changes
│   └── IF still unresolved → [Human] Escalate to L2 support
├── [SmolModel] Draft response to customer
├── IF complex → [Human] Review response before sending
└── [Tool] Send response and update ticket status
```

**Handlers Used**: SmolModel (heavy for efficiency), Tool, LLM, WebSearch, Human
**BFS/DFS Strategy**: BFS for quick wins, DFS only when necessary
**Convergence**: Time-based escalation (5min → L1, 30min → L2, 2hr → L3)
**Success Criteria**: CSAT score >4.5, resolution time <2 hours

---

## Use Case 7: Content Creation Pipeline

**Objective**: Create a multi-format marketing campaign (blog posts, social media, videos, emails).

**Why This Tests BFS/DFS**:
- **Multiple Outputs**: Many parallel work streams
- **Review Cycles**: Human feedback at multiple stages
- **Iterative Refinement**: May need to revise based on feedback
- **Mixed Creativity/Analysis**: Different handler strengths

### Task Decomposition

```
Root Task: "Create Q2 product launch campaign for AI Analytics Platform"
├── [BFS] Research and Strategy
│   ├── [WebSearch] Competitor marketing analysis
│   ├── [WebSearch] Target audience pain points
│   ├── [Tool] Analyze past campaign performance (Google Analytics)
│   └── [LLM] Generate campaign themes and messaging
├── [Human] Marketing director approves strategy
├── [BFS] Content Creation (parallel streams)
│   ├── Blog Posts (3 articles)
│   │   ├── [LLM] Generate outlines
│   │   ├── [LLM] Write first drafts
│   │   ├── [Human] Editor review and feedback
│   │   ├── [LLM] Revise based on feedback
│   │   └── [Human] Final approval
│   ├── Social Media (20 posts)
│   │   ├── [SmolModel] Generate post variations
│   │   ├── [Tool] Create graphics (DALL-E API)
│   │   └── [Human] Review and schedule
│   ├── Email Campaign (5 emails)
│   │   ├── [LLM] Write email copy
│   │   ├── [Tool] A/B test subject lines (ML model)
│   │   └── [Human] Approval before sending
│   └── Video Scripts (2 videos)
│       ├── [LLM] Generate scripts
│       ├── [Human] Video producer review
│       └── [Human] Record and edit
├── [Tool] Schedule all content in CMS
└── [Tool] Set up tracking and analytics
```

**Handlers Used**: LLM (creative), SmolModel, Tool, Human (approval), WebSearch
**BFS/DFS Strategy**: BFS for parallel content streams, iteration within each
**Convergence**: Timeline-driven (3 weeks), quality gates at each stage
**Success Criteria**: All content created, approved, and scheduled by launch date

---

## Comparison Matrix: When to Use BFS vs DFS

| Scenario | Strategy | Reason |
|----------|----------|--------|
| **Unknown problem space** | BFS first | Explore multiple hypotheses in parallel |
| **Limited time/budget** | BFS with cutoff | Get broad coverage, accept less depth |
| **High confidence in direction** | DFS | Go deep quickly on known path |
| **Debugging/diagnosis** | BFS → DFS | Triage broadly, then follow strongest lead |
| **Research/discovery** | Hybrid | BFS for literature, DFS on key topics |
| **Parallel independent tasks** | BFS | Maximize throughput with parallelism |
| **Sequential dependencies** | DFS | Must complete one task before next |
| **Resource-constrained** | DFS | Focus limited resources on highest ROI path |

---

## Handler Selection Guidelines

| Task Type | Recommended Handler | Rationale |
|-----------|-------------------|-----------|
| **Simple classification** | SmolModel | Fast, cheap, good enough |
| **Complex reasoning** | LLM | High accuracy, nuanced understanding |
| **Factual lookup** | WebSearch + SmolModel | Real-time data, model for filtering |
| **Code execution** | Tool | Deterministic, reliable, fast |
| **High-stakes decision** | Human | Judgment, accountability, context |
| **Creative synthesis** | LLM | Generates novel connections |
| **Repetitive analysis** | SmolModel | Cost-efficient at scale |
| **Expert knowledge** | Human + LLM | Combine domain expertise with AI assistance |

---

## Success Metrics for Testing

### Quantitative
- **Task completion rate**: % of tasks successfully completed
- **Time to resolution**: Average time from start to convergence
- **Cost efficiency**: Total cost (API calls + human time) vs baseline
- **Parallelism factor**: Average number of concurrent tasks
- **Escalation rate**: % of tasks requiring human intervention

### Qualitative
- **Output quality**: Human evaluation of final artifacts
- **Appropriate handler selection**: Did system choose right tools?
- **Convergence effectiveness**: Clean termination vs timeouts
- **Error handling**: Graceful degradation when handlers fail

### System Behavior
- **Loop prevention**: Did loop detector catch cycles?
- **Context sharing**: Did agents build on each other's work?
- **Resource management**: Stayed within token/time/memory budgets?
- **Human integration**: Smooth handoffs, clear escalation paths?

---

## Recommended Testing Order

1. **Start Simple**: Use Case 6 (Support Tickets) - Well-defined, clear success criteria
2. **Add Complexity**: Use Case 2 (Competitive Analysis) - More ambiguous, requires synthesis
3. **Test Depth**: Use Case 3 (Bug Investigation) - Deep DFS, backtracking, hypothesis testing
4. **Test Breadth**: Use Case 4 (Research Report) - Wide BFS, large information space
5. **Full System**: Use Case 1 (Due Diligence) - All handlers, high stakes, complex convergence
6. **Long-Running**: Use Case 5 (Infrastructure Migration) - Multi-week, milestone-based
7. **High-Volume**: Use Case 6 at scale (100+ tickets/hour) - Stress test, efficiency

---

## Key Insights from Real-World Testing

Based on industry experience (OpenAI, Cursor, Claude Code), expect:

1. **80/20 Rule**: 80% of value from first 20% of exploration (favor BFS early)
2. **Human Bottleneck**: Human handlers will be slowest - design async patterns
3. **Context Explosion**: Aggressive context pruning needed for long sessions
4. **Tool Reliability**: Tools fail often - retry logic and graceful degradation critical
5. **Convergence is Hard**: Natural stopping points rare - need multiple termination criteria
6. **Cost Optimization**: Small models for 70% of tasks, big models for complex 30%
7. **Loop Detection**: Will catch many issues - invest in good loop detector

---

## Implementation Priorities

1. **Phase 1**: LLM + SmolModel + Tool handlers, basic BFS/DFS
2. **Phase 2**: WebSearch handler, convergence manager
3. **Phase 3**: Human handler with timeout/escalation
4. **Phase 4**: Loop detection, context sharing
5. **Phase 5**: Advanced orchestration (hierarchical, hybrid strategies)

Start with **Use Case 6 (Support Tickets)** as proof of concept. It's bounded, testable, and demonstrates clear ROI.

