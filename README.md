# 🧠 Memory Agent Evolution

**自动长期记忆系统 | Auto Long-term Memory**

> 在 Claude Code、GitHub Copilot 或 Codex 中**自动**累积和学习项目知识。

---

## ⚡ 它是如何工作的

```
你在 Claude Code 中写代码
     ↓
系统自动激活 ✨
     ↓
你的对话 → 自动保存到 memory_local/
对话太长 → 自动总结并巩固
     ↓
下次打开 → 恢复上下文并学习历史
```

---

## 🚀 一分钟快速开始

```bash
# 1️⃣  启动系统（首次）
python quick_start.py

# 2️⃣  打开 Claude Code - 系统自动激活 ⚡

# 3️⃣  开始工作 - 一切自动进行
```

完全自动！无需任何配置。

---

## 📂 项目结构

```
memorymeinskill/
├── .instructions.md              ← Claude Code 自动配置 ⚡
├── memory_local/                 ← 私密记忆存储 🔒
│   ├── qa_agent/
│   ├── code_agent/
│   ├── debug_agent/
│   └── planning_agent/
├── .github/skills/               ← 核心 Skill 定义
## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **自动激活** | 打开 Claude Code 即自动启动 ⚡ |
| **自动保存** | 对话自动归档到 `memory_local/` 📁 |
| **自动总结** | 信息过量时自动压缩 🔄 |
| **跨项目学习** | 从历史中吸取经验 🧠 |
| **完全私密** | 所有数据本地存储，永不上传 🔒 |

---

## 💻 在代码中使用

```python
# 自动加载你的项目记忆
from scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory_local/code_agent')
memories = loader.load_store(mode='full')

# 查看你学到的东西
print(f"✓ {len(memories.get('L2', []))} 个代码模式")
print(f"✓ {len(memories.get('L3', []))} 个长期洞察")
```

---

## 📚 文档

| 文档 | 用途 | 适合 |
|------|------|------|
| [快速开始](#-一分钟快速开始) | 5 分钟上手 | 所有人 |
| `docs/README_CN.md` | 中文完整说明 | 中文用户 |
| `docs/AGENT_INTEGRATION_GUIDE.md` | 深度集成指南 | 开发者 |
| `docs/LOCAL_RUN_GUIDE.md` | 本地部署细节 | 系统管理员 |
| `.github/skills/memory-agent-evolution/SKILL.md` | 架构规范 | 研究者 |

---

## ❓ 常见问题

**Q: 记忆会泄露隐私吗？**  
A: 不会。所有记忆存储在 `memory_local/`，完全离线私密。

**Q: 如何重置记忆？**  
A: 运行 `rm -rf memory_local && python quick_start.py`

**Q: 支持哪些 IDE？**  
A: Claude Code ⚡ | GitHub Copilot | VS Code | Jupyter | 任何 Python IDE

**Q: 记忆会变得很大吗？**  
A: 系统自动总结和压缩。平均项目只占 5-50MB。

**Q: 能共享记忆吗？**  
A: 不建议。复制 `memory_local/` 文件夹到新项目即可迁移。

---

## 🔥 立即开始

```bash
# Windows
.\start.bat

# macOS/Linux  
./start.sh

