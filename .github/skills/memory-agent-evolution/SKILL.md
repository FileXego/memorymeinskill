---
name: memory-agent-evolution
description: This skill should be used when the user asks to "设计 memory agent 架构", "搭建分层记忆系统", "加入元认知反思层", "构建带知识链接的长期记忆", "让智能体持续进化", "用 Markdown 做记忆存储", or requests a "四层记忆 + 两层控制 + 时间感知知识图" blueprint with reflect/store dual-memory classes and evolution loop.
argument-hint: 目标任务、业务场景、约束条件、现有技术栈
user-invocable: true
disable-model-invocation: false
---
# Memory Agent Evolution (Lightweight Markdown Edition)

## Purpose

Define a continuous multi-dimensional evolving memory architecture with:

- Four memory layers: L0, L1, L2, L3
- Two control layers: Memory Orchestrator, Reflector/Critic
- One graph backbone: Temporal Knowledge Graph (TKG)
- Two runtime memory classes: Store and Reflect

Produce an actionable architecture spec that supports long-term learning, adaptive behavior, and lightweight operation using Markdown storage.

## When to Use

Apply this skill for requests that involve:

- Long-term memory for agents or copilots
- Layered cognition (episodic, semantic, procedural, metacognitive)
- Knowledge linking across time
- Reflection-driven policy improvement
- Failure pattern learning and strategy evolution

Do not apply this skill for:

- Single-turn memory snippets
- Stateless prompt-only tasks
- Pure UI design tasks without memory intelligence

## Constraint Profile

Use the default profile:

- Lightweight by default: Lite-Invoke first, Full-Invoke only when gate conditions are met
- Markdown-only storage
- No risk or compliance constraints unless explicitly requested

Do not add risk-control modules by default.

## Required Folder Layout

Use this minimal layout in the same folder:

```text
memory/
  store.md
  reflect.md
```

Optional archives may be added later, but runtime reads must always target both primary files.

## Runtime Read Contract (Mandatory)

Always read both memory classes during runtime.

Per turn:

1. Read `memory/store.md`
2. Read `memory/reflect.md`
3. Merge retrieval candidates from both
4. In Lite-Invoke mode, read only minimal slices from both files

Read contract:

`ReadSet = StoreSet + ReflectSet`

Never run with Store-only or Reflect-only reads.

## Inputs

Collect these inputs before design:

- Business objective: what outcomes the agent must optimize
- Task mix: QA, execution, planning, debugging, review, etc.
- Constraints: latency, storage budget, explainability level
- Feedback channel: explicit ratings, implicit signals, tool outcomes
- Existing stack: vector DB, graph DB, event bus, workflow engine

If critical inputs are missing, make assumptions explicit and tag them as `ASSUMPTION`.

## Core Architecture

### 1. Four Memory Layers

Define each layer with distinct write/read and lifecycle semantics.

#### L0 Event Layer (Episodic)

- Store raw interaction turns, tool operations, runtime signals, and outcomes
- Preserve what happened
- Keep high-throughput, low-abstraction records
- Attach timestamp, source, and trace ID

#### L1 Semantic Layer

- Store stable facts, constraints, preferences, concept/entity relations
- Represent what is known
- Maintain deduplication, verifiability, and versioning
- Resolve conflicts through confidence and provenance scoring

#### L2 Procedural Layer

- Store strategy templates, workflows, decision heuristics, repair patterns
- Represent how to act
- Bind procedures to task types
- Track performance by version and run context

#### L3 Metacognitive Layer

- Store self-evaluation, bias calibration, blind spots, learning agenda
- Represent how well the system is performing and how to improve
- Keep low-frequency but high-value insights
- Drive long-term adaptation and policy updates

### 2. Two Control Layers

#### Control A: Memory Orchestrator

- Orchestrate ingest, extraction, linking, consolidation, retrieval, and writeback
- Enforce layer-specific policies (TTL, dedup, versioning, privacy scope)
- Gate read/write paths based on task type and confidence thresholds

#### Control B: Reflector/Critic

- Evaluate each run from quality signals
- Classify failures (retrieval, reasoning, execution, communication)
- Produce metacognitive insights and learning actions
- Trigger strategy rollback, supersede, or A/B promotion

### 3. Temporal Knowledge Graph (TKG)

Use TKG as the cross-layer linkage backbone.

#### Node Types

- Event
- Fact
- Concept
- Procedure
- MetaInsight
- Goal

#### Relationship Types

- supports
- contradicts
- derived_from
- used_by_task
- improves
- fails_on
- supersedes
- valid_during

Use `valid_during` for temporal validity windows and `supersedes` for controlled replacement of outdated memory.

## Mandatory Component Topology

Implement this logical pipeline:

1. Ingestor: receive event stream
2. Extractor: extract fact/preference/task/error signals
3. Linker: align entities and create graph edges
4. Consolidator: promote L0 content into L1/L2/L3
5. Retriever: perform cross-layer retrieval with gated scoring
6. Reasoner: execute generation or action planning
7. Reflector: analyze outcome and produce meta-insights
8. Evolution Manager: update weights, confidence, and policy versions

## Runtime Closed Loop (Per Turn)

Execute this loop every turn:

1. Observe: read task, context, constraints
2. Retrieve: evaluate gate -> choose Lite/Full expert -> gather candidates with selected read scope
3. Act/Reason: generate response or tool plan
4. Evaluate: collect explicit/implicit feedback
5. Reflect: detect success and failure patterns
6. Consolidate: write promoted memory into L1/L2/L3
7. Evolve: update retrieval weights and policy priorities

## Layer-Gated Retrieval Policy

Use weighted scoring:

`score = a*Relevance + b*Confidence + c*Recency + d*SuccessRate + e*MetaPriority + f*DiversityBonus`

Set routing presets by scenario:

- Simple fact QA: prioritize L1
- Task execution: prioritize L2
- Repeated failure: prioritize L3
- Context continuity: mix L0 + L1

Adjust coefficients dynamically from evaluation signals in `store.md` and `reflect.md`.

## MoE Gate (Full-Store, Lite-Invoke)

Apply a lightweight MoE-style gate so memory is complete on write but efficient on read.

### Storage Mode (always complete)

- Always use Full-Store writeback for promoted memory (L0/L1/L2/L3)
- Keep traceability, links, and versions intact

### Invocation Modes

#### Expert-Lite (default)

Use when routine task and no critical escalation signal.

Read scope:
- `store.md`: prioritize L1/L2 and optional `Lite Snapshot`
- `reflect.md`: latest run evaluation + skill telemetry summary + top learning agenda item

#### Expert-Full (escalation)

Use when deep context is required.

Read scope:
- `store.md`: full L0/L1/L2/L3 sections
- `reflect.md`: full evaluation and learning context

### Gate Condition (rule-based)

Use Expert-Full when any condition is true:
- `task_priority = HIGH`
- `repeated_error_count >= 2`
- `needs_deep_trace = true`

Otherwise use Expert-Lite.

This keeps invocation professional and lightweight while preserving complete storage.

## Markdown Data Contract (Minimum)

Use Markdown records with YAML frontmatter.

### Store Class Template (`memory/store.md`)

```markdown
---
file_type: memory_store
version: 1
updated_at: 2026-04-24T00:00:00Z
---

## L0 Events
- id: evt-001
  time: 2026-04-24T10:00:00Z
  source: dialogue:turn_1
  content: user request summary
  links:
    - to: fact-001
      rel: derived_from
      weight: 0.82

## L1 Semantics
- id: fact-001
  confidence: 0.76
  valid_during: [2026-04-24, null]
  content: stable fact or preference

## L2 Procedures
- id: proc-001
  task_type: architecture_design
  success_rate: 0.67
  version: 3
  content: reusable workflow steps

## Lite Snapshot
- last_compacted_at: 2026-04-24T10:00:00Z
  l1_focus_ids: [fact-001]
  l2_focus_ids: [proc-001]
  note: minimal slice for Expert-Lite retrieval

## L3 MetaInsights
- id: meta-001
  category: calibration
  content: overconfidence detected in constraint estimation
```

### Reflect Class Template (`memory/reflect.md`)

```markdown
---
file_type: memory_reflect
version: 1
updated_at: 2026-04-24T00:00:00Z
---

## Run Evaluation
- run_id: run-001
  outcome: success|partial|fail
  error_type: retrieval|reasoning|execution|communication|none
  route_mode: lite|full
  gate_signals:
    task_priority: ROUTINE|HIGH
    repeated_error_count: 0
    needs_deep_trace: false
  gate_reason: why selected expert mode
  note: short post-run reflection

## Skill Usage Telemetry
- window: last_7d
  total_skill_calls: 24
  unique_skills: 5
  calls_by_skill:
    - memory-agent-evolution: 12
    - bug-detective: 4
    - test-driven-development: 3
    - verification-before-completion: 3
    - other: 2
  top_skill_ratio: 0.50
  hhi: 0.33
  over_specialized: false
  decision: keep current routing

## Learning Agenda
- item: increase procedural diversity for execution tasks
  owner: evolution-manager
  due: 2026-05-01

## Route Replay
- replay_id: replay-001
  selected_expert: Expert-Lite|Expert-Full
  decision_path: "signal check -> mode selection"
  can_replay: true
```

## Skill Usage Memory (Required)

Persist both metrics below in `memory/reflect.md`:

- Skill invocation frequency
- Over-specialization to a narrow skill subset

Compute:

- `top_skill_ratio = max(calls_by_skill) / total_skill_calls`
- `hhi = sum((calls_by_skill_i / total_skill_calls)^2)`

Default rule:

- `over_specialized = true` if `top_skill_ratio > 0.65` or `hhi > 0.45`

