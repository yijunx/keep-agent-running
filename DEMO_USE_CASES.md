# Demo-Grade Use Cases

Simple, runnable examples to demonstrate BFS/DFS problem solving.

---

## Demo 1: Recipe Finder (5 minutes)

**Goal**: Find a recipe based on ingredients you have at home.

**Why it's simple**:
- Clear input (ingredients list)
- Clear output (recipe with instructions)
- No external dependencies needed
- Easy to understand BFS → DFS flow

### Task Flow

```
Input: "I have chicken, rice, and soy sauce"

[BFS] Find possible recipes (parallel search)
├── [SmolModel] Classify cuisine type → Asian
├── [SmolModel] Find 5 matching recipes
└── [SmolModel] Rate each recipe (1-10)

[DFS] Get details for top recipe
├── [LLM] Generate full recipe with steps
├── [LLM] Suggest ingredient substitutions
└── [LLM] Estimate cooking time and difficulty

Output: Complete recipe with steps
```

**Handlers**: SmolModel (2-3 calls), LLM (1-2 calls)
**Time**: 30 seconds
**Cost**: $0.01

---

## Demo 2: Email Triage (3 minutes)

**Goal**: Automatically sort and prioritize incoming emails.

**Why it's simple**:
- Easy to mock email data
- Binary decisions (urgent/not urgent)
- Demonstrates parallel processing (BFS)
- No tools needed, just LLM/SmolModel

### Task Flow

```
Input: 10 emails in inbox

[BFS] Classify all emails (parallel)
├── Email 1 → [SmolModel] → "Work / High Priority"
├── Email 2 → [SmolModel] → "Spam / Low Priority"
├── Email 3 → [SmolModel] → "Personal / Medium Priority"
... (all 10 in parallel)

[DFS] Handle high-priority emails only
├── Email 1 (urgent):
│   ├── [SmolModel] Extract action items
│   ├── [LLM] Draft response
│   └── [LLM] Set follow-up reminder

Output: Sorted emails + drafted responses for urgent ones
```

**Handlers**: SmolModel (10 calls), LLM (2-3 calls)
**Time**: 20 seconds
**Cost**: $0.02

---

## Demo 3: Trip Planner (7 minutes)

**Goal**: Plan a weekend trip given a destination.

**Why it's simple**:
- Fun, relatable problem
- Shows BFS (explore options) → DFS (finalize plan)
- Can use mock data, no real APIs needed
- Clear structure

### Task Flow

```
Input: "Plan a weekend trip to Tokyo"

[BFS] Explore options (parallel)
├── [SmolModel] Top 10 attractions
├── [SmolModel] 5 restaurant recommendations  
├── [SmolModel] 3 hotel options
└── [SmolModel] Transportation options

[DFS] Build detailed itinerary
├── Day 1:
│   ├── [LLM] Morning: Visit temple (with details)
│   ├── [LLM] Lunch: Restaurant A (with booking info)
│   └── [LLM] Afternoon: Shopping district
├── Day 2:
│   └── [LLM] Similar breakdown

Output: 2-day itinerary with times, locations, tips
```

**Handlers**: SmolModel (4 calls), LLM (6-8 calls)
**Time**: 45 seconds
**Cost**: $0.03

---

## Demo 4: Code Review Helper (5 minutes)

**Goal**: Review a code snippet and suggest improvements.

**Why it's simple**:
- Developers understand it immediately
- Single input (code snippet)
- Multiple analysis dimensions (BFS)
- No external tools needed

### Task Flow

```
Input: Python function (50 lines)

[BFS] Analyze different aspects (parallel)
├── [SmolModel] Check code style (PEP8)
├── [SmolModel] Find potential bugs
├── [SmolModel] Calculate complexity metrics
└── [SmolModel] Check for security issues

[DFS] Fix the most critical issue
├── Most critical: SQL injection vulnerability
│   ├── [LLM] Explain the vulnerability
│   ├── [LLM] Show secure code example
│   └── [LLM] Suggest testing approach

Output: Review summary + detailed fix for top issue
```

**Handlers**: SmolModel (4 calls), LLM (3 calls)
**Time**: 25 seconds
**Cost**: $0.02

---

## Demo 5: Meeting Notes Summarizer (4 minutes)

**Goal**: Take messy meeting notes and create structured summary.

