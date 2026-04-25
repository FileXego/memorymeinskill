# Memory Agent Evolution Skill - 生产就绪版

**版本:** 1.0.0  
**状态:** ✅ 生产就绪  
**最后更新:** 2026-04-25

---

## 📚 这个 Skill 提供什么

一个**完整、轻量级的记忆架构**，让 AI 智能体能够学习和不断进化。

### 核心特性

- **四层记忆系统** (L0-L3): 事件层、语义层、程序层、元认知层
- **双模式检索**: Lite-Mode 用于日常任务（快速），Full-Mode 用于升级任务（深入）
- **时间知识图谱**: 跨时间和记忆层的链接关系
- **自动技能追踪**: 自动检测过度专业化（技能浓度过高）
- **Markdown 原生存储**: 无需数据库，版本可控
- **完整规范**: 架构蓝图 + 集成代码 + 模板文件

---

## 📁 项目结构

```
memorymeinskill/
├── .github/skills/memory-agent-evolution/
│   ├── SKILL.md                          ← 核心规范 (900 行)
│   ├── memory/                           ← 运行时存储
│   │   ├── store.md                      ← 完整记忆 (L0-L3)
│   │   └── reflect.md                    ← 反思 & 遥测
│   ├── scripts/
│   │   ├── init_memory_system.py         ← 初始化脚本
│   │   ├── load_memory.py                ← 记忆加载器 API
│   │   └── auto_summary.py               ← 自动总结与记忆 ⭐
│   ├── references/
│   │   ├── integration-guide.md          ← 集成指南
│   │   ├── four-layer-memory-detail.md   ← 四层详解
│   │   └── threshold-rules.md            ← 触发规则 ⭐
│   └── assets/
│       └── store-template.md             ← store.md 模板
│
├── README_CN.md                          ← 本文件（中文）
├── README.md                             ← 英文版本
├── MEMORY_INTEGRATION_GUIDE.md           ← 全局集成指南
├── GLOBAL_AGENT_CONFIG.yaml              ← 全局 agent 配置 ⭐
└── SKILL_CHECKLIST.md                    ← 生产清单
```

---

## 🚀 快速开始 (5 分钟)

### 1️⃣ 初始化记忆系统

```bash
cd /path/to/your/project
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py --path ./memory
```

✓ 创建 `memory/store.md` 和 `memory/reflect.md`

### 2️⃣ 在代码中加载记忆

```python
import sys
sys.path.insert(0, '.github/skills/memory-agent-evolution/scripts')
from load_memory import MemoryLoader

loader = MemoryLoader("memory")

# 轻量模式（日常任务，快速）
store = loader.load_store(mode="lite")
reflect = loader.load_reflect(mode="lite")

# 深入模式（调试、复杂推理）
store_full = loader.load_store(mode="full")
reflect_full = loader.load_reflect(mode="full")
```

### 3️⃣ 运行 7 步循环

```python
def agent_turn(task):
    # 1️⃣ 观察
    print(f"处理任务: {task}")
    
    # 2️⃣ 检索（带门控）
    mode = "full" if is_high_priority(task) else "lite"
    store = loader.load_store(mode=mode)
    
    # 3️⃣ 行动/推理
    result = generate_response(task, store)
    
    # 4️⃣-7️⃣ 评估、反思、巩固、演化
    outcome = evaluate(result)
    loader.log_run(task.id, outcome)
    
    return result
```

---

## 💡 核心概念

### 双模式检索

| 维度 | **Lite-Mode** | **Full-Mode** |
|-----|---|---|
| **使用场景** | 日常任务、快速回复 | 调试、复杂推理、高优先级 |
| **读取范围** | L1 + L2 + 快照 | L0 + L1 + L2 + L3（完整） |
| **耗时** | ~50-100ms | ~300-500ms |
| **何时用** | 默认 | task_priority=HIGH 或 错误≥2 次 或 debug_mode |

### 四层记忆

```
L0 事件层    ← 原始数据（对话、工具调用）
  ↓
L1 语义层    ← 稳定事实、偏好、约束
  ↓
L2 程序层    ← 可复用工作流、决策模板
  ↓
L3 元认知层  ← 自我评估、学习目标、校准
```

### 门控条件（何时升级到 Full-Mode）

1. `task_priority == HIGH` （高优先级任务）
2. `repeated_error_count >= 2` （连续错误 ≥2 次）
3. `needs_deep_trace == true` （需要深度追踪）

### 自动技能追踪

系统自动检测过度专业化：

```
top_skill_ratio = max_calls / total_calls
hhi = sum((calls_i / total_calls)²)

过度专业化 = (top_skill_ratio > 0.65) 或 (hhi > 0.45)
```

若触发，系统自动：
- 增加多样性奖励
- 注入非热门技能候选
- 触发学习实验

---

## 🎯 适用场景

### ✅ 非常适合

- 多轮问答，需要上下文学习
- 从失败中学习的调试智能体
- 工作流优化（记住什么有效）
- 研究实验追踪
- 多智能体协作（共享事实层）
- 生产 Copilot（长期学习能力）

