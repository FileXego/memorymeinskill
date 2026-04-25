#!/usr/bin/env python3
"""
Local Development Initialization Script
初始化本地开发环境
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def main():
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("=" * 60)
    print("🚀 Memory Agent Evolution - 本地开发环境初始化")
    print("=" * 60)
    print()
    
    # 1. 检查目录结构
    print("✓ 检查目录结构...")
    required_dirs = [
        "memory_local",
        "memory_local/qa_agent",
        "memory_local/code_agent", 
        "memory_local/debug_agent",
        "memory_local/planning_agent",
        ".github/skills/memory-agent-evolution/scripts",
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} (缺失)")
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"    → 已创建")
    
    print()
    
    # 2. 检查关键文件
    print("✓ 检查关键文件...")
    required_files = [
        "GLOBAL_AGENT_CONFIG.yaml",
        "config.local.yaml",
        ".github/skills/memory-agent-evolution/scripts/auto_summary.py",
        ".github/skills/memory-agent-evolution/scripts/load_memory.py",
        "README_CN.md",
        "AGENT_INTEGRATION_GUIDE.md",
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ⚠ {file_path} (缺失)")
    
    print()
    
    # 3. 检查 Python 环境
    print("✓ 检查 Python 环境...")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  可执行文件: {sys.executable}")
    
    # 尝试导入必要的模块
    try:
        import yaml
        print("  ✓ PyYAML 已安装")
    except ImportError:
        print("  ✗ PyYAML 未安装 - 运行: pip install pyyaml")
    
    print()
    
    # 4. 检查 Git
    print("✓ 检查 Git 配置...")
    try:
        import subprocess
        result = subprocess.run(
            ["git", "config", "--list"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        if result.returncode == 0:
            print("  ✓ Git 已配置")
            # 检查 .gitignore
            gitignore_path = project_root / ".gitignore"
            if gitignore_path.exists():
                with open(gitignore_path, 'r') as f:
                    content = f.read()
                    if "memory_local/" in content:
                        print("  ✓ .gitignore 已配置 - memory_local/ 被排除")
                    else:
                        print("  ⚠ .gitignore 存在但 memory_local/ 未被排除")
        else:
            print("  ⚠ Git 配置检查失败")
    except Exception as e:
        print(f"  ⚠ Git 检查失败: {e}")
    
    print()
    
    # 5. 生成初始化报告
    print("✓ 初始化报告...")
    report = {
        "timestamp": datetime.now().isoformat(),
        "project_root": str(project_root),
        "python_version": sys.version.split()[0],
        "memory_dirs": {
            "qa_agent": str(project_root / "memory_local/qa_agent"),
            "code_agent": str(project_root / "memory_local/code_agent"),
            "debug_agent": str(project_root / "memory_local/debug_agent"),
            "planning_agent": str(project_root / "memory_local/planning_agent"),
        },
        "config": {
            "local": "config.local.yaml",
            "global": "GLOBAL_AGENT_CONFIG.yaml",
        }
    }
    
    report_path = project_root / ".init_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ 报告已保存: {report_path}")
    
    print()
    
    # 6. 显示下一步
    print("=" * 60)
    print("✨ 初始化完成！")
    print("=" * 60)
    print()
    print("📖 下一步:")
    print()
    print("1️⃣  选择你的角色:")
    print("   - 中文用户? → 打开 README_CN.md")
    print("   - 开发者?   → 打开 AGENT_INTEGRATION_GUIDE.md")
    print("   - 系统管理? → 编辑 config.local.yaml")
    print()
    print("2️⃣  导入记忆系统到你的项目:")
    print("   from scripts.load_memory import MemoryLoader")
    print("   loader = MemoryLoader('memory_local/qa_agent')")
    print("   memories = loader.load_all()")
    print()
    print("3️⃣  自动总结和巩固:")
    print("   from scripts.auto_summary import AutoSummarizer")
    print("   summarizer = AutoSummarizer('memory_local', 'config.local.yaml')")
    print("   result = summarizer.monitor_context(conversation)")
    print()
    print("4️⃣  监控所有 Agent:")
    print("   from AGENT_INTEGRATION_GUIDE import GlobalMonitor")
    print("   monitor = GlobalMonitor()")
    print("   status = monitor.monitor_all()")
    print()
    print("📝 配置文件:")
    print("   - 全局配置: GLOBAL_AGENT_CONFIG.yaml")
    print("   - 本地开发: config.local.yaml")
    print()
    print("🎯 记忆存储位置: memory_local/")
    print("   (已在 .gitignore 中排除)")
    print()
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
