# Memory Agent Evolution - Project Integration Guide

This document explains how to integrate the **Memory Agent Evolution** skill across your entire project.

## Quick Setup

### 1. Verify Skill Installation

Check that the skill is in the correct location:

```bash
ls -la .github/skills/memory-agent-evolution/
# Should show:
# - SKILL.md (main specification)
# - scripts/init_memory_system.py
# - scripts/load_memory.py
# - references/
# - assets/
```

### 2. Initialize Global Memory System

```bash
# From project root
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py --path ./memory

# This creates:
ls -la memory/
# - store.md (complete memory storage)
# - reflect.md (reflection and telemetry)
```

### 3. Add to `.gitignore` (Optional)

If you want to exclude memory from version control:

```bash
echo "memory/" >> .gitignore
```

Or, to track memory evolution:

```bash
# Don't ignore - let memory grow over time
# This tracks how the agent learns
```

---

## Applying Across Your Project

### For: AI Agent / Copilot

```python
# your_agent.py
import sys
sys.path.insert(0, '.github/skills/memory-agent-evolution/scripts')

from load_memory import MemoryLoader

class MyAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def process(self, task):
        # 1. Observe
        # 2. Retrieve with gate
        mode = "full" if self.memory.is_high_priority(task) else "lite"
        store = self.memory.load_store(mode=mode)
        reflect = self.memory.load_reflect(mode=mode)
        
        # 3. Act (your logic)
        result = self.generate_result(task, store, reflect)
        
        # 4-7. Evaluate, Reflect, Consolidate, Evolve
        self.memory.update_run(task, result)
        
        return result
```

### For: Multi-Agent System

Each agent gets its own memory directory:

```
agents/
  agent-1/
    memory/
      store.md
      reflect.md
  agent-2/
    memory/
      store.md
      reflect.md
```

```python
from load_memory import MemoryLoader

agent_1_memory = MemoryLoader("agents/agent-1/memory")
agent_2_memory = MemoryLoader("agents/agent-2/memory")
```

### For: Research Experiments

Track experimental runs and learning progress:

```python
# experiments/run_experiment.py
import sys
sys.path.insert(0, '../.github/skills/memory-agent-evolution/scripts')

from load_memory import MemoryLoader
import json
from datetime import datetime

class ExperimentTracker:
    def __init__(self, exp_name):
        self.memory = MemoryLoader(f"experiments/{exp_name}/memory")
    
    def log_trial(self, trial_id, config, result):
        # This automatically goes into memory/reflect.md
        self.memory.log_run(
            run_id=trial_id,
            outcome="success" if result.success else "fail",
            metadata={"config": config, "result": result}
        )
    
    def get_best_config(self):
        reflect = self.memory.load_reflect(mode="full")
        # Analyze all trials and return best
```

---

## Configuration Reference

### Gate Conditions

In your code, customize when to escalate from Lite-Mode to Full-Mode:

```python
def should_use_full_mode(task, context, memory):
    """Decide between Lite-Mode and Full-Mode."""
    
    # Check multiple conditions
    conditions = []
    
    # Condition 1: Priority
    if task.priority == "HIGH":
        conditions.append(("priority", True))
    
    # Condition 2: Recent errors
    recent_errors = memory.get_gate_signals()
    if recent_errors["repeated_error_count"] >= 2:
        conditions.append(("errors", True))
    
    # Condition 3: Complex task
    if len(context) > 10000:  # Large context
        conditions.append(("complexity", True))
    
    # Condition 4: Debug mode
    if task.debug:
        conditions.append(("debug", True))
    
    # Decision: Use Full if any condition is true
    use_full = any(c[1] for c in conditions)
    
    # Log decision reason
    reason = ", ".join(c[0] for c in conditions if c[1]) or "routine"
    print(f"Gate decision: {'FULL' if use_full else 'LITE'} ({reason})")
    
    return use_full
```

### Retrieval Scoring

Customize how candidates are ranked:

