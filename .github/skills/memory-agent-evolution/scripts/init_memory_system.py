#!/usr/bin/env python3
"""
Initialize Memory Agent Evolution System

This script sets up the memory directory structure and creates
initial store.md and reflect.md files for a new memory agent.

Usage:
    python init_memory_system.py [--path /path/to/memory]
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
import argparse


def create_store_md(memory_dir: Path) -> None:
    """Create initial store.md file."""
    store_path = memory_dir / "store.md"
    
    store_content = """---
file_type: memory_store
version: 1
created_at: {timestamp}
updated_at: {timestamp}
---

# Memory Store (Complete)

This file maintains full memory records across all four layers.
It is written completely on every consolidation (write once, read flexibly).

## L0 Events
- id: init-evt-001
  time: {timestamp}
  source: system:init
  content: Memory system initialization
  links: []

## L1 Semantics
- id: init-fact-001
  confidence: 1.0
  valid_during: [{date}, null]
  content: Memory system initialized and ready for operation

## L2 Procedures
- id: init-proc-001
  task_type: memory_management
  version: 1
  success_rate: null
  content: |
    1. Receive input and context
    2. Evaluate dual-mode gate conditions
    3. Select Lite-Mode or Full-Mode retrieval
    4. Gather memory candidates from L1/L2 (Lite) or all layers (Full)
    5. Execute generation with retrieved memory
    6. Collect evaluation signals
    7. Update retrieval scores and policy weights
    8. Write complete memory back to store.md

## Lite Snapshot
- last_compacted_at: {timestamp}
  l1_focus_ids: [init-fact-001]
  l2_focus_ids: [init-proc-001]
  note: Initial minimal snapshot for Lite-Mode fast read

## L3 MetaInsights
- id: init-meta-001
  category: initialization
  content: Memory system bootstrapped with default policies
"""
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    date = datetime.utcnow().strftime("%Y-%m-%d")
    
    store_path.write_text(
        store_content.format(timestamp=timestamp, date=date)
    )
    print(f"✓ Created {store_path}")


def create_reflect_md(memory_dir: Path) -> None:
    """Create initial reflect.md file."""
    reflect_path = memory_dir / "reflect.md"
    
    reflect_content = """---
file_type: memory_reflect
version: 1
created_at: {timestamp}
updated_at: {timestamp}
---

# Memory Reflect (Complete)

This file maintains reflection, evaluation, and telemetry records.
It tracks routing decisions, skill usage, and learning progress.

## Run Evaluation
- run_id: init-run-001
  outcome: success
  error_type: none
  route_mode: lite
  gate_signals:
    task_priority: ROUTINE
    repeated_error_count: 0
    needs_deep_trace: false
  gate_reason: Initialization with default routing
  note: Memory system initialized

## Skill Usage Telemetry
- window: all_time
  total_skill_calls: 1
  unique_skills: 1
  calls_by_skill:
    - memory-agent-evolution: 1
  top_skill_ratio: 1.0
  hhi: 1.0
  over_specialized: false
  decision: Normal initialization

## Learning Agenda
- item: Monitor skill diversity as system learns
  owner: memory-system
  due: 2026-05-15

## Route Replay
- replay_id: init-replay-001
  selected_mode: Lite-Mode
  decision_path: "initialization -> default Lite-Mode"
  can_replay: true
"""
    
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    reflect_path.write_text(
        reflect_content.format(timestamp=timestamp)
    )
    print(f"✓ Created {reflect_path}")


def init_memory_system(path: str = None) -> None:
    """Initialize the memory system."""
    if path is None:
        path = "memory"
    
    memory_dir = Path(path)
    memory_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Initializing Memory Agent Evolution System at: {memory_dir.absolute()}")
    print("=" * 60)
    
    create_store_md(memory_dir)
    create_reflect_md(memory_dir)
    
    print("=" * 60)
    print("✓ Memory system initialized successfully!")
    print("\nNext steps:")
    print("  1. Configure gate conditions in your application code")
    print("  2. Set up the runtime closed loop (7 steps)")
    print("  3. Start collecting memory records from your agent runs")
    print("  4. Monitor skill usage in reflect.md")
    print("\nFor detailed documentation, see references/integration-guide.md")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Initialize Memory Agent Evolution System"
    )
    parser.add_argument(
        "--path",
        type=str,
        default="memory",
        help="Path to create memory directory (default: memory)"
    )
    
    args = parser.parse_args()
    init_memory_system(args.path)
