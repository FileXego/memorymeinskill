#!/usr/bin/env python3
"""
Load Memory Agent Evolution Data

This module provides utilities to read and parse memory records
from store.md and reflect.md files.

Usage:
    from load_memory import MemoryLoader
    
    loader = MemoryLoader("memory")
    store = loader.load_store()
    reflect = loader.load_reflect()
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class MemoryRecord:
    """Parsed memory record."""
    id: str
    data: Dict[str, Any]


class MemoryLoader:
    """Load and parse memory records from Markdown files."""
    
    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.store_path = self.memory_dir / "store.md"
        self.reflect_path = self.memory_dir / "reflect.md"
    
    def load_store(self, mode: str = "full") -> Dict[str, Any]:
        """
        Load store.md records.
        
        Args:
            mode: "lite" for L1/L2 + snapshot, "full" for all layers
        
        Returns:
            Dictionary with L0/L1/L2/L3 records
        """
        if not self.store_path.exists():
            return {}
        
        content = self.store_path.read_text(encoding="utf-8")
        sections = self._parse_sections(content)
        
        result = {}
        
        if mode == "lite":
            # Return only L1, L2, and Lite Snapshot
            if "L1 Semantics" in sections:
                result["L1"] = self._parse_records(sections["L1 Semantics"])
            if "L2 Procedures" in sections:
                result["L2"] = self._parse_records(sections["L2 Procedures"])
            if "Lite Snapshot" in sections:
                result["snapshot"] = self._parse_records(sections["Lite Snapshot"])
        else:  # full
            # Return all layers
            for layer in ["L0 Events", "L1 Semantics", "L2 Procedures", "L3 MetaInsights"]:
                if layer in sections:
                    key = layer.split()[0]  # "L0", "L1", etc.
                    result[key] = self._parse_records(sections[layer])
        
        return result
    
    def load_reflect(self, mode: str = "full") -> Dict[str, Any]:
        """
        Load reflect.md records.
        
        Args:
            mode: "lite" for latest run + summary, "full" for all
        
        Returns:
            Dictionary with evaluation and telemetry records
        """
        if not self.reflect_path.exists():
            return {}
        
        content = self.reflect_path.read_text(encoding="utf-8")
        sections = self._parse_sections(content)
        
        result = {}
        
        if mode == "lite":
            # Return only latest run and telemetry summary
            if "Run Evaluation" in sections:
                runs = self._parse_records(sections["Run Evaluation"])
                result["latest_run"] = runs[-1] if runs else None
            if "Skill Usage Telemetry" in sections:
                telemetry = self._parse_records(sections["Skill Usage Telemetry"])
                result["telemetry"] = telemetry[-1] if telemetry else None
        else:  # full
            for section in ["Run Evaluation", "Skill Usage Telemetry", "Learning Agenda", "Route Replay"]:
                if section in sections:
                    result[section.lower().replace(" ", "_")] = self._parse_records(sections[section])
        
        return result
    
    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse Markdown sections."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)
        
        if current_section and current_content:
            sections[current_section] = "\n".join(current_content).strip()
        
        return sections
    
    def _parse_records(self, section_content: str) -> List[MemoryRecord]:
        """Parse YAML records from section content."""
        records = []
        
        # Split by lines starting with "- id:" or just "-"
        record_blocks = re.split(r'\n(?=- )', section_content.strip())
        
        for block in record_blocks:
            if not block.strip():
                continue
            
            try:
                # Parse YAML
                data = yaml.safe_load(block)
                if isinstance(data, dict) and "id" in data:
                    records.append(MemoryRecord(id=data["id"], data=data))
            except yaml.YAMLError:
                continue
        
        return records
    
    def get_gate_signals(self) -> Dict[str, Any]:
        """Extract gate signals from latest run evaluation."""
        reflect = self.load_reflect(mode="lite")
        
        if not reflect.get("latest_run"):
            return {
                "task_priority": "ROUTINE",
                "repeated_error_count": 0,
                "needs_deep_trace": False
            }
        
        latest_run = reflect["latest_run"].data
        return latest_run.get("gate_signals", {})
    
    def is_over_specialized(self) -> bool:
        """Check if skill usage is over-specialized."""
        reflect = self.load_reflect(mode="lite")
        
        if not reflect.get("telemetry"):
            return False
        
        telemetry = reflect["telemetry"].data
        return telemetry.get("over_specialized", False)


if __name__ == "__main__":
    # Example usage
    loader = MemoryLoader()
    
    print("Loading memory system...")
    print("\n[Lite Mode]")
    store_lite = loader.load_store(mode="lite")
    print(f"L1 records: {len(store_lite.get('L1', []))}")
    print(f"L2 records: {len(store_lite.get('L2', []))}")
    
    print("\n[Full Mode]")
    store_full = loader.load_store(mode="full")
    print(f"L0 events: {len(store_full.get('L0', []))}")
    print(f"L1 facts: {len(store_full.get('L1', []))}")
    print(f"L2 procedures: {len(store_full.get('L2', []))}")
    print(f"L3 insights: {len(store_full.get('L3', []))}")
    
    print("\n[Gate Signals]")
    signals = loader.get_gate_signals()
    print(f"Priority: {signals.get('task_priority')}")
    print(f"Error count: {signals.get('repeated_error_count')}")
    print(f"Over-specialized: {loader.is_over_specialized()}")