### ❌ 不太适合

- 单轮无状态任务
- 严格延迟要求（<50ms）
- 无学习机会的任务
- 隐私敏感（需要遗忘的数据）

---

## 📖 详细文档

| 文档 | 内容 | 阅读时间 |
|-----|------|--------|
| **SKILL.md** | 完整架构规范 | 20-30 分钟 |
| **MEMORY_INTEGRATION_GUIDE.md** | 全局集成 + 配置 | 10-15 分钟 |
| **references/integration-guide.md** | 8+ 集成模式示例 | 15-20 分钟 |
| **references/four-layer-memory-detail.md** | 分层内存深入详解 | 20-25 分钟 |

**推荐阅读顺序：**
1. 本文件的快速开始（5 分钟）
2. MEMORY_INTEGRATION_GUIDE.md 的快速开始（5 分钟）
3. 选择符合你使用场景的集成模式（15 分钟）
4. 根据需要深入阅读（可选）

---

## 🔧 配置参考

### 自定义门控条件

```python
def should_use_full_mode(task):
    return (
        task.priority == "HIGH"
        or error_count >= 2
        or task.debug_mode
    )
```

### 检索评分公式

```python
score = (
    0.3 * relevance +        # 相关性
    0.2 * confidence +       # 置信度
    0.2 * recency +          # 新近性
    0.15 * success_rate +    # 成功率
    0.15 * diversity_bonus   # 多样性奖励
)
```

### 技能追踪配置

自动启用，若要禁用：

```yaml
# 在 reflect.md 中设置
over_specialized: false
decision: manual_tracking
```

详见 **MEMORY_INTEGRATION_GUIDE.md** 的配置部分。

---

## 📊 监控与分析

### 检查内存状态

```bash
python -c "
from .github.skills.memory_agent_evolution.scripts.load_memory import MemoryLoader
loader = MemoryLoader('memory')

store = loader.load_store(mode='lite')
print(f'L1 事实数: {len(store.get(\"L1\", []))}')
print(f'L2 程序数: {len(store.get(\"L2\", []))}')
print(f'过度专业化: {loader.is_over_specialized()}')
"
```

### 分析性能

```python
from scripts.load_memory import MemoryLoader

loader = MemoryLoader('memory')
reflect = loader.load_reflect(mode='full')

runs = reflect.get('run_evaluation', [])
success_rate = sum(1 for r in runs if r.data['outcome'] == 'success') / len(runs)

print(f'成功率: {success_rate * 100:.1f}%')
```

---

## 🧩 集成模式

### 模式 1: 简单智能体

```python
class SimpleAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def ask(self, question):
        store = self.memory.load_store(mode="lite")
        answer = self.generate(question, store)
        self.memory.log_run("ask", "success")
        return answer
```

### 模式 2: 学习型智能体

```python
class LearningAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
        self.run_count = 0
    
    def execute(self, task):
        # 决定模式
        mode = "full" if self.run_count % 10 == 0 else "lite"
        
        store = self.memory.load_store(mode=mode)
        result = self.execute(task, store)
        
        self.memory.log_run(task.id, result.status)
        
        # 每 50 轮演化一次
        if self.run_count % 50 == 0:
            self.evolve()
        
        self.run_count += 1
        return result
```

### 模式 3: 多智能体系统

```python
# 每个智能体有自己的记忆
agents = {
    'planner': Agent('memory/planner'),
    'executor': Agent('memory/executor'),
    'reviewer': Agent('memory/reviewer')
}

# 通过统一事实层共享知识
for agent in agents.values():
    agent.memory.update_shared_facts(shared_knowledge)
```

详见 **MEMORY_INTEGRATION_GUIDE.md** 的 8+ 更多模式。

---

## ⚡ 性能特性

| 操作 | Lite-Mode | Full-Mode |
|------|-----------|-----------|
| 加载 store.md | ~20ms | ~100ms |
| 加载 reflect.md | ~10ms | ~50ms |
| 总检索耗时 | ~50-100ms | ~300-500ms |
| 写入（巩固） | ~100-200ms | ~100-200ms |
| 技能追踪更新 | ~5ms | ~5ms |

**典型内存大小：**
- L0 (100 事件): 50-100 KB
- L1 (50 事实): 20-50 KB
- L2 (20 程序): 80-150 KB
- L3 (10 洞察): 30-60 KB
- **总计: 180-360 KB** 每个完整历史

---

## 🐛 常见问题

| 问题 | 解决方案 |
|------|--------|
| 内存系统未初始化 | 运行: `python scripts/init_memory_system.py --path ./memory` |
| 门控不升级 | 检查代码中的门控条件逻辑 |
| 内存文件过大 | 实施 L0 月度归档；使用 Lite-Mode |
| 技能过度专业化 | 启用 DiversityBonus；注入非热门技能 |
| 性能下降 | 检查文件大小；实施清理；更多使用 Lite-Mode |