```python
def score_candidate(candidate, task, store, reflect):
    """Score a memory candidate for relevance."""
    
    # Base score
    score = 0.5
    
    # Relevance boost
    if candidate.matches_task_type(task):
        score += 0.2
    
    # Confidence bonus
    score += candidate.confidence * 0.15
    
    # Recency bonus (give boost to newer items)
    days_old = (now - candidate.created_at).days
    recency_bonus = max(0, 1 - days_old/365)  # Decay over 1 year
    score += recency_bonus * 0.1
    
    # Success rate bonus
    if hasattr(candidate, 'success_rate'):
        score += candidate.success_rate * 0.05
    
    return min(1.0, score)
```

### Skill Usage Tracking

Monitor which skills you rely on:

```python
# This is automatic in reflect.md, but you can customize:

from collections import Counter

class SkillTracker:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.calls = []
    
    def track_skill(self, skill_name):
        """Record a skill invocation."""
        self.calls.append(skill_name)
        if len(self.calls) > self.window_size:
            self.calls.pop(0)
    
    def get_specialization(self):
        """Calculate concentration metrics."""
        if not self.calls:
            return {"over_specialized": False, "hhi": 0, "top_ratio": 0}
        
        counter = Counter(self.calls)
        total = len(self.calls)
        
        top_skill_ratio = max(counter.values()) / total
        hhi = sum((count/total)**2 for count in counter.values())
        
        return {
            "over_specialized": top_skill_ratio > 0.65 or hhi > 0.45,
            "hhi": round(hhi, 2),
            "top_ratio": round(top_skill_ratio, 2),
            "unique_skills": len(counter)
        }
```

---

## Monitoring & Debugging

### Check Memory Status

```bash
# See current memory state
python -c "
from scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory')

# Lite mode summary
print('=== LITE MODE ===')
store = loader.load_store(mode='lite')
print(f'L1 facts: {len(store.get(\"L1\", []))}')
print(f'L2 procedures: {len(store.get(\"L2\", []))}')

# Full mode for analysis
print('\n=== FULL MODE ===')
store_full = loader.load_store(mode='full')
print(f'L0 events: {len(store_full.get(\"L0\", []))}')
print(f'L3 insights: {len(store_full.get(\"L3\", []))}')

# Reflect data
reflect = loader.load_reflect(mode='full')
print(f'\nTotal runs: {len(reflect.get(\"run_evaluation\", []))}')
print(f'Specialization: {loader.is_over_specialized()}')
"
```

### Tail Recent Events

```bash
# See latest events in memory
python -c "
from scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory')

store = loader.load_store(mode='full')
events = store.get('L0', [])[-5:]

for evt in events:
    print(f'[{evt.data[\"id\"]}] {evt.data[\"time\"]} - {evt.data[\"content\"][:60]}...')
"
```

### Analyze Performance

```python
# analyze_memory.py
from scripts.load_memory import MemoryLoader

def analyze():
    loader = MemoryLoader('memory')
    reflect = loader.load_reflect(mode='full')
    
    runs = reflect.get('run_evaluation', [])
    
    total = len(runs)
    success = sum(1 for r in runs if r.data['outcome'] == 'success')
    full_mode = sum(1 for r in runs if r.data['route_mode'] == 'full')
    
    print(f"Total runs: {total}")
    print(f"Success rate: {success/total*100:.1f}%")
    print(f"Full-Mode usage: {full_mode/total*100:.1f}%")
    
    # Error breakdown
    errors = {}
    for r in runs:
        et = r.data.get('error_type', 'none')
        errors[et] = errors.get(et, 0) + 1
    
    print("\nError breakdown:")
    for error, count in sorted(errors.items(), key=lambda x: -x[1]):
        print(f"  {error}: {count} ({count/total*100:.1f}%)")
```

---

## Best Practices

### 1. **Write Frequently, Read Selectively**

```python
# ✓ GOOD: Write complete memory often
def consolidate_memory():
    complete_store = build_full_store()
    write_to_file(complete_store, "memory/store.md")

# ✗ BAD: Read everything every time
def get_context():
    return load_store(mode="full")  # Only when needed!
```

### 2. **Use Lite Mode by Default**

