# Integration Guide: Memory Agent Evolution

This guide shows how to integrate the Memory Agent Evolution skill into your project.

## 1. Quick Start

### Step 1: Initialize the Memory System

```bash
cd /path/to/your/project
python /path/to/skill/scripts/init_memory_system.py --path ./memory
```

This creates:
- `memory/store.md` - Complete memory storage (all four layers)
- `memory/reflect.md` - Reflection and telemetry tracking

### Step 2: Import the Memory Loader

```python
from pathlib import Path
import sys

# Add skill scripts to path
sys.path.insert(0, '/path/to/skill/scripts')
from load_memory import MemoryLoader

# Initialize loader
loader = MemoryLoader("memory")
```

### Step 3: Implement the Runtime Loop

```python
def run_agent_turn(task: str, context: dict):
    """Execute one turn of the agent with memory management."""
    
    # 1. Observe
    print(f"Observing: {task}")
    
    # 2. Retrieve (with dual-mode gate)
    gate_signals = loader.get_gate_signals()
    mode = "full" if should_escalate(gate_signals) else "lite"
    
    store = loader.load_store(mode=mode)
    reflect = loader.load_reflect(mode=mode)
    
    # 3. Act/Reason
    response = generate_response(task, store, reflect)
    
    # 4-6. Evaluate, Reflect, Consolidate
    outcome = evaluate(response)
    update_memory(outcome, mode)
    
    return response


def should_escalate(gate_signals: dict) -> bool:
    """Determine if Full-Mode is needed."""
    return (
        gate_signals.get("task_priority") == "HIGH"
        or gate_signals.get("repeated_error_count", 0) >= 2
        or gate_signals.get("needs_deep_trace", False)
    )
```

## 2. Gate Condition Implementation

The dual-mode gate decides between Lite-Mode and Full-Mode reads:

### Lite-Mode (default)
- ✓ Best for: routine tasks, quick responses
- ✓ Reads: L1 + L2 + Lite Snapshot
- ✓ Cost: ~50-100ms
- ✓ Use when: task_priority != HIGH AND error_count < 2 AND !needs_deep_trace

### Full-Mode (escalation)
- ✓ Best for: debugging, learning, complex reasoning
- ✓ Reads: All L0-L3 layers, full history
- ✓ Cost: ~300-500ms
- ✓ Use when: Any gate condition is true

### Example: Custom Gate

```python
def evaluate_gate(task: str, history: List[dict]) -> str:
    """Custom gate logic."""
    
    # Count recent errors
    error_count = sum(1 for h in history[-5:] if h.get("outcome") == "fail")
    
    # Priority from task
    priority = task.get("priority", "ROUTINE")
    
    # Check for deep investigation need
    needs_trace = task.get("debug_mode", False)
    
    # Decision
    if priority == "HIGH" or error_count >= 2 or needs_trace:
        return "full"
    return "lite"
```

## 3. Memory Update Pattern

After each turn, update memory with the outcome:

```python
import yaml
from datetime import datetime

def update_memory(run_id: str, outcome: str, error_type: str, route_mode: str):
    """Append run evaluation to reflect.md."""
    
    new_run = {
        "run_id": run_id,
        "outcome": outcome,
        "error_type": error_type,
        "route_mode": route_mode,
        "gate_signals": {
            "task_priority": "ROUTINE",
            "repeated_error_count": 0,
            "needs_deep_trace": False
        },
        "gate_reason": "Routine task with no escalation signals",
        "note": f"Completed {outcome}"
    }
    
    reflect_path = Path("memory/reflect.md")
    content = reflect_path.read_text()
    
    # Find and update Run Evaluation section
    # (In production, use structured YAML updates)
    
    reflect_path.write_text(content)
```

## 4. Skill Usage Tracking

The system automatically tracks which skills are being used:

```python
def update_skill_telemetry(skill_calls: List[str]):
    """Update skill usage statistics."""
    
    from collections import Counter
    
    total = len(skill_calls)
    counter = Counter(skill_calls)
    
    # Calculate metrics
    top_skill_ratio = max(counter.values()) / total if total > 0 else 0
    hhi = sum((count / total) ** 2 for count in counter.values())
    over_specialized = top_skill_ratio > 0.65 or hhi > 0.45
    
    # Log to reflect.md
    telemetry = {
        "window": "last_session",
        "total_skill_calls": total,
        "unique_skills": len(counter),
        "calls_by_skill": [
            {skill: count} for skill, count in counter.most_common()
        ],
        "top_skill_ratio": round(top_skill_ratio, 2),
        "hhi": round(hhi, 2),
        "over_specialized": over_specialized,
        "decision": "expand diversity" if over_specialized else "normal"
    }
    
    return telemetry
```

## 5. Four Memory Layers in Practice

### L0: Events (Raw Records)
```yaml
- id: evt-001
  time: 2026-04-25T10:00:00Z
  source: dialogue:turn_5
  content: User asked for code optimization
  links:
    - to: proc-003
      rel: used_by_task
```

**When to write**: After every turn
**When to read**: During debugging or strategy review

### L1: Semantics (Facts & Preferences)
```yaml
- id: fact-001
  confidence: 0.95
  valid_during: [2026-04-25, null]
  content: User prefers Python over JavaScript
```

**When to write**: Consolidate from L0 with deduplication
**When to read**: Always (Lite-Mode includes this)