详见 **MEMORY_INTEGRATION_GUIDE.md** 的完整故障排除。

---

## 🔄 维护任务

### 📅 月度任务

- [ ] 归档 30 天前的 L0 事件
- [ ] 检查 L2 程序是否已过时
- [ ] 监控内存文件大小（应 <10MB）
- [ ] 分析成功率和错误模式

### 📈 季度任务

- [ ] 审查 L3 元认知洞察
- [ ] 根据数据更新门控条件
- [ ] 推广成功程序到新版本
- [ ] 规划下季度学习议程

### 📊 年度任务

- [ ] 完整系统评估
- [ ] 考虑升级到 V2（学习门控）
- [ ] 归档或删除非常旧的事件

---

## 📝 版本历史

### v1.0.0 (2026-04-25) ✅ 当前版本

- ✅ 完整四层架构 (L0-L3)
- ✅ 双模式检索 (Lite/Full + 规则门控)
- ✅ 时间知识图谱
- ✅ 自动技能追踪
- ✅ Markdown 原生存储
- ✅ 生产初始化脚本
- ✅ 完整文档 + 模板
- ✅ 8+ 集成示例

### v1.1 (规划: Q2 2026)

- 学习门控（用 ML 模型替代规则）
- 程序版本控制 + 回滚
- 成本感知检索评分
- 归档管理工具

### v2.0 (规划: Q3-Q4 2026)

- 多专家系统 (>2 个专家 + 加权路由)
- 向量嵌入支持（可选）
- 图谱可视化
- REST API 远程访问

---

## 🎓 使用示例

### 示例 1: Q&A 智能体

```python
from scripts.load_memory import MemoryLoader

class QAAgent:
    def __init__(self):
        self.loader = MemoryLoader("memory")
    
    def answer(self, question):
        # 检索
        store = self.loader.load_store(mode="lite")
        
        # 根据之前的事实生成答案
        facts = store.get("L1", [])
        answer = self.generate_from_facts(question, facts)
        
        # 记录
        self.loader.log_run(f"qa:{question}", "success")
        
        return answer

# 使用
agent = QAAgent()
print(agent.answer("Python 的优点是什么？"))
```

### 示例 2: 调试智能体

```python
class DebugAgent:
    def __init__(self):
        self.loader = MemoryLoader("memory")
    
    def debug(self, error):
        # 升级到 Full-Mode（调试需要深入信息）
        store_full = self.loader.load_store(mode="full")
        
        # 查找类似的错误历史
        error_patterns = store_full.get("L3", [])
        
        # 推荐修复
        fix = self.suggest_fix(error, error_patterns)
        
        self.loader.log_run(f"debug:{error}", "success")
        
        return fix

# 使用
agent = DebugAgent()
agent.debug("NullReferenceException in line 42")
```

---

## 🤝 集成到现有项目

### 步骤 1: 复制 Skill

```bash
# 假设你已经有了这个仓库
cp -r memorymeinskill/.github/skills/memory-agent-evolution \
      your-project/.github/skills/
```

### 步骤 2: 在你的 Agent 中使用

```python
# your_agent.py
import sys
sys.path.insert(0, './.github/skills/memory-agent-evolution/scripts')
from load_memory import MemoryLoader

class MyAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory")
    
    def run(self, task):
        # ... 你的逻辑
        self.memory.log_run(task.id, outcome)
```

### 步骤 3: 初始化

```bash
cd your-project
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py
```

完成！ 🎉

---

## 📞 快速参考

**你将编辑的文件：**
- 你的代码: 导入 `MemoryLoader`，调用 `.load_store()` 和 `.load_reflect()`
- `memory/store.md`: 自动更新（巩固步骤）
- `memory/reflect.md`: 自动更新（评估步骤）

**你不需要编辑的文件：**
- `SKILL.md`: 仅供参考
- 脚本: 使用但不编辑（除非自定义）
- 模板: 参考用

**关键命令：**

```bash
# 初始化
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py --path ./memory

# 检查状态
python -c "from scripts.load_memory import MemoryLoader; print(MemoryLoader('memory').is_over_specialized())"

# 运行示例
python .github/skills/memory-agent-evolution/scripts/load_memory.py
```

---

## 🎉 现在就开始！

1. **初始化**: `python scripts/init_memory_system.py --path ./memory`
2. **阅读**: 5 分钟 MEMORY_INTEGRATION_GUIDE.md 快速开始
3. **集成**: 15 分钟选择一个集成模式
4. **测试**: 运行你的智能体并观察 memory/ 目录
5. **监控**: 检查 memory/store.md 和 memory/reflect.md 的活动
6. **演化**: 每 50 轮分析并改进

**问题?** 从这些开始：
- `SKILL.md` - "何时使用" 部分
- `MEMORY_INTEGRATION_GUIDE.md` - 快速开始或故障排除
- `references/integration-guide.md` - 集成模式

---

**准备好让你的智能体拥有长期记忆了吗？让我们开始吧！ 🚀**

**中文文档维护**: 与英文版本同步更新
