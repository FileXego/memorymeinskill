# Four-Layer Memory System: Deep Dive

This document provides detailed semantics and implementation patterns for each memory layer.

## Layer 0: Events (Episodic / High-Throughput)

### Purpose
Capture raw interaction data exactly as it occurs. Events are the atomic unit of memory—everything else is derived from events.

### Writing Pattern

**When**: After every action, tool call, feedback signal

```yaml
# Example: User gives feedback
- id: evt-042
  time: 2026-04-25T14:32:00Z
  source: dialogue:turn_15
  content: |
    User said: "Your code suggestion is too complex. 
    Can you simplify it?"
  links:
    - to: resp-041
      rel: response_to
      weight: 1.0
    - to: fact-001
      rel: updates_preference
      weight: 0.8
```

**Fields**:
- `id`: Unique identifier (evt-NNN)
- `time`: ISO 8601 timestamp
- `source`: Origin (dialogue:turnN, tool:name, system:event)
- `content`: Actual event text or summary
- `links`: Edges to other memory items
  - `to`: Target ID
  - `rel`: Relationship type (see Temporal Knowledge Graph)
  - `weight`: Confidence/strength (0.0-1.0)

### Reading Pattern

**Lite-Mode**: Skip L0 entirely (use Lite Snapshot instead)

**Full-Mode**: Read all L0, filter by:
- Time range: last 100 events or last 24 hours
- Source: specific dialogue turn or tool call
- Content pattern: search by keyword

### Retention Policy
- Keep last 100 events in memory
- Archive older events to external storage monthly
- Delete events older than 90 days unless explicitly marked

### Key Metrics
- Event throughput: >100 events/hour typical
- Event size: 100-500 bytes average
- Compression ratio: ~40% (GZIP) due to repetitive structure

---

## Layer 1: Semantics (Facts / Knowledge Base)

### Purpose
Maintain a deduped, versioned knowledge base of facts, constraints, and preferences.

### Semantics Include
- Facts: "Python is better for data science than JavaScript"
- Preferences: "User prefers concise explanations"
- Constraints: "Budget limit: $50k"
- Relations: "Function A calls Function B"
- Concepts: "Microservices = distributed architecture pattern"

### Writing Pattern

