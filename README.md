# Memory Agent Evolution Skill - Production Ready

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2026-04-25

---

## 📚 What This Skill Provides

A **complete, lightweight memory architecture** for AI agents that learn and evolve.

### Core Features

- **Four Memory Layers** (L0-L3): Events, Semantics, Procedures, Metacognition
- **Dual-Mode Retrieval**: Lite-Mode for routine (fast) + Full-Mode for escalation (deep)
- **Temporal Knowledge Graph**: Links across time and memory layers
- **Automatic Skill Tracking**: Detects over-specialization automatically
- **Markdown-Native**: No databases required, version-controllable storage
- **Complete Specification**: Architecture blueprint + integration code + templates

---

## 📁 Project Structure

```
memorymeinskill/
├── .github/skills/memory-agent-evolution/
│   ├── SKILL.md                          ← Start here (900 lines, complete spec)
│   ├── memory/                           ← Runtime storage
│   │   ├── store.md                      ← Full memory (L0-L3)
│   │   └── reflect.md                    ← Reflection & telemetry
│   ├── scripts/
│   │   ├── init_memory_system.py         ← Setup new memory (Python)
│   │   └── load_memory.py                ← Read/parse memory (Python API)
│   ├── references/
│   │   ├── integration-guide.md          ← How to integrate (with examples)
│   │   ├── four-layer-memory-detail.md   ← Layer semantics (deep dive)
│   │   └── examples.md                   ← Real integration examples
│   └── assets/
│       ├── store-template.md             ← Template for store.md
│       └── reflect-template.md           ← Template for reflect.md
│
├── MEMORY_INTEGRATION_GUIDE.md           ← Global setup & configuration
├── README.md                             ← This file
└── SKILL_CHECKLIST.md                    ← Launch checklist
```

---

## 🚀 Quick Start (5 minutes)

### 1. Initialize Memory System

```bash
cd /path/to/your/project
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py --path ./memory

# ✓ Creates memory/store.md and memory/reflect.md
```

### 2. Load Memory in Your Code

```python
import sys
sys.path.insert(0, '.github/skills/memory-agent-evolution/scripts')
from load_memory import MemoryLoader

loader = MemoryLoader("memory")

# Get memory (Lite-Mode: fast, routine tasks)
store = loader.load_store(mode="lite")
reflect = loader.load_reflect(mode="lite")

# Your logic here...

# Save results
loader.log_run(run_id="task-001", outcome="success")
```

### 3. Run the 7-Step Loop

```python
def agent_turn(task):
    # 1. Observe
    # 2. Retrieve (with gate)
    if high_priority(task):
        mode = "full"
    else:
        mode = "lite"
    
    store = loader.load_store(mode=mode)
    reflect = loader.load_reflect(mode=mode)
    
    # 3. Act/Reason
    result = generate(task, store, reflect)
    
    # 4-7. Evaluate, Reflect, Consolidate, Evolve
    outcome = evaluate(result)
    loader.log_run(task.id, outcome)
    
    return result
```

See `MEMORY_INTEGRATION_GUIDE.md` for detailed examples.

---

## 📖 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **SKILL.md** | Complete architectural specification | 20-30 min |
| **MEMORY_INTEGRATION_GUIDE.md** | Global integration & configuration | 10-15 min |
| **references/integration-guide.md** | Step-by-step integration with patterns | 15-20 min |
| **references/four-layer-memory-detail.md** | Deep dive into each memory layer | 20-25 min |
| **assets/store-template.md** | Template & best practices for store.md | 5-10 min |

**Recommended reading order:**
1. This README (5 min)
2. SKILL.md sections on Purpose & When to Use (5 min)
3. MEMORY_INTEGRATION_GUIDE.md Quick Start (5 min)
4. Try the integration pattern that matches your use case (15 min)
5. Deep dive as needed (optional)

---

## 🎯 Key Concepts

### Dual-Mode Retrieval

|  | **Lite-Mode** | **Full-Mode** |
|---|---|---|
| **Use Case** | Routine tasks, quick responses | Debugging, complex reasoning, high priority |
| **Reads** | L1 + L2 + Lite Snapshot | L0 + L1 + L2 + L3 (complete) |
| **Cost** | ~50-100ms | ~300-500ms |
| **When** | Default | task_priority=HIGH OR repeated_errors≥2 OR debug_mode |

