# Demo Examples

Simple, runnable examples to test the BFS/DFS system.

## Quick Demos (Start Here!)

### 1. 🛒 Shopping List Organizer
**File**: `shopping_list_demo.py`  
**Time**: 10 seconds  
**Cost**: $0.005  

Takes random grocery items, organizes by store section.

```bash
python examples/shopping_list_demo.py
```

**What it demonstrates**:
- ✅ BFS parallel classification (all items at once)
- ✅ Small model for efficiency
- ✅ Simple input → useful output

---

### 2. 📧 Email Triage
**File**: `email_triage_demo.py`  
**Time**: 20 seconds  
**Cost**: $0.01  

Sorts 5 emails by priority, extracts action items.

```bash
python examples/email_triage_demo.py
```

**What it demonstrates**:
- ✅ BFS parallel processing (5x faster than sequential)
- ✅ Smart resource allocation (only analyze urgent emails)
- ✅ Practical use case

---

### 3. 📐 Math Tutor
**File**: `math_tutor_demo.py`  
**Time**: 30 seconds  
**Cost**: $0.02  

Solves algebra problem step-by-step with explanations.

```bash
python examples/math_tutor_demo.py
```

**What it demonstrates**:
- ✅ DFS depth-first breakdown
- ✅ Sequential dependencies (analyze → solve → validate)
- ✅ Educational value

---

## Production Example

### 🎫 Customer Support Tickets
**File**: `support_ticket_example.py`  
**Time**: 2-3 minutes  
**Cost**: $0.05-0.10  

Full-featured support ticket resolution with all handler types.

```bash
python examples/support_ticket_example.py
```

**What it demonstrates**:
- ✅ All 5 handler types (LLM, SmolModel, Tool, WebSearch, Human)
- ✅ BFS triage → DFS investigation
- ✅ Real-world complexity
- ✅ Human escalation

---

## Comparison

| Demo | Time | Cost | Complexity | Best For |
|------|------|------|------------|----------|
| **Shopping List** | 10s | $0.005 | ⭐ | First demo |
| **Email Triage** | 20s | $0.01 | ⭐⭐ | BFS showcase |
| **Math Tutor** | 30s | $0.02 | ⭐⭐ | DFS showcase |
| **Support Tickets** | 2-3min | $0.05 | ⭐⭐⭐⭐ | Full system |

---

## Running the Demos

### Prerequisites
```bash
# Make sure your vLLM server is running
# Default: http://10.4.33.17:80/v1
```

### Run a Demo
```bash
# From project root
cd /Users/xuyijun/projects/keep-agent-running
python examples/shopping_list_demo.py
```

### Expected Output
Each demo prints:
1. **Input** - What problem we're solving
2. **Progress** - What the system is doing (streamed)
3. **Output** - Final result, nicely formatted

---

## What Happens Behind the Scenes

### Shopping List (BFS)
```
Input: 10 items
  ↓
Orchestrator: Break into 10 classification tasks
  ↓
BFS: Process all 10 in parallel
  ↓
Output: Organized by section
```

### Math Tutor (DFS)
```
Input: Math problem
  ↓
Analyze: Identify problem type
  ↓ (go deeper)
Solve: Generate step-by-step solution
  ↓ (go deeper)
Validate: Check each step
  ↓
Output: Step-by-step solution
```

### Email Triage (Hybrid BFS→DFS)
```
Input: 5 emails
  ↓
BFS: Classify all 5 in parallel
  ↓
Filter: Keep only urgent/high priority
  ↓
DFS: Extract actions from urgent ones
  ↓
Output: Prioritized list with actions
```

---

## Troubleshooting

### "Connection refused" error
- Check if vLLM server is running
- Verify base_url in demo files matches your server

### "Model not found" error
- Update model_name in demo to match your available models
- Check your vLLM server's model list

### Demo runs but no output
- Check if PydanticConverter is working
- Verify LLM is returning valid JSON

### Slow performance
- First run downloads models (can take time)
- Subsequent runs should be faster
- Try smaller models for demos

---

## Next Steps

1. ✅ Run all 3 quick demos
2. ✅ Understand BFS vs DFS tradeoffs
3. ✅ Try modifying inputs (your own data)
4. 📖 Read [DEMO_USE_CASES.md](../DEMO_USE_CASES.md) for 5 more ideas
5. 🚀 Scale up to [USE_CASES.md](../USE_CASES.md) for production scenarios

---

## Contributing

Have a simple demo idea? Add it!

Requirements for a good demo:
- ✅ Runs in <1 minute
- ✅ Costs <$0.05
- ✅ No external dependencies
- ✅ Clear BFS or DFS pattern
- ✅ Obviously useful output

See `shopping_list_demo.py` as template.