# 或任何平台
python quick_start.py
```

**就这样！** 系统会自动：
1. 检查依赖
2. 初始化环境  
3. 启动所有 Agent
4. 准备好使用

---

## 📊 项目信息

- **版本**: 1.0 - 自动激活版
- **状态**: ✅ 生产就绪
- **更新**: 2026-04-25
- **许可**: MIT

---

## 🌟 下一步

1. **现在**: 运行 `python quick_start.py`
2. **打开**: Claude Code（自动激活）
3. **开始**: 写代码（一切自动）
4. **查看**: 你积累的记忆

**享受自动化的智能助手！** 🚀

---

需要帮助？查看 `docs/` 文件夹了解完整文档。
- **L3 Metacognitive**: Self-evaluation, learning goals, calibration

### Gate Conditions (Escalate to Full-Mode when):

1. `task_priority == HIGH`
2. `repeated_error_count >= 2`
3. `needs_deep_trace == true`

### Skill Usage Tracking

Automatically detects over-specialization:

```
top_skill_ratio = max_calls / total_calls
hhi = sum((calls_i / total_calls)²)
over_specialized = (top_skill_ratio > 0.65) OR (hhi > 0.45)
```

---

## 💡 Use Cases

### ✅ Ideal For:
- Multi-turn Q&A with context learning
- Debugging agents that learn from failures
- Workflow optimization (remembering what works)
- Research tracking across experiments
- Multi-agent coordination (shared facts)
- Long-running copilots that improve over time

### ❌ Not Ideal For:
- Single-turn, stateless tasks
- Real-time systems with strict latency (<50ms required)
- Tasks with no opportunity to learn
- Systems that must forget (privacy-sensitive data)

---

## 🔧 Configuration

### Gate Conditions

Customize in your code:

```python
def should_use_full_mode(task):
    return (
        task.priority == "HIGH"
        or error_count >= 2
        or task.debug_mode
    )
```

### Retrieval Scoring

```python
score = (
    0.3 * relevance +
    0.2 * confidence +
    0.2 * recency +
    0.15 * success_rate +
    0.15 * diversity_bonus
)
```

### Skill Tracking

Automatically enabled. Disable if needed:

```python
# In reflect.md, set:
over_specialized: false  # System won't auto-escalate
decision: manual_tracking
```

See `MEMORY_INTEGRATION_GUIDE.md` for more configurations.

---

## 📊 Monitoring

### Check Memory Status

```bash
# See what's in memory
python -c "
from .github.skills.memory_agent_evolution.scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory')

store = loader.load_store(mode='lite')
print(f'L1 facts: {len(store.get(\"L1\", []))}')
print(f'L2 procedures: {len(store.get(\"L2\", []))}')

print(f'Over-specialized: {loader.is_over_specialized()}')
"
```

### Analyze Performance

```bash
# Get success rate and error breakdown
python -c "
from scripts.load_memory import MemoryLoader

loader = MemoryLoader('memory')
reflect = loader.load_reflect(mode='full')

runs = reflect.get('run_evaluation', [])
success_rate = sum(1 for r in runs if r.data['outcome'] == 'success') / len(runs)

print(f'Success rate: {success_rate * 100:.1f}%')
"
```

---

## 🎓 Integration Patterns

### Pattern 1: Simple Agent

```python
class Agent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def ask(self, question):
        store = self.memory.load_store(mode="lite")
        answer = self.generate(question, store)
        self.memory.log_run("ask", "success")
        return answer
```

### Pattern 2: Learning Agent

```python
class LearningAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def execute(self, task):
        mode = "full" if high_priority else "lite"
        store = self.memory.load_store(mode=mode)
        result = self.execute(task, store)
        self.memory.log_run(task.id, result.status)
        return result
```

### Pattern 3: Multi-Agent System

```python
# Each agent has its own memory
agents = {
    'planner': Agent('memory/planner'),
    'executor': Agent('memory/executor'),
}