```python
# ✓ GOOD
mode = "lite"
if is_high_priority:
    mode = "full"

# ✗ BAD
mode = "full"  # Always using Full-Mode defeats the purpose
```

### 3. **Clean Up Old Events**

```python
# Implement monthly cleanup
def archive_old_events():
    from datetime import datetime, timedelta
    store = load_store(mode="full")
    
    cutoff = datetime.now() - timedelta(days=30)
    
    old_events = [e for e in store.get("L0", [])
                  if datetime.fromisoformat(e.data['time']) < cutoff]
    
    # Archive to separate file
    # Delete from store.md
```

### 4. **Version Procedures**

```python
# When procedure improves, create new version
procedure_v2 = procedure_v1.copy()
procedure_v2['version'] = 2
procedure_v2['success_rate'] = 0.85  # From data
procedure_v2['created_at'] = now()

# Mark old as superseded
procedure_v1['status'] = 'superseded'
```

### 5. **Regular Evolution Cycles**

```python
# Every 50 runs, do a full evolution
if run_count % 50 == 0:
    # Analyze errors
    # Update procedures
    # Recalibrate gate thresholds
    # Create learning agenda items
    evolve_memory()
```

---

## Integration Patterns

### Pattern 1: Simple Agent

```python
class SimpleAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def ask(self, question):
        store = self.memory.load_store(mode="lite")
        answer = generate_answer(question, store)
        self.memory.log_run("ask", "success", answer)
        return answer
```

### Pattern 2: Learning Agent

```python
class LearningAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
        self.run_count = 0
    
    def execute_task(self, task):
        # Gate: decide mode
        mode = "full" if self.run_count % 10 == 0 else "lite"
        
        # Retrieve
        store = self.memory.load_store(mode=mode)
        
        # Execute
        result = execute(task, store)
        
        # Consolidate
        self.memory.log_run(task.id, result.status, result)
        
        # Evolve every 50 runs
        if self.run_count % 50 == 0:
            self.evolve()
        
        self.run_count += 1
        return result
    
    def evolve(self):
        """Update memory policies based on performance."""
        reflect = self.memory.load_reflect(mode="full")
        # Analyze and update procedures, facts, etc.
```

### Pattern 3: Multi-Agent Coordination

```python
class MultiAgentSystem:
    def __init__(self):
        self.agents = {
            'planner': Agent('memory/planner'),
            'executor': Agent('memory/executor'),
            'reviewer': Agent('memory/reviewer')
        }
    
    def execute_plan(self, goal):
        # Planner
        plan = self.agents['planner'].create_plan(goal)
        
        # Executor
        result = self.agents['executor'].execute(plan)
        
        # Reviewer
        feedback = self.agents['reviewer'].review(result)
        
        # Share learnings
        for agent in self.agents.values():
            agent.memory.update_shared_facts(feedback)
```

---

## Next Steps

1. ✓ Run: `python scripts/init_memory_system.py --path ./memory`
2. ✓ Integrate: Import `MemoryLoader` in your agent code
3. ✓ Configure: Set custom gate conditions and retrieval scoring
4. ✓ Monitor: Check `memory/store.md` and `memory/reflect.md` for activity
5. ✓ Evolve: Every 50 runs, analyze and improve procedures
6. ? Deploy: Set up archiving and cleanup for production systems

---

## Troubleshooting

**Q: Memory system not initialized?**
→ Run `python scripts/init_memory_system.py --path ./memory`

**Q: Gate always choosing Full-Mode?**
→ Check gate conditions in your code
→ Verify `repeated_error_count` is being set

**Q: Memory growing too large?**
→ Implement L0 event archiving (monthly)
→ Use Lite-Mode more aggressively

**Q: Skills over-specialized?**
→ Check `is_over_specialized()` flag in reflect.md
→ Inject non-top-skill candidates in retrieval
→ Increase `DiversityBonus` weight

---

## Support

- **SKILL.md**: Full architectural specification
- **references/integration-guide.md**: Detailed integration patterns
- **references/four-layer-memory-detail.md**: Deep dive into memory layers
- **scripts/load_memory.py**: Python API documentation

See `.github/skills/memory-agent-evolution/` for all resources.