### L2: Procedures (How-to Templates)
```yaml
- id: proc-001
  task_type: code_generation
  version: 2
  success_rate: 0.89
  content: |
    1. Clarify requirements from user
    2. Check memory for similar past tasks
    3. Generate initial solution
    4. Request feedback
    5. Iterate based on feedback
```

**When to write**: Lift successful single-case outcomes to reusable templates
**When to read**: Always (Lite-Mode includes this)

### L3: Metacognitive (Self-Improvement)
```yaml
- id: meta-001
  category: calibration
  content: |
    Pattern: Overconfident estimates on deadline tasks.
    Action: Add 20% buffer to estimates for high-priority tasks.
    Due: 2026-05-01
```

**When to write**: Every 5-10 runs or after repeated failures
**When to read**: Full-Mode only (for deep analysis)

## 6. Dual-Memory Read Pattern

Every turn must perform both reads:

```python
def retrieval_step(mode: str = "lite"):
    """Execute retrieval with dual read."""
    
    # ALWAYS read both files, adjust scope by mode
    store = loader.load_store(mode=mode)
    reflect = loader.load_reflect(mode=mode)
    
    # Merge retrieval candidates
    candidates = []
    candidates.extend(retrieve_from(store, mode))
    candidates.extend(retrieve_from(reflect, mode))
    
    # Rank by relevance
    ranked = rank_candidates(candidates, task)
    
    return ranked[:5]  # Return top-5
```

## 7. Evolution Loop

Every 10 turns, evaluate and evolve:

```python
def evolution_step():
    """Update memory policies based on outcomes."""
    
    reflect = loader.load_reflect(mode="full")
    all_runs = reflect.get("run_evaluation", [])
    
    # Analyze success patterns
    success_rate = sum(1 for r in all_runs if r.data["outcome"] == "success") / len(all_runs)
    
    # Update L3 insights
    if success_rate < 0.7:
        # Add learning goal
        pass
    
    # Update retrieval weights
    # Update gate thresholds
    # Promote successful procedures to L2
```

## 8. Troubleshooting

### Gate not escalating when needed?
→ Check `get_gate_signals()` output
→ Verify `repeated_error_count` is being incremented
→ Add logging to `should_escalate()`

### Memory growing too large?
→ Implement TTL for L0 events (e.g., delete after 30 days)
→ Archive old procedures to external storage
→ Use `Lite Snapshot` aggressively

### Skills over-specialized?
→ The system detects this automatically via `over_specialized` flag
→ Response: Increase DiversityBonus in retrieval scoring
→ Inject non-top-skill candidates into L2 retrieval

## 9. Full Example: Q&A Agent

```python
#!/usr/bin/env python3
"""Example: Q&A Agent with Memory Evolution."""

import sys
sys.path.insert(0, 'scripts')

from load_memory import MemoryLoader
from pathlib import Path
from datetime import datetime
import uuid

class MemoryQAAgent:
    def __init__(self, memory_dir: str = "memory"):
        self.loader = MemoryLoader(memory_dir)
        self.memory_dir = Path(memory_dir)
    
    def run(self, question: str, priority: str = "ROUTINE"):
        """Process one question."""
        
        run_id = str(uuid.uuid4())[:8]
        
        # 1. Observe
        print(f"[{run_id}] Q: {question}")
        
        # 2. Retrieve
        mode = self._select_mode(priority)
        print(f"  Mode: {mode.upper()}")
        
        store = self.loader.load_store(mode=mode)
        reflect = self.loader.load_reflect(mode=mode)
        
        # 3. Act
        answer = self._generate_answer(question, store)
        print(f"  A: {answer}")
        
        # 4-6. Evaluate, Reflect, Consolidate
        outcome = "success"  # In real system, evaluate quality
        self._update_memory(run_id, question, answer, outcome, mode)
        
        return answer
    
    def _select_mode(self, priority: str) -> str:
        signals = self.loader.get_gate_signals()
        if priority == "HIGH" or signals.get("repeated_error_count", 0) >= 2:
            return "full"
        return "lite"
    
    def _generate_answer(self, question: str, store: dict) -> str:
        # Simplified: just use L1 facts
        facts = store.get("L1", [])
        relevant = [f for f in facts if "question" in str(f.data)]
        return f"Based on {len(facts)} facts in memory: [answer]"
    
    def _update_memory(self, run_id: str, q: str, a: str, outcome: str, mode: str):
        # In production, actually write to reflect.md
        print(f"  ✓ Memory updated")


if __name__ == "__main__":
    agent = MemoryQAAgent()
    
    # Initialize if needed
    if not (Path("memory") / "store.md").exists():
        print("Initializing memory system...")
        import subprocess
        subprocess.run(["python", "scripts/init_memory_system.py", "--path", "memory"])
    
    # Run some questions
    agent.run("What is Python?", priority="ROUTINE")
    agent.run("Debug this error", priority="HIGH")
    agent.run("What do I prefer?")
    
    print("\n✓ Agent completed")
```

Run it:
```bash
python example_qa_agent.py
```

## Next Steps

1. ✓ Initialize memory with `init_memory_system.py`
2. ✓ Load memory in your code with `MemoryLoader`
3. ✓ Implement the 7-step runtime loop
4. ✓ Track skills and detect over-specialization
5. ✓ Run evolution every 10-50 turns
6. ? Monitor memory size and clean up old L0 events
7. ? Implement version control for procedures (L2)

For more details, see:
- `../SKILL.md` - Complete architectural specification
- `./four-layer-memory-detail.md` - Deep dive into each layer
- `./examples.md` - More integration patterns