**Why it's simple**:
- Very practical (everyone has meeting notes)
- Input/output very clear
- Shows information extraction + synthesis
- No external dependencies

### Task Flow

```
Input: Raw meeting transcript (2000 words)

[BFS] Extract information (parallel)
├── [SmolModel] Extract action items
├── [SmolModel] Extract decisions made
├── [SmolModel] Extract attendees and roles
└── [SmolModel] Identify topics discussed

[DFS] Create structured output
├── [LLM] Write executive summary (3 sentences)
├── [LLM] Format action items with owners
└── [LLM] Create follow-up email draft

Output: Structured notes + follow-up email
```

**Handlers**: SmolModel (4 calls), LLM (3 calls)
**Time**: 30 seconds
**Cost**: $0.02

---

## Demo 6: Product Description Generator (3 minutes)

**Goal**: Generate marketing copy for a product.

**Why it's simple**:
- Single product as input
- Multiple content formats (BFS for parallel generation)
- Fun to show different styles
- Pure LLM work, easy to demo

### Task Flow

```
Input: "Wireless earbuds with noise cancellation"

[BFS] Generate different formats (parallel)
├── [SmolModel] Short description (50 words)
├── [LLM] Long description (200 words)
├── [LLM] Social media post (Twitter-style)
├── [LLM] Email marketing copy
└── [SmolModel] Bullet points (key features)

[DFS] Optimize the best-performing format
├── Long description (most engaging)
│   ├── [LLM] A/B test two variants
│   ├── [SmolModel] Score each for engagement
│   └── [LLM] Finalize winner

Output: 5 formats + optimized long description
```

**Handlers**: SmolModel (3 calls), LLM (6 calls)
**Time**: 35 seconds
**Cost**: $0.03

---

## Demo 7: Math Tutor - GOAL-DRIVEN Decomposition ⭐

**Goal**: Solve for x (SAME GOAL, DIFFERENT PATHS)

**Why this demonstrates goal-driven BFS/DFS**:
- **Same goal**: "Solve for x"
- **Different context**: Problem complexity determines decomposition
- **Adaptive strategy**: System chooses different paths automatically
- Like losing weight: 200kg→120kg needs different plan than 130kg→120kg

### Example A: Simple Problem (2 steps)

```
Input: "Solve: 2x + 5 = 15"
Context: Linear equation, beginner level

[BFS] Analyze
└── [SmolModel] → "Simple linear, 2 steps needed"

[DFS] Solution (SHORT path - only 2 steps)
├── Step 1: Subtract 5 → "2x = 10"
└── Step 2: Divide by 2 → "x = 5"

Time: 20 seconds
Steps: 2
```

### Example B: Medium Problem (6 steps)

```
Input: "Solve: x² - 5x + 6 = 0"
Context: Quadratic equation, intermediate level

[BFS] Analyze
└── [SmolModel] → "Quadratic, needs factoring, 6 steps"

[DFS] Solution (LONGER path - 6 steps)
├── Step 1: Identify a, b, c coefficients
├── Step 2: Check if factorable
├── Step 3: Find factors of 6 that sum to -5
├── Step 4: Write as (x-2)(x-3) = 0
├── Step 5: Solve x-2=0 → x=2
└── Step 6: Solve x-3=0 → x=3

Time: 45 seconds
Steps: 6
```

### Example C: Complex Word Problem (10+ steps)

```
Input: "A train travels 120km in 2 hours. If it increases speed by 20km/h, 
how long to travel 180km? Solve for t."
Context: Word problem, requires translation to equation first

[BFS] Analyze
└── [SmolModel] → "Word problem, need to translate, 10+ steps"

[DFS] Solution (MUCH LONGER path - 10+ steps)
├── Step 1: Identify what we're solving for (time t)
├── Step 2: Find current speed (120/2 = 60 km/h)
├── Step 3: Calculate new speed (60+20 = 80 km/h)
├── Step 4: Recall formula: distance = speed × time
├── Step 5: Set up equation: 180 = 80 × t
├── Step 6: Rearrange: t = 180/80
├── Step 7: Simplify: t = 9/4
├── Step 8: Convert to mixed number: t = 2.25 hours
├── Step 9: Convert to hours and minutes: 2h 15min
└── Step 10: Verify answer makes sense

Time: 90 seconds
Steps: 10+
```

