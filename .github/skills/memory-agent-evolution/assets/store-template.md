---
file_type: memory_store
version: 1
created_at: 2026-04-25T00:00:00Z
updated_at: 2026-04-25T00:00:00Z
---

# Memory Store Template

Use this template when initializing a new memory system.
This file maintains the complete record of all four memory layers.

## L0 Events

Raw interaction data. High-throughput, low-abstraction records of what happened.

```yaml
- id: evt-NNN
  time: ISO-8601-timestamp
  source: dialogue:turn_N | tool:name | system:event
  content: Raw text or summary of the event
  links:
    - to: fact-XXX | proc-XXX | evt-MMM
      rel: derived_from | response_to | triggers | ...
      weight: 0.0-1.0
```

Guidelines:
- Write immediately after every turn or action
- Keep ~100 most recent, archive older than 30 days
- Use high-level summary for large events
- Include all feedback signals (explicit and implicit)

**Example:**
```yaml
- id: evt-001
  time: 2026-04-25T10:30:00Z
  source: dialogue:turn_1
  content: |
    User asked: "How do I optimize this database query?"
    Context: PostgreSQL, 1M+ rows, join operation
  links:
    - to: proc-001
      rel: triggers
      weight: 1.0
```

## L1 Semantics

Stable facts, constraints, and preferences derived from L0.

```yaml
- id: fact-NNN
  confidence: 0.0-1.0
  valid_during: [YYYY-MM-DD, null | YYYY-MM-DD]
  content: The actual fact or preference statement
  source_events:
    - evt-XXX
    - evt-YYY
  note: Optional context or derivation explanation
```

Guidelines:
- Promote from L0 when: appears 2+ times, confidence ≥ 0.6, stable
- Use `valid_during` for temporal reasoning
- Include source events for traceability
- Set confidence based on evidence strength

**Example:**
```yaml
- id: fact-001
  confidence: 0.92
  valid_during: [2026-04-25, null]
  content: User prefers PostgreSQL for large datasets
  source_events:
    - evt-001
    - evt-005
  note: Stated preference + shown in 3 queries

- id: fact-002
  confidence: 0.78
  valid_during: [2026-04-15, 2026-05-15]
  content: Current project budget limit is $50,000
  source_events:
    - evt-003
  note: Temporary constraint during Q2 project
```

## L2 Procedures

Reusable workflows and strategy templates for how to act.

```yaml
- id: proc-NNN
  task_type: code_generation | debugging | planning | ...
  version: integer
  success_rate: 0.0-1.0
  failure_patterns:
    - error_type: count | percentage
  created_at: ISO-8601
  last_updated: ISO-8601
  content: |
    Multi-line procedure steps:
    
    1. Step One
       - Sub-step
       - Sub-step
    
    2. Step Two
       ...
  boundary_conditions:
    - applies_to: condition description
    - avoid_when: condition description
    - performance_constraint: description
  metrics:
    avg_time_to_completion: seconds
    avg_iterations: number
    user_satisfaction: 0.0-1.0
```

Guidelines:
- Promote from L0 when: 3+ successes, generalizable, >30sec of thinking
- Include failure modes and boundary conditions
- Track metrics for improvement
- Version procedures when improved

**Example:**
```yaml
- id: proc-001
  task_type: query_optimization
  version: 2
  success_rate: 0.85
  failure_patterns:
    - timeout: 0.10
    - wrong_indexes: 0.05
  created_at: 2026-04-20
  last_updated: 2026-04-25
  content: |
    ## PostgreSQL Query Optimization
    
    1. Analyze Current Query
       - Run EXPLAIN to see execution plan
       - Check indexes on join columns
       - Note number of rows and table sizes
    
    2. Identify Bottleneck
       - Sequential scans? Add indexes.
       - Bad join order? Rewrite with better joins.
       - Missing statistics? Run ANALYZE.
    
    3. Optimize Strategy
       - Add indexes on foreign keys
       - Consider query restructuring
       - Profile with EXPLAIN ANALYZE
    
    4. Validate
       - Test on production-sized data
       - Verify query returns correct results
       - Check execution time < 100ms
    
    5. Deploy and Monitor
  
  boundary_conditions:
    - applies_to: PostgreSQL 12+
    - avoid_when: Tables < 10k rows (optimization overkill)
    - performance_constraint: Must complete analysis < 5min

  metrics:
    avg_time_to_completion: 4.2
    avg_iterations: 2.1
    user_satisfaction: 0.89
```

