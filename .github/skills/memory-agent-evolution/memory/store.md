---
file_type: memory_store
version: 1
updated_at: 2026-04-24T00:00:00Z
---

# Memory Store

## L0 Events

- id: evt-template-001
  time: 2026-04-24T00:00:00Z
  source: dialogue:turn_template
  content: short event summary
  links:
  - to: fact-template-001
    rel: derived_from
    weight: 0.80

## L1 Semantics

- id: fact-template-001
  confidence: 0.75
  valid_during: [2026-04-24, null]
  content: stable fact or preference

## L2 Procedures

- id: proc-template-001
  task_type: general
  version: 1
  success_rate: 0.50
  content: reusable task procedure

## Lite Snapshot

- last_compacted_at: 2026-04-24T00:00:00Z
  l1_focus_ids: [fact-template-001]
  l2_focus_ids: [proc-template-001]
  note: minimal slice for Expert-Lite retrieval

## L3 MetaInsights

- id: meta-template-001
  category: calibration
  content: brief metacognitive note