# Share knowledge via unified facts layer
```

See `MEMORY_INTEGRATION_GUIDE.md` for 8 more patterns.

---

## 🧹 Maintenance

### Monthly Tasks

- [ ] Archive L0 events older than 30 days
- [ ] Review L2 procedures for obsolescence
- [ ] Check memory file size (should be <10MB for typical use)
- [ ] Analyze success rates and error patterns

### Quarterly Tasks

- [ ] Review L3 metacognitive insights
- [ ] Update gate conditions based on data
- [ ] Promote successful procedures to new versions
- [ ] Plan next quarter's learning agenda

### Annual Tasks

- [ ] Full system evaluation
- [ ] Consider moving to V2 (learned gating, more experts)
- [ ] Archive or delete very old events

---

## ⚡ Performance Characteristics

| Operation | Lite-Mode | Full-Mode |
|-----------|-----------|-----------|
| Load store.md | ~20ms | ~100ms |
| Load reflect.md | ~10ms | ~50ms |
| Total retrieval | ~50-100ms | ~300-500ms |
| Write (consolidation) | ~100-200ms | ~100-200ms |
| Skill tracking update | ~5ms | ~5ms |

**Typical memory sizes:**
- L0 (100 events): 50-100 KB
- L1 (50 facts): 20-50 KB
- L2 (20 procedures): 80-150 KB
- L3 (10 insights): 30-60 KB
- **Total: 180-360 KB** per full history

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Memory not created | Run: `python scripts/init_memory_system.py --path ./memory` |
| Gate not escalating | Check gate condition logic in your code |
| Memory too large | Archive L0 events monthly; implement TTL |
| Skills over-specialized | Enable DiversityBonus; inject non-top-skill candidates |
| Performance degrading | Check file size; implement cleanup; use Lite-Mode more |

See `MEMORY_INTEGRATION_GUIDE.md` for detailed troubleshooting.

---

## 📝 Version History

### v1.0.0 (2026-04-25)
- ✅ Complete four-layer architecture (L0-L3)
- ✅ Dual-mode retrieval (Lite/Full with rule-based gate)
- ✅ Temporal Knowledge Graph backbone
- ✅ Automatic skill usage tracking
- ✅ Markdown-native storage (no database)
- ✅ Production initialization scripts
- ✅ Complete documentation & templates
- ✅ Integration examples

### Roadmap: v1.1 (Q2 2026)
- Learned gate (replaces rule-based with ML model)
- Procedure versioning with rollback
- Cost-aware retrieval scoring
- Archive management utilities

### Roadmap: v2.0 (Q3-Q4 2026)
- Multi-expert system (>2 experts with weighted routing)
- Support for vector embeddings (optional)
- Graph visualization
- REST API for remote access

---

## 📄 License & Attribution

This skill is part of the **Claude Skills** ecosystem.

- Based on: 4-layer memory architecture + MoE routing patterns
- Storage: Markdown YAML (no external dependencies)
- Python dependencies: Only `PyYAML` (for parsing)

---

## 🤝 Contributing

Improvements welcome! Consider:

1. **Bug fixes**: File issues with memory/store.md edge cases
2. **Performance**: Optimize load_memory.py for large history
3. **Documentation**: Add integration examples for your domain
4. **Features**: Custom gate conditions, retrieval scoring strategies

---

## 📞 Quick Reference

**Files You'll Edit:**
- Your code: Import `MemoryLoader`, call `.load_store()` and `.load_reflect()`
- `memory/store.md`: Automatically updated (consolidation step)
- `memory/reflect.md`: Automatically updated (evaluation step)

**Files You Won't Touch:**
- `SKILL.md`: Reference only
- Scripts: Use but don't edit (unless customizing)
- Templates: For reference

**Key Commands:**

```bash
# Initialize
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py --path ./memory

# Check status
python -c "from scripts.load_memory import MemoryLoader; loader = MemoryLoader('memory'); print(loader.is_over_specialized())"

# Analyze
python .github/skills/memory-agent-evolution/scripts/load_memory.py  # Runs example analysis
```

---

## 🎉 Next Steps

1. **Initialize**: `python scripts/init_memory_system.py --path ./memory`
2. **Read**: Check `MEMORY_INTEGRATION_GUIDE.md` Quick Start (5 min)
3. **Integrate**: Pick a pattern from `references/integration-guide.md` (15 min)
4. **Test**: Run your agent with memory enabled
5. **Monitor**: Check `memory/store.md` and `memory/reflect.md` for activity
6. **Evolve**: Every 50 runs, analyze and improve

**Questions?** Start with:
- `SKILL.md` - "When to Use" section
- `MEMORY_INTEGRATION_GUIDE.md` - Quick Start or Troubleshooting
- `references/integration-guide.md` - Integration Patterns

---

**Ready to add memory to your agent? Let's go! 🚀**