### Key Insight: SAME GOAL, DIFFERENT DECOMPOSITION

```
GOAL: "Solve for x"

Context A (2x + 5 = 15):
  → System generates 2-step plan
  → Uses basic algebra only
  → Fast execution

Context B (x² - 5x + 6 = 0):
  → System generates 6-step plan  
  → Needs factoring technique
  → Medium execution

Context C (Word problem):
  → System generates 10+ step plan
  → Must translate to equation FIRST
  → Longer execution

The orchestrator ADAPTS the task breakdown based on starting context!
Just like: 200kg→120kg needs surgery + diet, but 130kg→120kg just needs diet.
```

**Handlers**: SmolModel (analysis), LLM (adaptive solution)
**Time**: 20-90 seconds (depends on problem)
**Cost**: $0.01-0.05 (scales with complexity)

---

## Demo 8: Shopping List Organizer (2 minutes)

**Goal**: Take random list of items and organize by store section.

**Why it's simple**:
- Super simple input (list of items)
- Fast classification task
- Shows BFS parallel processing
- Instant gratification

### Task Flow

```
Input: ["milk", "bread", "shampoo", "apples", "chicken", "batteries"]

[BFS] Classify all items (parallel)
├── milk → [SmolModel] → Dairy
├── bread → [SmolModel] → Bakery
├── shampoo → [SmolModel] → Personal Care
├── apples → [SmolModel] → Produce
├── chicken → [SmolModel] → Meat
└── batteries → [SmolModel] → Electronics

[Optional DFS] Add suggestions
├── Dairy section → [SmolModel] → Suggest: eggs, cheese
└── Produce section → [SmolModel] → Suggest: bananas, lettuce

Output: Organized list by section + suggestions
```

**Handlers**: SmolModel (6-8 calls)
**Time**: 10 seconds
**Cost**: $0.005

---

## Comparison: Demo vs Production Use Cases

| Aspect | Demo Cases | Production Cases |
|--------|-----------|------------------|
| **Time to run** | 10s - 1min | Minutes to hours |
| **Handler calls** | 5-10 | 50-500 |
| **Cost** | $0.01-0.03 | $1-100 |
| **Setup needed** | None (mock data) | Real APIs, databases |
| **Audience** | Demos, learning | Real users, business value |
| **Success metric** | "It works!" | ROI, accuracy, speed |

---

## Implementation Priority

### Start Here (Simplest)
1. **Shopping List** - Pure classification, 10 seconds
2. **Email Triage** - Binary decisions, very fast
3. **Math Tutor** - Step-by-step DFS, easy to validate

### Next (Still Simple)
4. **Meeting Notes** - Practical, shows extraction + synthesis
5. **Recipe Finder** - Fun, shows BFS → DFS clearly
6. **Code Review** - Developers love it

### Show-Off Demos
7. **Trip Planner** - Impressive output, lots of details
8. **Product Descriptions** - Shows creativity, multiple formats

---

## Quick Start Guide

### 1. Pick a Demo (Start with Shopping List)
```python
items = ["milk", "bread", "shampoo", "apples"]
# Takes 10 seconds, costs $0.005
```

### 2. Run It
```bash
python examples/shopping_list_demo.py
```

### 3. Show the Output
```
📦 ORGANIZED SHOPPING LIST
==========================
Dairy:
  - milk
  
Bakery:
  - bread
  
Personal Care:
  - shampoo
  
Produce:
  - apples
  
💡 Suggestions:
  Dairy: eggs, cheese
  Produce: bananas
```

### 4. Explain the Value
"The system used BFS to classify all items in parallel (10 seconds instead of 40), then optionally went deeper to add suggestions."

---

## Testing Checklist

For each demo, verify:
- [ ] Runs in <1 minute
- [ ] Costs <$0.05
- [ ] No external dependencies needed
- [ ] Output is clearly useful
- [ ] BFS/DFS strategy is obvious
- [ ] Works with mock data

---

## Next Steps

1. **Implement Shopping List demo** (easiest)
2. **Add Math Tutor demo** (shows DFS clearly)
3. **Build Email Triage demo** (practical)
4. Use these to validate your system works
5. Then scale up to production use cases

The demos prove the concept. The production use cases (from USE_CASES.md) show the business value.

