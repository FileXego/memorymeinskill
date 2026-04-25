# 🚀 5 分钟快速使用指南

**自动化系统已启动！** 现在你可以立即开始使用。

---

## ✨ 你现在拥有什么

```
✅ 4 个自动 Agent（QA、Code、Debug、Planning）
✅ 私密记忆存储（memory_local/）
✅ 自动总结和保存系统
✅ Claude Code 自动激活
✅ 完全零配置
```

---

## 💻 在 Claude Code 中使用

### 1️⃣ 获取你的学习记录

```python
# Claude Code 中，自动加载系统后执行：
from scripts.load_memory import MemoryLoader

# 查看 Code Agent 学到的内容
code_agent = MemoryLoader('memory_local/code_agent')
patterns = code_agent.load_store(mode='full')

print(f"✓ 已学习 {len(patterns['L2'])} 个代码模式")
print(f"✓ {len(patterns['L3'])} 个长期洞察")
```

### 2️⃣ 在代码中使用历史记忆

```python
# 查看已解决的类似问题
past_solutions = [item['content'] for item in patterns['L2'] 
                  if 'async' in item.get('tags', [])]

print("✓ 历史解决方案:")
for solution in past_solutions:
    print(f"  - {solution}")
```

### 3️⃣ 保存新发现

```python
from auto_memory_service import auto_save_memory

# 保存新的学习
auto_save_memory(
    content="发现：使用 pydantic 进行类型验证可以减少 50% 的错误",
    agent_name='code_agent',
    layer='L2'  # L1=语义，L2=流程，L3=洞察
)
print("✓ 已保存到长期记忆")
```

---

## 🎯 自动系统是如何工作的

### 自动保存

```python
# 你可以随时保存：
auto_save_memory(
    "SQL 优化: 使用 index 而不是 full scan",
    agent_name='code_agent',
    layer='L2'
)
# ✅ 自动保存到 memory_local/code_agent/store.md
```

### 自动总结

系统监控你的对话。当信息过多时（>5000 个 token），自动：
1. 总结关键信息
2. 保存到 L3（长期洞察）
3. 清理旧信息

### 自动学习

```python
# 每次启动时，系统自动：
# ✅ 加载所有历史记忆
# ✅ 初始化 4 个 Agent
# ✅ 启动后台监控
# ✅ 准备好使用
```

---

## 📚 快速参考

| 任务 | 代码 |
|------|------|
| 查看记忆 | `qa_loader.load_store(mode='full')` |
| 检查大小 | `summarizer.monitor_context(text)` |
| 保存发现 | `auto_save_memory(content, 'agent_name', 'L2')` |
| 执行总结 | `summarizer.run_consolidation_cycle(convo)` |
| 重置记忆 | `rm -rf memory_local && python quick_start.py` |

---

## 🔥 常见场景

### 场景 1: 调试某个错误

```python
# 查看之前遇到过的类似错误
debug_agent = MemoryLoader('memory_local/debug_agent')
past_errors = debug_agent.load_store(mode='full')['L2']

# 过滤相关的错误
similar = [e for e in past_errors 
           if 'timeout' in e.get('content', '')]

print("✓ 相似的历史错误：")
for error in similar:
    print(f"  - {error['content']}")
```

### 场景 2: 找到最佳实践

```python
# 查看 Planning Agent 学到的工作流
planning = MemoryLoader('memory_local/planning_agent')
workflows = planning.load_store(mode='full')['L2']

# 按使用频率排序
top_workflows = sorted(workflows, 
                       key=lambda x: x.get('usage_count', 0),
                       reverse=True)[:5]

print("✓ 常用工作流：")
for wf in top_workflows:
    print(f"  - {wf['content']}")
```

### 场景 3: 总结对话

```python
from scripts.auto_summary import AutoSummarizer

conversation = [
    "用户: 如何优化数据库查询?",
    "助手: 使用索引和查询计划分析",
    "用户: 有什么最佳实践?",
    "助手: 1) 规范化表 2) 使用索引..."
]

summarizer = AutoSummarizer('memory_local')
result = summarizer.monitor_context('\n'.join(conversation))

if result['should_summarize']:
    summary = summarizer.summarize_conversation(conversation)
    summarizer.save_to_memory(summary, 'task-001', 'L3')
    print("✓ 已自动总结并保存")
```

---

## 🎉 现在就试试吧！

```bash
# 1. 启动系统
python quick_start.py

# 2. 打开任何 Python 文件
# （系统自动激活！）

# 3. 导入和使用
from scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory_local/qa_agent')
memories = loader.load_store(mode='full')

# 4. 享受自动化的智能！
print(f"✓ 你有 {sum(len(v) for v in memories.values())} 条记忆")
```

---

## 📖 需要帮助？

| 问题 | 解决方案 |
|------|---------|
| 系统没启动? | `python quick_start.py` |
| 找不到记忆? | 检查 `memory_local/` 文件夹 |
| 想要重置? | `rm -rf memory_local/` |
| 想要配置? | 编辑 `config.local.yaml` |
| 想要详情? | 查看 `docs/INDEX.md` |

---

**享受自动化的长期记忆系统！** 🚀