**Conditions for promotion from L0 → L1**:
1. Appears in 2+ events
2. Confidence score ≥ 0.6
3. Stable (hasn't changed in 5+ events)
4. Relevant to future tasks

**Example: Fact extraction from events**

```yaml
Events leading to this fact:
- evt-001: "User asked about Python for ML"
- evt-005: "User said 'I prefer Python'"
- evt-012: "User rejected JavaScript suggestion"

Promoted fact:
- id: fact-001
  confidence: 0.87
  valid_during: [2026-04-25, null]
  content: User prefers Python for data science work
  source_events: [evt-001, evt-005, evt-012]
  contraints: applies to all future code suggestions
  note: High confidence from multiple signals
```

**Fields**:
- `id`: Fact identifier (fact-NNN)
- `confidence`: 0.0-1.0, updated by conflicts
- `valid_during`: [start_date, end_date or null]
  - `null` means "still valid"
  - Enables temporal reasoning
- `content`: The actual fact statement
- `source_events`: L0 events that produced this
- `constraints`: Scope or conditions
- `note`: Why this is important

### Conflict Resolution

**When new fact contradicts existing fact**:

```python
def resolve_conflict(new_fact, existing_fact):
    confidence_gap = abs(new_fact.confidence - existing_fact.confidence)
    
    if confidence_gap >= 0.3:
        # High confidence gap → replace
        if new_fact.confidence > existing_fact.confidence:
            return "replace"
        else:
            return "ignore_new"
    else:
        # Low confidence gap → keep both and link
        return "keep_both_with_contradiction_edge"
```

**Example: Conflict**

```yaml
Existing:
- id: fact-001
  confidence: 0.65
  content: User prefers Python

New (conflicting):
- id: fact-002
  confidence: 0.72
  content: User needs to use JavaScript for this project

Action: Keep both with "contradicts" edge
- fact-001 contradicts fact-002 (context-dependent)
- Schedule verification
- Lower confidence of fact-001 for JS contexts
```

### Reading Pattern

**Lite-Mode**: Read all L1 (usually 50-200 facts)
- Used for: Quick context, preference checking, constraint validation

**Full-Mode**: Read all L1 + provenance chain
- Used for: Debugging, fact verification, understanding derivation

### Queries Supported

```python
# All facts about a topic
loader.query_l1(topic="Python")

# Facts with high confidence
loader.query_l1(confidence_gte=0.8)

# Facts valid during a time period
loader.query_l1(valid_during=(date1, date2))

# Facts that contradict each other
loader.query_l1(contradictions_only=True)
```

---

## Layer 2: Procedures (How-To / Strategy Templates)

### Purpose
Store reusable workflows and decision heuristics that encode "how to act".

### Procedures Include
- Task templates: "How to generate code"
- Debugging workflows: "How to diagnose null reference errors"
- Decision heuristics: "When to escalate to Full-Mode"
- Repair patterns: "How to fix common mistakes"

### Anatomy of a Procedure

```yaml
- id: proc-042
  task_type: code_generation
  version: 3
  success_rate: 0.78
  failure_patterns:
    - timeout: 0.05  # 5% of runs timeout
    - user_reject: 0.15  # 15% rejected by user
    - compile_error: 0.02
  created_at: 2026-04-20
  last_updated: 2026-04-25
  content: |
    ## Procedure: Generate Production Python Code
    
    1. Understand Requirements
       - Parse task description
       - Check memory for similar tasks (L1/L2)
       - Validate against constraints (L1 facts)
    
    2. Initial Generation
       - Use template from L2 if available
       - Generate code with type hints
       - Add docstrings
    
    3. Quality Check
       - Syntax check
       - Security review (SQL injection, etc.)
       - Performance review
    
    4. Request Feedback
       - Show code to user
       - Ask for feedback
       - Log feedback to L0 events
    
    5. Iterate
       - Apply feedback
       - Re-validate
       - Store improved version as new procedure version
    
    6. Consolidate
       - If successful: promote as template
       - Record metrics: time, quality, feedback
  
  boundary_conditions:
    - applies_to: functions under 100 lines
    - avoid_when: ML/optimization code
    - performance_constraint: must complete < 2sec
  
  metrics:
    avg_user_satisfaction: 0.82
    avg_time_to_completion: 1.2
    avg_iterations: 2.1
```

**Fields**:
- `id`: Procedure identifier (proc-NNN)
- `task_type`: Category (code_generation, debugging, planning, etc.)
- `version`: Version number (1, 2, 3...)
- `success_rate`: 0.0-1.0 across all uses
- `failure_patterns`: Breakdown of failure modes
- `content`: The actual steps
- `boundary_conditions`: When to use/avoid
- `metrics`: Performance data

### Writing Pattern

**Conditions for promotion from L0 → L2**:
1. Successfully completed same task 3+ times
2. Task is generalizable (not one-off)
3. Takes >30 seconds of thinking
4. Has reusable steps

**Process**:

```python
def promote_to_procedure(past_successes):
    """Lift single successes into reusable templates."""
    
    # Identify pattern
    common_steps = extract_common_steps(past_successes)
    
    # Generalize
    generalized = generalize_for_variants(common_steps)
    
    # Create procedure
    procedure = {
        "id": f"proc-{next_id}",
        "task_type": classify_task(past_successes),
        "version": 1,
        "success_rate": 1.0,
        "content": generalized,
        "boundary_conditions": extract_constraints(past_successes)
    }
    
    return procedure
```

### Procedure Versioning

When a procedure changes:

```yaml
# Version 1 (Original)
- id: proc-001-v1
  success_rate: 0.65
  valid_during: [2026-04-20, 2026-04-25]
  status: superseded

# Version 2 (Improvement)
- id: proc-001-v2
  success_rate: 0.78
  valid_during: [2026-04-25, null]
  status: active
  improvements:
    - Added error handling
    - Reduced timeout rate from 10% to 5%
```

### Reading Pattern

**Lite-Mode**: Read all L2 procedures (usually 20-50)
- Used for: Task routing, strategy selection

**Full-Mode**: Read all L2 + failure history + metrics
- Used for: Deep debugging, strategy optimization

### Procedure Lookup

```python
# Exact task type
procedures = loader.query_l2(task_type="code_generation")

# High success rate
procedures = loader.query_l2(success_rate_gte=0.75)

# Applicable to current constraints
procedures = loader.query_l2(
    boundary_conditions_match=current_constraints
)

# Not failed recently
procedures = loader.query_l2(
    failure_patterns_recent=False
)
```

---

## Layer 3: Metacognitive (Self-Evaluation / Learning Goals)

### Purpose
Track system performance, identify blind spots, and drive long-term improvement.

### L3 Includes

1. **Self-Monitoring Ledger** (Calibration)
   - Overconfidence: predicting success but actually failing
   - Underconfidence: hesitating when should be confident
   - Blind spots: patterns that system misses

2. **Error Taxonomy Ledger** (Failure Analysis)
   - Retrieval errors: couldn't find relevant memory
   - Reasoning errors: wrong logic or inference
   - Execution errors: tool call failed
   - Communication errors: unclear or misunderstood

3. **Strategy Ledger** (Performance Tracking)
   - What strategies work in what contexts
   - Trade-offs and trade-offs revisited
   - A/B test results

4. **Learning Agenda** (What to Improve)
   - High-priority improvements
   - Experiments to run
   - Deadlines

### Anatomy of L3 Records

```yaml
- id: meta-001
  category: calibration
  created_at: 2026-04-20
  content: |
    ## Overconfidence on Deadline Pressure
    
    Pattern: When user marks task as HIGH priority, 
    I estimate 30% faster than actually needed.
    
    Evidence: 12 HIGH-priority tasks, 8 overshot deadline
    Success rate: 33% (vs 78% for ROUTINE tasks)
    
    Root cause: Gate escalates to Full-Mode retrieval,
    which makes me overconfident about my capabilities.
    
    Action: Add 20% buffer to time estimates for HIGH tasks
    
    A/B test: Start 2026-04-25, run for 20 tasks
    Success metric: Actual time within estimate 80% of time

- id: meta-002
  category: error_taxonomy
  created_at: 2026-04-25
  content: |
    ## Error Distribution (Last 100 runs)
    
    Success: 78
    Failure: 22
      - Retrieval error: 8 (couldn't find relevant memory)
      - Reasoning error: 6 (wrong logic)
      - Execution error: 5 (tool failed)
      - Communication error: 3 (misunderstood)
    
    Action: 
    - Increase Lite Snapshot coverage (reduce retrieval errors)
    - Add more error examples to L2 procedures
    - Verify tool stability

- id: meta-003
  category: strategy
  created_at: 2026-04-25
  content: |
    ## Strategy A/B: Lite-Mode vs Full-Mode
    
    Experiment: When should we escalate to Full-Mode?
    
    Baseline (current):
    - Lite-Mode: 1000 tasks, 76% success, 50ms avg
    - Full-Mode: 200 tasks, 82% success, 400ms avg
    
    Result: Full-Mode is not worth it except for very high stakes
    Recommendation: Keep current gate conditions
    
    Next experiment: Try probabilistic routing (70% Lite, 30% Full)
```

### Writing Pattern

**When to create L3 insights**:
1. After every 10 runs: Basic error analysis
2. After errors patterns repeat: Root cause analysis
3. After strategy change: A/B test results
4. After performance drifts: Calibration check

**L3 Update Frequency**:
- Fast channel: Every 5-10 runs (performance metrics)
- Normal channel: Every 20-50 runs (error analysis)
- Slow channel: Every 100+ runs (strategy review)

### Reading Pattern

**Lite-Mode**: Skip L3 (not needed for routine tasks)

**Full-Mode**: Read all L3
- Used for: Deep debugging, strategy review, learning

### Key Queries

```python
# Recent calibration insights
insights = loader.query_l3(category="calibration", recent=True)

# All error patterns
errors = loader.query_l3(category="error_taxonomy")

# Active A/B tests
experiments = loader.query_l3(category="strategy", status="active")

# Learning goals due soon
agenda = loader.query_l3(category="learning_agenda", due_soon=True)
```

---

## Cross-Layer Linking: Temporal Knowledge Graph

### Relationship Types

```
Events → Facts: derived_from
Events → Procedures: used_by_task
Events → MetaInsights: triggers

Facts → Procedures: enables, contradicts
Facts → Facts: contradicts, implies, similar_to

Procedures → Procedures: supersedes, improves_upon

MetaInsights → Procedures: suggests_change
MetaInsights → Facts: questions_confidence
```

### Example Query

**Question: "Why is procedure X failing?"**

```
meta-001 (failed_on: procedure-X)
  ↓ suggests_change
fact-001 (constraint violated)
  ↓ derived_from
evt-042 (user feedback)
  ↓ related_to
proc-X (the procedure)
```

---

## Summary: When to Use Each Layer

| Layer | Read | Write | Update Freq | Read Cost |
|-------|------|-------|-------------|-----------|
| L0 | Full-Mode only | Every action | Real-time | High |
| L1 | Both modes | Every 5 turns | 5-10 turns | Low |
| L2 | Both modes | Every success | On demand | Low |
| L3 | Full-Mode only | Every 10+ runs | 10-50 turns | High |

### Dual-Mode Read Pattern

**Lite-Mode** (routine tasks):
- L1 facts: Load all
- L2 procedures: Load all
- L3 insights: Load snapshot only

**Full-Mode** (escalated tasks):
- L0 events: Load last 100
- L1 facts: Load all + provenance
- L2 procedures: Load all + metrics + failures
- L3 insights: Load all

---

## Troubleshooting

**Q: Fact conflicts are too frequent**
→ Increase conflict resolution threshold
→ Add more context to facts (boundary conditions)

**Q: Procedures not generalizing well**
→ Require 5+ successes before promotion (not 3)
→ Add stricter boundary conditions

**Q: Memory growing too large**
→ Archive L0 events monthly
→ Implement TTL for facts (e.g., 6 months)
→ Review L2 procedures for obsolescence

**Q: Over-specialization not detected**
→ Check skill telemetry in reflect.md
→ Verify over_specialized flag calculation
→ Review DiversityBonus settings in retrieval
