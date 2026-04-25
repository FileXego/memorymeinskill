# 🚀 本地运行指南 - Memory Agent Evolution

> 让你的项目在本地电脑上运行记忆系统，集成到 Claude Code、Copilot、Codex

---

## 📋 前置要求

- ✅ Python 3.8+
- ✅ Git
- ✅ Claude Code / GitHub Copilot / Codex（可选，用于集成）

---

## ⚙️ 一键启动（3 分钟）

### 步骤 1: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 2: 初始化本地环境
```bash
python init_dev.py
```

输出应该显示：
```
✓ 检查目录结构...
✓ 检查关键文件...
✓ 检查 Python 环境...
✓ 检查 Git 配置...
✓ 初始化报告...
✨ 初始化完成！
```

### 步骤 3: 验证 .gitignore 配置
```bash
cat .gitignore | grep memory_local
```

应该显示 `memory_local/` 已被排除。

---

## 📁 本地项目结构

运行初始化后，你的项目看起来像这样：

```
d:\memorymeinskill\
├── memory_local/                    # ← 本地记忆存储（不同步到 GitHub）
│   ├── qa_agent/
│   │   ├── L0_events.md
│   │   ├── L1_semantics.md
│   │   ├── L2_procedures.md
│   │   └── L3_metacognitive.md
│   ├── code_agent/
│   ├── debug_agent/
│   └── planning_agent/
├── .gitignore                       # ← 排除 memory_local/
├── config.local.yaml                # ← 本地开发配置（不同步）
├── GLOBAL_AGENT_CONFIG.yaml         # ← 全局配置（同步）
├── init_dev.py                      # ← 初始化脚本
├── .init_report.json                # ← 初始化报告
└── ... 其他文件
```

**关键点：**
- `memory_local/` ← 本地记忆（私有，不上传 GitHub）
- `config.local.yaml` ← 本地配置（私有，不上传）
- `.gitignore` ← 已配置排除上述文件

---

## 🐍 在 Python 中使用

### 导入记忆系统

```python
import sys
sys.path.insert(0, 'd:/memorymeinskill')

# 加载记忆
from scripts.load_memory import MemoryLoader

loader = MemoryLoader('memory_local/qa_agent')
memories = loader.load_store(mode='full')  # 加载完整的四层记忆

print(f"✓ 已加载 QA Agent 的记忆")
print(f"  L0 事件数: {len(memories.get('L0', []))}")
print(f"  L1 语义数: {len(memories.get('L1', []))}")
print(f"  L2 工作流: {len(memories.get('L2', []))}")
print(f"  L3 洞察数: {len(memories.get('L3', []))}")
```

### 自动总结和巩固

```python
from scripts.auto_summary import AutoSummarizer

# 初始化
summarizer = AutoSummarizer('memory_local', config_path='config.local.yaml')

# 监控对话内容
conversation = """
用户: 什么是四层记忆系统？
AI: 四层记忆系统包括...
用户: 如何在项目中集成？
AI: 首先需要...
"""

# 检查是否需要总结
result = summarizer.monitor_context(
    current_text=conversation,
    task_id="qa_001"
)

print(f"Token 数: {result['token_count']}")
print(f"阈值: {result['threshold']}")
print(f"应该总结? {result['should_summarize']}")

# 如果需要，自动总结并保存
if result["should_summarize"]:
    cycle_result = summarizer.run_consolidation_cycle(conversation)
    print(f"✓ 已自动总结并保存到记忆")
    print(f"  压缩比: {cycle_result['compression_ratio']:.1%}")
```

### 监控所有 Agent

```python
# 需要在 AGENT_INTEGRATION_GUIDE.md 中找到 GlobalMonitor 类
# 或创建自己的监控脚本

import os
import json
from pathlib import Path

def monitor_all_agents():
    memory_base = Path('memory_local')
    agents = {}
    
    for agent_dir in memory_base.iterdir():
        if agent_dir.is_dir():
            store_file = agent_dir / 'store.md'
            if store_file.exists():
                size_kb = store_file.stat().st_size / 1024
                agents[agent_dir.name] = {
                    'memory_size_kb': size_kb,
                    'path': str(agent_dir),
                    'status': 'ok' if size_kb < 500 else 'warning'
                }
    
    return agents

status = monitor_all_agents()
for agent_name, info in status.items():
    print(f"{agent_name}: {info['memory_size_kb']:.1f} KB")
```

---

## 🔌 集成到 Claude Code

### 方式 1: 作为快速命令

在 VS Code 中，创建一个 `.vscode/settings.json`：

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "[python]": {
    "editor.formatOnSave": true
  }
}
```

然后在 Claude Code 中：
```
@memory_qa_agent 请使用记忆系统回答我的问题
```

### 方式 2: 作为 Python 脚本

创建 `run_with_memory.py`：

```python
#!/usr/bin/env python3
"""
运行代码并集成记忆系统
"""

import sys
sys.path.insert(0, '.')

from scripts.load_memory import MemoryLoader
from scripts.auto_summary import AutoSummarizer

def main():
    # 初始化记忆系统
    qa_loader = MemoryLoader('memory_local/qa_agent')
    memories = qa_loader.load_all()
    
    summarizer = AutoSummarizer('memory_local', 'config.local.yaml')
    
    print("✓ 记忆系统已启动")
    print(f"  - 加载了 {sum(len(m) for m in memories.values())} 条记忆")
    
    # 你的代码逻辑
    # ...
    
    print("✓ 完成")

if __name__ == "__main__":
    main()