If over-specialized for consecutive windows:

1. Increase `DiversityBonus` in retrieval scoring
2. Force at least one non-top-skill procedure candidate in L2 retrieval
3. Create a learning experiment item in L3
4. Keep Expert-Lite as default but inject one underused-skill procedure candidate
5. Escalate to Expert-Full only if repeated failure persists

## Metacognitive Subsystem Contract (L3)

Split L3 into four operational ledgers:

1. Self-Monitoring Ledger

- Track calibration drift: overconfidence vs underconfidence

2. Error Taxonomy Ledger

- Classify failure root causes: retrieval, reasoning, execution, communication

3. Strategy Ledger

- Compare strategy versions, contexts, and outcomes

4. Learning Agenda Ledger

- Store next learning goals, experiments, and deadlines

Treat L3 as executable improvement logic, not passive logs.

## Continuous Evolution Dimensions

Evaluate evolution over five dimensions:

1. Accuracy

- Detect fact conflicts
- Reweight by source quality and verification outcomes

2. Freshness

- Apply TTL, decay, and periodic revalidation

3. Transferability

- Lift single-case success into reusable procedures (L2)

4. Robustness

- Capture boundary conditions, counterexamples, and fail cases

5. Adaptivity

- Reweight preferences/strategies from user feedback and run metrics

## Decision and Branching Rules

Apply these branches during consolidation and evolution:

0. Mode branch (MoE gate)

- If escalation condition is met:
  - use Expert-Full read scope
- Else:
  - use Expert-Lite read scope

1. Conflict branch

- If new fact contradicts active L1 fact and confidence gap < threshold:
  - keep both
  - link with `contradicts`
  - schedule verification
- If confidence gap >= threshold:
  - mark lower-confidence fact as superseded
  - update `valid_time.to`

2. Procedure branch

- If procedure success rate drops below rollback threshold:
  - demote version priority
  - activate fallback procedure
  - log to L3 Strategy Ledger

3. Reflection branch

- If the same error class repeats over N runs:
  - increase L3 retrieval weight
  - inject targeted guardrails into L2 templates
  - create learning experiment item

4. Freshness branch

- If memory is stale and high-impact:
  - require revalidation before high-stakes usage
- If stale and low-impact:
  - allow soft use with confidence penalty

5. Skill concentration branch

- If `over_specialized = true` in reflect memory:
  - increase diversity routing weight
  - prioritize procedures from underused skills
  - log strategy change in L3 Strategy Ledger

## Quality Gates (Completion Checks)

Do not mark architecture complete until all checks pass:

1. Layer separation check

- Clear write/read boundaries for L0/L1/L2/L3

2. Graph linkage check

- Every promoted item has at least one typed edge in TKG

3. Traceability check

- Each decision can trace to memory_id, source, and version

4. Evolution check

- At least one measurable update path for each evolution dimension

5. Dual-read check

- Runtime loop reads both `store.md` and `reflect.md` every turn

6. Lightweight check

- Primary memory footprint stays in two Markdown files

7. Operational check

- MVP, V2, V3 milestones each have scope and acceptance criteria

8. MoE explainability check

- Each run records gate inputs, selected expert, and route reason

9. Route replay check

- Reviewer can replay why Lite or Full was selected

## Roadmap

### MVP (Week 1-2)

- Build L0 + L1 + basic TKG links
- Implement per-turn summary, preference extraction, fact dedup
- Ship basic retrieval scoring

### V2 (Week 2-4)

- Add L2 procedural memory
- Add task-type routing
- Add failure replay and procedure metrics

### V3 (Week 4-8)

- Add full L3 metacognitive subsystem
- Run strategy A/B tests
- Enable auto-updating retrieval and policy weights

## Output Template

When applying this skill, output in this order:

1. Architecture Blueprint (4 layers + 2 controls + TKG)
2. Component Interaction and Data Flow
3. Lightweight Markdown Storage Contract (`store.md` + `reflect.md`)
4. Retrieval and Routing Policy
5. Reflection and Evolution Policy
6. Skill Usage Concentration Analysis Policy
7. Milestones and Acceptance Gates
8. Route Decision Summary (gate inputs, selected expert, and escalation reason)

## Failure Recovery Playbook

If architecture quality is weak or ambiguous:

1. Identify missing assumptions and unresolved trade-offs
2. Run contradiction scan in L1 and strategy drift scan in L2/L3
3. Tighten branching thresholds and rollback criteria
4. Re-evaluate against quality gates
5. Re-issue revised architecture with explicit diffs

## Success Criteria

Consider this skill successful when it consistently produces:

- Reusable, layered memory architecture
- Explicit temporal knowledge linking
- Executable metacognitive improvement loops
- Measurable evolution controls and release milestones
- Runtime dual-read compliance for Store and Reflect memory classes
- Persistent skill-frequency and over-specialization memory
- Full-Store writeback with Lite-Invoke default and explicit gate-based escalation