### Memory Layers

- **L0 Events**: Raw data (dialogue turns, tool calls)
- **L1 Semantics**: Facts, preferences, constraints
- **L2 Procedures**: Reusable workflows, decision templates
- **L3 Metacognitive**: Self-evaluation, learning goals, calibration

### Gate Conditions (Escalate to Full-Mode when):

1. `task_priority == HIGH`
2. `repeated_error_count >= 2`
3. `needs_deep_trace == true`

### Skill Usage Tracking

Automatically detects over-specialization:

```
top_skill_ratio = max_calls / total_calls
hhi = sum((calls_i / total_calls)²)
over_specialized = (top_skill_ratio > 0.65) OR (hhi > 0.45)
```

---

## 💡 Use Cases

### ✅ Ideal For:
- Multi-turn Q&A with context learning
- Debugging agents that learn from failures
- Workflow optimization (remembering what works)
- Research tracking across experiments
- Multi-agent coordination (shared facts)
- Long-running copilots that improve over time

### ❌ Not Ideal For:
- Single-turn, stateless tasks
- Real-time systems with strict latency (<50ms required)
- Tasks with no opportunity to learn
- Systems that must forget (privacy-sensitive data)

---

## 🔧 Configuration

### Gate Conditions

Customize in your code:

```python
def should_use_full_mode(task):
    return (
        task.priority == "HIGH"
        or error_count >= 2
        or task.debug_mode
    )
```

### Retrieval Scoring

```python
score = (
    0.3 * relevance +
    0.2 * confidence +
    0.2 * recency +
    0.15 * success_rate +
    0.15 * diversity_bonus
)
```

### Skill Tracking

Automatically enabled. Disable if needed:

```python
# In reflect.md, set:
over_specialized: false  # System won't auto-escalate
decision: manual_tracking
```

See `MEMORY_INTEGRATION_GUIDE.md` for more configurations.

---

## 📊 Monitoring

### Check Memory Status

```bash
# See what's in memory
python -c "
from .github.skills.memory_agent_evolution.scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory')

store = loader.load_store(mode='lite')
print(f'L1 facts: {len(store.get(\"L1\", []))}')
print(f'L2 procedures: {len(store.get(\"L2\", []))}')

print(f'Over-specialized: {loader.is_over_specialized()}')
"
```

### Analyze Performance

```bash
# Get success rate and error breakdown
python -c "
from scripts.load_memory import MemoryLoader

loader = MemoryLoader('memory')
reflect = loader.load_reflect(mode='full')

runs = reflect.get('run_evaluation', [])
success_rate = sum(1 for r in runs if r.data['outcome'] == 'success') / len(runs)

print(f'Success rate: {success_rate * 100:.1f}%')
"
```

---

## 🎓 Integration Patterns

### Pattern 1: Simple Agent

```python
class Agent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def ask(self, question):
        store = self.memory.load_store(mode="lite")
        answer = self.generate(question, store)
        self.memory.log_run("ask", "success")
        return answer
```

### Pattern 2: Learning Agent

```python
class LearningAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def execute(self, task):
        mode = "full" if high_priority else "lite"
        store = self.memory.load_store(mode=mode)
        result = self.execute(task, store)
        self.memory.log_run(task.id, result.status)
        return result
```

### Pattern 3: Multi-Agent System

```python
# Each agent has its own memory
agents = {
    'planner': Agent('memory/planner'),
    'executor': Agent('memory/executor'),
}

# Share knowledge via unified facts layer
```

See `MEMORY_INTEGRATION_GUIDE.md` for 8 more patterns.

---

## 🧹 Maintenance

### Monthly Tasks

- [ ] Archive L0 events older than 30 days
- [ ] Review L2 procedures for obsolescence
- [ ] Check memory file size (should be <10MB for typical use)
- [ ] Analyze success rates and error patterns

### Quarterly Tasks

- [ ] Review L3 metacognitive insights
- [ ] Update gate conditions based on data
- [ ] Promote successful procedures to new versions
- [ ] Plan next quarter's learning agenda

### Annual Tasks