```

运行它：
```bash
python run_with_memory.py
```

### 方式 3: 在 Jupyter Notebook 中

```python
# 在 Notebook 的第一个 Cell 中执行

import sys
sys.path.insert(0, 'd:/memorymeinskill')

from scripts.load_memory import MemoryLoader
from scripts.auto_summary import AutoSummarizer

# 初始化
loader = MemoryLoader('memory_local/qa_agent')
summarizer = AutoSummarizer('memory_local', 'config.local.yaml')

print("✓ 记忆系统已在 Notebook 中启动")
```

然后在后续的 Cell 中使用：

```python
# Cell 2
memories = loader.load_all()
print(f"✓ 已加载 {len(memories)} 层记忆")
```

---

## 📊 配置文件说明

### config.local.yaml（本地开发专用）

```yaml
global:
  memory_base_dir: "memory_local"  # 本地记忆根目录
  mode: "full"                     # lite 或 full
  debug: true                      # 开启调试

agents:
  qa_agent:
    memory_dir: "memory_local/qa_agent"
    auto_summary:
      enabled: true
      token_threshold: 5000        # 5000 个 Token 时触发总结
      time_threshold_minutes: 5    # 5 分钟时触发总结
```

修改这些参数来调整行为：
- `token_threshold`: 触发总结的 Token 数（增大 = 记忆更密集）
- `time_threshold_minutes`: 触发总结的时间间隔（增大 = 更少打断）
- `enabled`: 关闭自动总结

---

## ✅ 验证一切正常

运行这个检查脚本：

```python
import subprocess
import json
from pathlib import Path

def verify_setup():
    print("验证本地设置...")
    checks = []
    
    # 1. Python
    print("✓ Python 版本", end=" ")
    result = subprocess.run(['python', '--version'], capture_output=True, text=True)
    print(result.stdout.strip())
    checks.append(("Python", True))
    
    # 2. 目录
    print("✓ 目录结构", end=" ")
    required_dirs = [
        'memory_local/qa_agent',
        'memory_local/code_agent',
        'memory_local/debug_agent',
        'memory_local/planning_agent',
    ]
    all_exist = all(Path(d).exists() for d in required_dirs)
    print("✓" if all_exist else "✗")
    checks.append(("目录", all_exist))
    
    # 3. Git 配置
    print("✓ Git 配置", end=" ")
    gitignore_path = Path('.gitignore')
    has_memory_local = 'memory_local/' in gitignore_path.read_text()
    print("✓" if has_memory_local else "✗")
    checks.append(("Git 配置", has_memory_local))
    
    # 4. 初始化报告
    print("✓ 初始化报告", end=" ")
    init_report = Path('.init_report.json')
    has_report = init_report.exists()
    print("✓" if has_report else "✗")
    checks.append(("初始化报告", has_report))
    
    print()
    print("=" * 40)
    all_ok = all(check[1] for check in checks)
    status = "✨ 所有检查通过！" if all_ok else "⚠️  有检查未通过"
    print(status)
    print("=" * 40)
    
    return all_ok

verify_setup()
```

---

## 🆘 常见问题

### Q: 为什么记忆文件不同步到 GitHub？
**A:** 这是设计的。本地记忆文件很大且私人化，不应该上传版本控制。`.gitignore` 已配置排除 `memory_local/`。

### Q: 可以自定义记忆存储位置吗？
**A:** 可以！编辑 `config.local.yaml`：
```yaml
global:
  memory_base_dir: "/custom/path/memory"
```

### Q: 忘记了 Agent 的名称？
**A:** 查看 `memory_local/` 目录：
```bash
ls memory_local/
# 输出: code_agent, debug_agent, planning_agent, qa_agent
```

### Q: 如何重置某个 Agent 的记忆？
**A:** 删除并重新初始化：
```bash
rm -rf memory_local/qa_agent
python init_dev.py
```

### Q: 记忆文件变得太大了怎么办？
**A:** 检查 `auto_summary` 配置，降低 `token_threshold` 值以更频繁地触发总结。

### Q: 在多个项目中使用同一套记忆系统？
**A:** 复制整个 `memory_local/` 目录到新项目，或修改 `config.local.yaml` 的路径。

---

## 🎯 下一步

1. ✅ **已完成**: 本地环境设置
2. ⏭️ **接下来**: 在你的 Agent 代码中集成记忆系统
3. ⏭️ **然后**: 体验自动总结的便利
4. ⏭️ **最后**: 建立跨项目的统一记忆库

---

## 📚 更多资源

- 📖 [中文完整文档](README_CN.md) - 四层记忆系统详细讲解
- 🔧 [Agent 集成指南](AGENT_INTEGRATION_GUIDE.md) - 如何在代码中使用
- 📋 [规则参考](references/threshold-rules.md) - 所有触发规则说明
- 🌐 [Claude Code 集成](CLAUDE_CODE_INTEGRATION.yaml) - VS Code 集成配置
- 📝 [全局配置](GLOBAL_AGENT_CONFIG.yaml) - 生产环境配置

---

## ⚠️ 重要提醒

- ✅ 记住：`memory_local/` 文件夹已被 `.gitignore` 排除，不会同步到 GitHub
- ✅ `config.local.yaml` 也已被排除（本地配置）
- ✅ 版本控制中保留的是全局配置 `GLOBAL_AGENT_CONFIG.yaml`
- ✅ 每个项目/电脑有自己的本地记忆，不互相干扰

---

**祝你使用愉快！** 🎉

有任何问题，参考 README_CN.md 或 AGENT_INTEGRATION_GUIDE.md。