## Lite Snapshot

Minimal slice for Lite-Mode fast reads. Updated during consolidation.

```yaml
- last_compacted_at: ISO-8601
  l1_focus_ids:
    - fact-001
    - fact-002
    - fact-003
  l2_focus_ids:
    - proc-001
    - proc-002
  note: Top 3 facts and 2 procedures for fast retrieval
```

Guidelines:
- Update after every consolidation
- Include top 3-5 facts (highest confidence + most recent)
- Include top 2-3 procedures (highest success rate + most recent)
- Use for Lite-Mode reads only

## L3 MetaInsights

Self-evaluation, calibration, and learning goals.

```yaml
- id: meta-NNN
  category: calibration | error_taxonomy | strategy | learning_agenda
  created_at: ISO-8601
  content: |
    Multi-line insight content.
    
    For calibration: Describe the pattern, evidence, root cause, action.
    For error_taxonomy: Breakdown of failure modes.
    For strategy: A/B test setup and results.
    For learning_agenda: What to improve and by when.
```

Guidelines:
- Create calibration insights: every 10 runs
- Create error taxonomy: every 20-50 runs
- Create strategy insights: after experiments
- Create learning agenda: as needed

**Examples:**

```yaml
# Calibration
- id: meta-001
  category: calibration
  created_at: 2026-04-25
  content: |
    ## Overconfidence on Time Estimates
    
    Pattern: I estimate tasks 20% faster than they actually take.
    Evidence: Last 20 tasks, avg estimate 2hr, avg actual 2.4hr
    Root cause: Full-Mode retrieval makes me overconfident
    
    Action: Add 25% time buffer to all estimates
    Target: Achieve 90% on-time completion rate

# Error Taxonomy
- id: meta-002
  category: error_taxonomy
  created_at: 2026-04-25
  content: |
    ## Failure Analysis (Last 50 runs)
    
    Success: 39 (78%)
    Failure: 11 (22%)
      - Retrieval error: 5 (incorrect memory selection)
      - Reasoning error: 3 (logic mistake)
      - Execution error: 2 (tool failure)
      - Communication error: 1 (misunderstood)
    
    Priority fix: Improve retrieval accuracy (45% of failures)

# Strategy
- id: meta-003
  category: strategy
  created_at: 2026-04-25
  content: |
    ## A/B Test: Lite-Mode vs Full-Mode
    
    Baseline:
    - Lite: 1000 tasks, 76% success, 50ms avg
    - Full: 200 tasks, 82% success, 400ms avg
    
    Result: Not worth the 8x latency cost for 6% improvement
    Recommendation: Keep current gate, explore hybrid routing

# Learning Agenda
- id: meta-004
  category: learning_agenda
  created_at: 2026-04-25
  content: |
    ## Improvement Goals
    
    - [ ] Increase retrieval accuracy to 85% by 2026-05-15
    - [ ] Implement cost-aware procedure selection by 2026-05-01
    - [ ] Reduce average task time by 20% by 2026-06-01
    - [ ] Add error recovery procedures by 2026-05-20
```

---

## Usage Notes

1. **Keep complete**: Always write all four layers even if some are empty
2. **Update frequently**: Write to store.md after consolidation (~every 10 turns)
3. **Time-order within sections**: Put newest items first
4. **Preserve links**: Every item should link to related items
5. **Archive monthly**: Move L0 older than 30 days to archive
6. **Validate YAML**: Ensure file is valid YAML after edits