- [ ] Full system evaluation
- [ ] Consider moving to V2 (learned gating, more experts)
- [ ] Archive or delete very old events

---

## ⚡ Performance Characteristics

| Operation | Lite-Mode | Full-Mode |
|-----------|-----------|-----------|
| Load store.md | ~20ms | ~100ms |
| Load reflect.md | ~10ms | ~50ms |
| Total retrieval | ~50-100ms | ~300-500ms |
| Write (consolidation) | ~100-200ms | ~100-200ms |
| Skill tracking update | ~5ms | ~5ms |

**Typical memory sizes:**
- L0 (100 events): 50-100 KB
- L1 (50 facts): 20-50 KB
- L2 (20 procedures): 80-150 KB
- L3 (10 insights): 30-60 KB
- **Total: 180-360 KB** per full history

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Memory not created | Run: `python scripts/init_memory_system.py --path ./memory` |
| Gate not escalating | Check gate condition logic in your code |
| Memory too large | Archive L0 events monthly; implement TTL |
| Skills over-specialized | Enable DiversityBonus; inject non-top-skill candidates |
| Performance degrading | Check file size; implement cleanup; use Lite-Mode more |

See `MEMORY_INTEGRATION_GUIDE.md` for detailed troubleshooting.

---

## 📝 Version History

### v1.0.0 (2026-04-25)
- ✅ Complete four-layer architecture (L0-L3)
- ✅ Dual-mode retrieval (Lite/Full with rule-based gate)
- ✅ Temporal Knowledge Graph backbone
- ✅ Automatic skill usage tracking
- ✅ Markdown-native storage (no database)
- ✅ Production initialization scripts
- ✅ Complete documentation & templates
- ✅ Integration examples

### Roadmap: v1.1 (Q2 2026)
- Learned gate (replaces rule-based with ML model)
- Procedure versioning with rollback
- Cost-aware retrieval scoring
- Archive management utilities

### Roadmap: v2.0 (Q3-Q4 2026)
- Multi-expert system (>2 experts with weighted routing)
- Support for vector embeddings (optional)
- Graph visualization
- REST API for remote access

---

## 📄 License & Attribution

This skill is part of the **Claude Skills** ecosystem.

- Based on: 4-layer memory architecture + MoE routing patterns
- Storage: Markdown YAML (no external dependencies)
- Python dependencies: Only `PyYAML` (for parsing)

---

## 🤝 Contributing

Improvements welcome! Consider:

1. **Bug fixes**: File issues with memory/store.md edge cases
2. **Performance**: Optimize load_memory.py for large history
3. **Documentation**: Add integration examples for your domain
4. **Features**: Custom gate conditions, retrieval scoring strategies

---

## 📞 Quick Reference

**Files You'll Edit:**
- Your code: Import `MemoryLoader`, call `.load_store()` and `.load_reflect()`
- `memory/store.md`: Automatically updated (consolidation step)
- `memory/reflect.md`: Automatically updated (evaluation step)

**Files You Won't Touch:**
- `SKILL.md`: Reference only
- Scripts: Use but don't edit (unless customizing)
- Templates: For reference

**Key Commands:**

```bash
# Initialize
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py --path ./memory

# Check status
python -c "from scripts.load_memory import MemoryLoader; loader = MemoryLoader('memory'); print(loader.is_over_specialized())"

# Analyze
python .github/skills/memory-agent-evolution/scripts/load_memory.py  # Runs example analysis
```

---

## 🎉 Next Steps

1. **Initialize**: `python scripts/init_memory_system.py --path ./memory`
2. **Read**: Check `MEMORY_INTEGRATION_GUIDE.md` Quick Start (5 min)
3. **Integrate**: Pick a pattern from `references/integration-guide.md` (15 min)
4. **Test**: Run your agent with memory enabled
5. **Monitor**: Check `memory/store.md` and `memory/reflect.md` for activity
6. **Evolve**: Every 50 runs, analyze and improve

**Questions?** Start with:
- `SKILL.md` - "When to Use" section
- `MEMORY_INTEGRATION_GUIDE.md` - Quick Start or Troubleshooting
- `references/integration-guide.md` - Integration Patterns

---

**Ready to add memory to your agent? Let's go! 🚀**
