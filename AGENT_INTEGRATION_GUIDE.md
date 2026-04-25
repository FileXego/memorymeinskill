# Agent 全局集成指南
# Global Agent Integration Guide

**版本:** 1.0.0  
**最后更新:** 2026-04-25  
**兼容:** memory-agent-evolution >= 1.0.0

---

## 📚 目录

1. [快速集成](#快速集成)
2. [统一配置](#统一配置)
3. [Agent 种类](#agent-种类)
4. [集成检查表](#集成检查表)
5. [全局监控](#全局监控)
6. [故障排查](#故障排查)

---

## 快速集成

### ⏱️ 5 分钟集成

#### 步骤 1: 复制到项目

```bash
# 在你的项目根目录
cp -r memorymeinskill/.github/skills/memory-agent-evolution \
      .github/skills/
```

#### 步骤 2: 创建 Agent 内存目录

```bash
# 为每个 agent 创建内存目录
mkdir -p memory/qa_agent
mkdir -p memory/code_agent
mkdir -p memory/debug_agent
mkdir -p memory/planning_agent

# 初始化
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py \
  --path ./memory/qa_agent

python .github/skills/memory-agent-evolution/scripts/init_memory_system.py \
  --path ./memory/code_agent

# ... 对其他 agent 重复
```

#### 步骤 3: 复制配置文件

```bash
# 从 memorymeinskill 项目复制全局配置
cp memorymeinskill/GLOBAL_AGENT_CONFIG.yaml ./
```

#### 步骤 4: 在代码中集成

```python
# your_qa_agent.py
import sys
sys.path.insert(0, './.github/skills/memory-agent-evolution/scripts')

from load_memory import MemoryLoader
from auto_summary import AutoSummarizer

class QAAgent:
    def __init__(self, agent_name="qa_agent"):
        self.memory = MemoryLoader(f"memory/{agent_name}")
        self.summarizer = AutoSummarizer(f"memory/{agent_name}")
    
    def process_question(self, question):
        # 监控上下文
        monitor_result = self.summarizer.monitor_context(
            current_text=question,
            task_id=f"qa_{int(time.time())}"
        )
        
        if monitor_result["should_summarize"]:
            print("⚠️  触发自动总结")
            # 触发总结...
        
        # 正常处理
        store = self.memory.load_store(mode="lite")
        answer = self.generate_answer(question, store)
        return answer
```

完成！✅

---

## 统一配置

### 📋 配置结构

```yaml
# GLOBAL_AGENT_CONFIG.yaml

agents:
  qa_agent:
    memory_dir: ./memory/qa_agent
    mode: lite
    token_threshold: 5000
    # ...
  
  code_agent:
    memory_dir: ./memory/code_agent
    mode: lite
    token_threshold: 8000
    # ...
```

### 🔧 配置优先级

1. **Agent 级别配置** (最高) - `GLOBAL_AGENT_CONFIG.yaml` 中的 `agents.{agent_name}`
2. **全局配置** (中) - `GLOBAL_AGENT_CONFIG.yaml` 中的 `global`
3. **默认值** (最低) - `auto_summary.py` 和 `load_memory.py` 中硬编码

### 🎛️ 关键配置参数

```yaml
agents:
  my_agent:
    enabled: true                     # 启用此 agent
    memory_dir: ./memory/my_agent     # 内存目录
    mode: lite                        # 默认模式
    
    # 门控条件
    gate_conditions:
      high_priority:
        triggers_full_mode: true
      error_escalation:
        triggers_full_mode: true
        threshold: 2
    
    # 自动总结
    auto_summary:
      enabled: true
      token_threshold: 5000           # 触发阈值
      check_interval: 10              # 检查频率
    
    # 技能追踪
    skill_tracking:
      enabled: true
      window: 50
      over_specialization_threshold: 0.65
```

---

## Agent 种类

### 🤖 预定义 Agent 模板

#### Agent 1: QA Agent (问答)

**适用场景:** 用户提问、知识库查询、FAQ 系统

**配置:**
```yaml
agents:
  qa_agent:
    memory_dir: ./memory/qa_agent
    mode: lite
    auto_summary:
      token_threshold: 5000
      methods: ["extractive", "abstractive"]
    skill_tracking:
      enabled: true
```

**集成代码:**
```python
class QAAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory/qa_agent")
        self.summarizer = AutoSummarizer("memory/qa_agent")
    
    def ask(self, question):
        # 1. 监控
        self.summarizer.monitor_context(current_text=question)
        
        # 2. 检索
        store = self.memory.load_store(mode="lite")
        facts = store.get("L1", [])
        
        # 3. 生成
        answer = self.generate(question, facts)
        
        # 4. 记录
        self.memory.log_run(question, "success")
        
        return answer
```

#### Agent 2: Code Agent (代码生成)

**适用场景:** 代码生成、代码审查、重构建议

**配置:**
```yaml
agents:
  code_agent:
    memory_dir: ./memory/code_agent
    mode: lite
    auto_summary:
      token_threshold: 8000          # 代码更长
      methods: ["extractive", "code_summary"]
    gate_conditions:
      complexity_detection:
        triggers_full_mode: true
        min_lines: 100
```

**集成代码:**
```python
class CodeAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory/code_agent")
    
    def generate_code(self, spec):
        # 检查复杂度
        lines = spec.count('\n')
        mode = "full" if lines > 100 else "lite"
        
        # 检索相似代码
        store = self.memory.load_store(mode=mode)
        
        # 生成
        code = self.generate(spec, store)
        
        # 记录成功的代码模式到 L2
        if self.is_good_code(code):
            self.memory.add_procedure(f"pattern_{spec[:10]}", code)
        
        return code
```

#### Agent 3: Debug Agent (调试)

**适用场景:** 错误诊断、日志分析、问题排查

**配置:**
```yaml
agents:
  debug_agent:
    memory_dir: ./memory/debug_agent
    mode: lite
    auto_summary:
      token_threshold: 6000
      methods: ["error_taxonomy", "pattern_extraction"]
    gate_conditions:
      error_type:
        triggers_full_mode: true
        severe_errors: ["segmentation_fault", "deadlock"]
```

**集成代码:**
```python
class DebugAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory/debug_agent")
        self.error_count = 0
    
    def debug(self, error_log):
        # 计数
        self.error_count += 1
        
        # 升级检查
        mode = "full" if self.error_count >= 2 else "lite"
        
        # 检索错误模式
        store = self.memory.load_store(mode=mode)
        patterns = store.get("L2", [])
        
        # 诊断
        diagnosis = self.analyze(error_log, patterns)
        
        # 如果是新错误，创建洞察
        if not self.is_known_error(error_log):
            self.memory.add_metacognitive_insight(
                f"error_pattern_{error_log[:20]}", 
                diagnosis
            )
        
        return diagnosis
```

#### Agent 4: Planning Agent (规划)

**适用场景:** 任务分解、工作流设计、依赖管理

**配置:**
```yaml
agents:
  planning_agent:
    memory_dir: ./memory/planning_agent
    mode: lite
    auto_summary:
      token_threshold: 7000
      methods: ["task_decomposition", "dependency_graph"]
```

**集成代码:**
```python
class PlanningAgent:
    def __init__(self):
        self.memory = MemoryLoader("memory/planning_agent")
    
    def plan(self, large_task):
        # 检查复杂度（子任务数）
        subtasks = self.decompose(large_task)
        mode = "full" if len(subtasks) > 5 else "lite"
        
        # 检索相似计划
        store = self.memory.load_store(mode=mode)
        
        # 制定计划
        plan = self.create_plan(large_task, subtasks, store)
        
        # 保存成功的计划结构
        if self.is_viable_plan(plan):
            self.memory.add_procedure(
                f"plan_template_{len(subtasks)}_tasks",
                plan
            )
        
        return plan
```

---

## 集成检查表

### ✅ 集成前检查

- [ ] `memory-agent-evolution` Skill 已复制到 `.github/skills/`
- [ ] `GLOBAL_AGENT_CONFIG.yaml` 已复制到项目根目录
- [ ] `memory/` 目录为每个 agent 初始化完成
- [ ] `init_memory_system.py` 已为所有 agent 运行

### ✅ 代码集成检查

- [ ] 所有 agent 导入 `MemoryLoader`
- [ ] 所有 agent 导入 `AutoSummarizer`
- [ ] 每个 agent 初始化 `self.memory = MemoryLoader(...)`
- [ ] 每个 agent 初始化 `self.summarizer = AutoSummarizer(...)`
- [ ] 所有 agent 调用 `monitor_context()` 检查信息量
- [ ] 所有 agent 调用 `load_store()` 进行检索
- [ ] 所有 agent 调用 `log_run()` 记录结果

### ✅ 配置集成检查

- [ ] `GLOBAL_AGENT_CONFIG.yaml` 包含所有 agent 配置
- [ ] 每个 agent 的 `memory_dir` 指向正确目录
- [ ] `token_threshold` 根据 agent 类型设置
- [ ] `auto_summary.enabled` 设置为 `true`
- [ ] `skill_tracking.enabled` 设置为 `true`

### ✅ 运行时检查

- [ ] 启动 agent 系统
- [ ] 检查 `memory/*/store.md` 文件是否存在
- [ ] 检查 `memory/*/reflect.md` 文件是否存在
- [ ] 监控一个 agent，确认信息量被追踪
- [ ] 手动触发超过阈值的信息量，确认总结被触发
- [ ] 检查 `L1`、`L2`、`L3` 记录是否被创建

### ✅ 部署前检查

- [ ] 内存目录大小 < 100 MB
- [ ] 没有错误日志
- [ ] 成功率 > 90%
- [ ] 平均延迟 < 500ms
- [ ] 文档已更新（README 指向集成指南）

---

## 全局监控

### 📊 监控所有 Agent

```python
# monitor_all_agents.py

from pathlib import Path
from load_memory import MemoryLoader
from auto_summary import AutoSummarizer

class GlobalMonitor:
    def __init__(self, memory_root="memory"):
        self.memory_root = Path(memory_root)
        self.agents = {}
        self._init_agents()
    
    def _init_agents(self):
        """初始化所有 agent 的监控"""
        for agent_dir in self.memory_root.iterdir():
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                self.agents[agent_name] = {
                    "loader": MemoryLoader(str(agent_dir)),
                    "summarizer": AutoSummarizer(str(agent_dir))
                }
    
    def monitor_all(self):
        """监控所有 agent 的健康状态"""
        print("\n" + "="*60)
        print("🔍 GLOBAL AGENT MONITORING")
        print("="*60 + "\n")
        
        for agent_name, tools in self.agents.items():
            health = tools["summarizer"].check_memory_health()
            
            print(f"📊 {agent_name}")
            print(f"   Status: {health['status']}")
            print(f"   Store size: {health['checks'].get('store_size_mb', 0):.1f} MB")
            print(f"   Reflect size: {health['checks'].get('reflect_size_mb', 0):.1f} MB")
            
            if not health['checks'].get('size_ok'):
                print(f"   ⚠️  SIZE WARNING!")
            
            print()
    
    def get_overall_status(self):
        """获取全局状态"""
        statuses = []
        total_size = 0
        
        for agent_name, tools in self.agents.items():
            health = tools["summarizer"].check_memory_health()
            statuses.append(health['status'])
            total_size += health['checks'].get('store_size_mb', 0)
            total_size += health['checks'].get('reflect_size_mb', 0)
        
        # 判断全局状态
        if "degraded" in statuses:
            global_status = "degraded"
        elif "warning" in statuses:
            global_status = "warning"
        else:
            global_status = "healthy"
        
        return {
            "status": global_status,
            "agents_count": len(self.agents),
            "total_size_mb": total_size,
            "agent_statuses": {name: self.agents[name] for name in self.agents}
        }

# 使用
monitor = GlobalMonitor()
monitor.monitor_all()
status = monitor.get_overall_status()
print(f"Overall: {status['status']} | Total Size: {status['total_size_mb']:.1f} MB")
```

### 📈 收集全局指标

```python
# collect_metrics.py

import json
from datetime import datetime
from pathlib import Path

class MetricsCollector:
    def __init__(self, memory_root="memory"):
        self.memory_root = Path(memory_root)
        self.metrics_file = Path("memory_metrics.json")
    
    def collect(self):
        """收集所有 agent 的指标"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "agents": {}
        }
        
        for agent_dir in self.memory_root.iterdir():
            if agent_dir.is_dir():
                agent_name = agent_dir.name
                store_path = agent_dir / "store.md"
                reflect_path = agent_dir / "reflect.md"
                
                metrics["agents"][agent_name] = {
                    "store_lines": self._count_lines(store_path),
                    "reflect_lines": self._count_lines(reflect_path),
                    "store_size_mb": store_path.stat().st_size / (1024*1024) if store_path.exists() else 0,
                    "reflect_size_mb": reflect_path.stat().st_size / (1024*1024) if reflect_path.exists() else 0
                }
        
        # 保存到文件
        with open(self.metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return metrics
    
    @staticmethod
    def _count_lines(filepath):
        """计算文件行数"""
        if not filepath.exists():
            return 0
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())

# 定期收集（可放在 cron 或定时器中）
collector = MetricsCollector()
metrics = collector.collect()
```

---

## 故障排查

### 🔧 常见问题

#### Q1: "ModuleNotFoundError: No module named 'load_memory'"

**原因:** 路径未正确设置

**解决:**
```python
import sys
# 添加到 sys.path（必须在 import 前）
sys.path.insert(0, './.github/skills/memory-agent-evolution/scripts')

from load_memory import MemoryLoader
```

#### Q2: "FileNotFoundError: memory/qa_agent/store.md"

**原因:** 内存目录未初始化

**解决:**
```bash
python .github/skills/memory-agent-evolution/scripts/init_memory_system.py \
  --path ./memory/qa_agent
```

#### Q3: Agent 总是使用 Lite-Mode

**原因:** 门控条件未正确配置或触发

**调试:**
```python
from load_memory import MemoryLoader

loader = MemoryLoader("memory/qa_agent")

# 检查最后一次运行的门控信号
reflect = loader.load_reflect(mode="full")
last_run = reflect["run_evaluation"][-1] if reflect["run_evaluation"] else None

if last_run:
    print(f"Gate signals: {last_run.get('gate_signals')}")
    print(f"Route mode: {last_run.get('route_mode')}")
```

#### Q4: 内存文件增长过快

**原因:** L0 事件未清理，或总结频率过低

**解决:**
1. 增加自动总结频率
2. 启用 L0 月度归档
3. 检查记忆巩固是否在运行

```bash
# 手动触发巩固
python -c "
from auto_summary import AutoSummarizer

summarizer = AutoSummarizer('memory/qa_agent')
# 模拟对话
conversation = [
    {'role': 'user', 'content': 'test'},
    {'role': 'assistant', 'content': 'response'}
]
result = summarizer.run_consolidation_cycle(conversation, 'cleanup')
print(result)
"
```

#### Q5: Token 计数不准确

**原因:** 估计方法不匹配实际模型

**解决:** 集成真实 tokenizer

```python
# 使用 tiktoken（OpenAI 的 tokenizer）
import tiktoken

def accurate_token_count(text):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    return len(tokens)

# 替换 AutoSummarizer 中的估计方法
summarizer.estimate_tokens = accurate_token_count
```

### 📋 诊断命令

```bash
# 检查所有 agent 的内存文件
find memory -name "store.md" -exec wc -l {} +

# 检查内存文件大小
du -sh memory/*/

# 检查最新的运行记录
tail -20 memory/qa_agent/reflect.md

# 统计 L1 事实数
grep "^- \*\*id\*\*:" memory/qa_agent/store.md | wc -l

# 检查 L3 洞察
grep "## L3 MetaInsight" memory/qa_agent/store.md | wc -l
```

---

## 最佳实践

### ✅ DO

- ✅ 为每个 agent 类型创建独立的内存目录
- ✅ 定期检查 `memory_health()`
- ✅ 监控 `token_threshold` 并根据需要调整
- ✅ 启用 `skill_tracking` 检测过度专业化
- ✅ 备份 `memory/*/store.md` 和 `reflect.md`
- ✅ 使用全局配置管理所有 agent

### ❌ DON'T

- ❌ 手动编辑 `store.md` 或 `reflect.md`（应让系统自动更新）
- ❌ 对所有 agent 使用相同的 `token_threshold`（代码 agent 需要更高）
- ❌ 禁用 `auto_summary`（会导致内存增长）
- ❌ 在 `memory/` 目录中存储其他文件
- ❌ 跳过健康检查（可预防问题）

---

## 总结

| 步骤 | 时间 | 难度 |
|------|------|------|
| 1. 复制 Skill | 1 min | ⭐ |
| 2. 初始化内存目录 | 2 min | ⭐ |
| 3. 集成 Agent 代码 | 10 min | ⭐⭐ |
| 4. 配置全局参数 | 5 min | ⭐⭐ |
| 5. 部署与监控 | 5 min | ⭐ |

**总计: 23 分钟即可完成全局集成** ✅

准备开始？

1. 按上面的 5 分钟快速集成开始
2. 使用提供的 Agent 模板扩展
3. 运行 `GlobalMonitor` 检查健康状态
4. 根据需要调整配置

有问题？查看 [故障排查](#故障排查) 部分。

祝你使用愉快！ 🚀
