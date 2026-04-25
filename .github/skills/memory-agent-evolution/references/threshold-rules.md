# 触发规则与阈值指南
# Threshold Rules & Trigger Guidelines

**版本:** 1.0.0  
**最后更新:** 2026-04-25

---

## 📋 目录

1. [触发规则概览](#触发规则概览)
2. [信息量监控](#信息量监控)
3. [门控规则](#门控规则)
4. [自动总结触发](#自动总结触发)
5. [记忆更新触发](#记忆更新触发)
6. [规则优先级](#规则优先级)
7. [调试与监控](#调试与监控)
8. [常见触发场景](#常见触发场景)

---

## 触发规则概览

整个系统基于**事件驱动**的触发机制。系统在以下关键点评估规则：

```
┌─────────────┐
│   任务开始   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 1. 门控评估                         │
│    → 升级到 Full-Mode 吗?           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 2. 信息量监控                       │
│    → 触发自动总结吗?                │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 3. 记忆巩固                         │
│    → 更新 L1/L2/L3 吗?              │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│   任务完成   │
└─────────────┘
```

---

## 信息量监控

### 📊 Token 计数规则

系统估计当前上下文的 token 数，决定是否触发自动总结。

#### 计算方法

```python
estimated_tokens = (
    word_count * 1.3 * 0.7 +      # 词数权重（一般 1 词 = 1.3 token）
    char_count * 0.003 * 0.3       # 字符数权重
)
```

#### 标准阈值

| Agent 类型 | 默认阈值 | 触发阈值 | 临界阈值 | 备注 |
|-----------|---------|--------|---------|------|
| **qa_agent** | 5000 | 5000+ | 7500+ | 问答系统 |
| **code_agent** | 8000 | 8000+ | 12000+ | 代码生成（更冗长） |
| **debug_agent** | 6000 | 6000+ | 9000+ | 调试信息较多 |
| **planning_agent** | 7000 | 7000+ | 10500+ | 规划任务复杂 |
| **全局** | 5000 | 5000+ | 7500+ | 默认值 |

**含义：**
- **默认阈值**: 开始考虑总结的 token 数
- **触发阈值**: 自动总结的 token 数
- **临界阈值**: 警告水平（可能性能下降）

### 🔔 触发条件

#### 规则 1: Token 超过阈值

```yaml
name: "token_threshold"
condition: "current_tokens > global_token_threshold"

trigger_check:
  - frequency: "每次上下文更新后"
  - severity: "HIGH"
  - action: "trigger_summary"

example:
  current_tokens: 5200
  threshold: 5000
  result: "✓ 触发自动总结"
```

#### 规则 2: 时间阈值

```yaml
name: "time_based"
condition: "elapsed_time_since_last_summary > 300 seconds"

trigger_check:
  - frequency: "每 30 秒检查一次"
  - severity: "MEDIUM"
  - action: "trigger_summary"

parameters:
  check_interval_seconds: 30
  trigger_duration_seconds: 300    # 5 分钟

example:
  time_since_last_summary: 310
  trigger_duration: 300
  result: "✓ 触发定期总结"
```

#### 规则 3: 语义漂移

```yaml
name: "topic_drift"
condition: "semantic_similarity < 0.5"

description: |
  检测对话主题是否发生突然变化。
  如果新消息与最后 5 条消息的语义相似度 < 0.5，
  表示话题已转变，应该总结前面的内容。

trigger_check:
  - frequency: "每条新消息"
  - severity: "MEDIUM"
  - action: "trigger_summary"

parameters:
  similarity_window: 5             # 对比最后 5 条消息
  similarity_threshold: 0.5

example:
  topic: "Python 编程"
  new_message: "请帮我设计一个神经网络"
  similarity: 0.3
  result: "✓ 触发话题转变总结"
```

#### 规则 4: 内存压力

```yaml
name: "memory_pressure"
condition: "memory_usage_mb > threshold"

description: |
  当内存使用超过限制时，强制总结并压缩。
  这是防止 OOM 的最后一道防线。

trigger_check:
  - frequency: "每秒"
  - severity: "CRITICAL"
  - action: "trigger_summary"

parameters:
  warning_threshold_mb: 50         # 发出警告
  critical_threshold_mb: 80        # 强制总结
  max_size_mb: 100                 # 硬限制

example:
  memory_usage: 75
  critical_threshold: 80
  result: "⚠️  发出警告（升级等待）"
  
  memory_usage: 85
  critical_threshold: 80
  result: "⚠️  CRITICAL：强制总结"
```

---

## 门控规则

### 🚪 升级到 Full-Mode 的条件

系统使用以下规则决定是否从 Lite-Mode 升级到 Full-Mode。

#### 规则优先级

```
优先级 0: Mode Selection (最高优先级)
  ├─ task.priority == HIGH              ✓ 升级
  ├─ error_count >= 2                   ✓ 升级
  └─ debug_mode == true                 ✓ 升级

优先级 1: Complexity Checks
  ├─ context_tokens > threshold         ✓ 升级
  ├─ min_lines > threshold (code)       ✓ 升级
  └─ semantic_complexity > threshold    ✓ 升级

优先级 2: Domain-Specific Checks
  ├─ framework in ["ml", "distributed"] ✓ 升级
  └─ domain_expertise_required          ✓ 升级

优先级 3: Recovery Checks
  ├─ repeated_pattern == true           ✓ 升级
  └─ learning_opportunity               ✓ 升级
```

#### 规则详解

##### 规则 1: 高优先级任务

```python
if task.priority == "HIGH":
    mode = "full"
    reason = "High priority task requires full context"
```

**何时触发：**
- 用户明确标记为高优先级
- 系统关键任务
- 生产环境问题修复

**示例：**
```yaml
task:
  id: "prod_bug_001"
  priority: "HIGH"
  title: "修复数据库连接泄漏"

result:
  mode_selected: "full"
  reason: "High priority task"
  scope: ["L0", "L1", "L2", "L3"]
```

##### 规则 2: 连续错误

```python
if repeated_error_count >= 2:
    mode = "full"
    reason = "Repeated errors detected, escalating for deep analysis"
```

**何时触发：**
- 同一任务连续失败 2 次
- 相似错误在不同任务中重复

**示例：**
```yaml
run_history:
  - run_1: status=FAILED, error="timeout"
  - run_2: status=FAILED, error="timeout"
  
result:
  error_count: 2
  mode_selected: "full"
  reason: "Repeated timeout errors"
```

##### 规则 3: 调试模式

```python
if debug_flag == true:
    mode = "full"
    reason = "Debug mode enabled"
```

**何时触发：**
- 用户启用调试模式（`debug_mode=true`）
- 环境变量 `MEMORY_DEBUG=1`
- 代码中显式调用

**示例：**
```python
# 启用调试模式
agent = Agent(debug_mode=True)
result = agent.run(task)
# → 自动使用 Full-Mode
```

##### 规则 4: 上下文复杂度

```python
if context_tokens > complexity_threshold:
    mode = "full"
    reason = "Context complexity exceeds threshold"
```

**阈值：**
- qa_agent: 3000 tokens
- code_agent: 5000 tokens
- planning_agent: 4000 tokens

##### 规则 5: 代码行数（仅 code_agent）

```python
if code_lines > min_lines_threshold:
    mode = "full"
    reason = "Large code block requires full analysis"
```

**阈值：**
- 100+ 行代码 → Full-Mode
- 涉及多个文件 → Full-Mode

---

## 自动总结触发

### 🎯 触发点

#### 触发点 1: Token 计数

```python
def check_token_threshold(context):
    tokens = estimate_tokens(context)
    threshold = get_threshold(agent_type)
    
    if tokens > threshold:
        trigger_summary("token_exceeded")
        return True
    
    return False
```

**检查频率:** 每条新消息/每秒
**延迟:** ~50ms

#### 触发点 2: 定时检查

```python
def check_time_based(last_summary_time):
    elapsed = now() - last_summary_time
    
    if elapsed > timedelta(seconds=300):
        trigger_summary("time_elapsed")
        return True
    
    return False
```

**检查频率:** 每 30 秒
**间隔:** 5 分钟（可配置）

#### 触发点 3: 话题转变

```python
def check_topic_drift(conversation):
    recent_msgs = conversation[-5:]
    new_msg = conversation[-1]
    
    similarity = calculate_similarity(recent_msgs, new_msg)
    
    if similarity < 0.5:
        trigger_summary("topic_drift")
        return True
    
    return False
```

**检查频率:** 每条新消息
**相似度阈值:** 0.5

#### 触发点 4: 内存压力

```python
def check_memory_pressure(memory_usage_mb):
    if memory_usage_mb > 80:  # 临界值
        trigger_summary("memory_pressure", severity="CRITICAL")
        return True
    
    elif memory_usage_mb > 50:
        log_warning("Memory pressure increasing")
        return False
    
    return False
```

**检查频率:** 每秒
**警告阈值:** 50 MB
**临界阈值:** 80 MB

---

## 记忆更新触发

### 💾 何时更新记忆

#### 触发 1: 定期巩固

```python
if run_count % consolidation_frequency == 0:
    consolidate_memory()
    # 每 10 轮一次
```

| Agent | 频率 | 原因 |
|-------|------|------|
| qa_agent | 每 10 轮 | 问题模式快速变化 |
| code_agent | 每 15 轮 | 代码生成需要更多时间巩固 |
| debug_agent | 每 8 轮 | 错误模式快速演化 |

#### 触发 2: 成功模式识别

```python
if success_count >= 3 and similar_pattern:
    promote_to_l2()
    # 连续 3 次成功 → 推广到 L2 程序层
```

**条件：**
- 同一类型任务成功 3+ 次
- 使用相同策略
- 成功率 > 70%

#### 触发 3: 错误模式识别

```python
if similar_errors >= 2 and needs_insight:
    create_l3_insight()
    # 2 个相似错误 → 创建 L3 洞察
```

**条件：**
- 相同错误出现 2+ 次
- 需要深入分析
- 可能影响未来任务

#### 触发 4: 策略变化

```python
if policy_updated or config_changed:
    log_strategy_change()
    # 记录所有策略变化
```

**包括：**
- 门控条件更改
- 评分权重更新
- 技能追踪配置变化

---

## 规则优先级

### ⚙️ 冲突解决

当多个规则同时满足时，系统按以下优先级执行：

```
优先级 1 (最高):
  CRITICAL memory_pressure    → 强制总结 + 重置
  CRITICAL error              → 升级 Full-Mode + 日志

优先级 2:
  HIGH repeated_error         → 升级 Full-Mode
  HIGH topic_drift           → 触发总结
  HIGH token_exceeded        → 触发总结

优先级 3:
  MEDIUM time_elapsed        → 触发总结（如果不忙）
  MEDIUM learning_opportunity → 记忆更新

优先级 4 (最低):
  LOW info_log              → 只记录日志
  LOW performance_metric    → 更新指标
```

### 🔄 执行顺序

```python
def evaluate_triggers(context):
    # 1. 检查 CRITICAL 规则（立即执行）
    if memory_pressure > CRITICAL:
        trigger_summary("memory_pressure", severity="CRITICAL")
        reset_context()
        return
    
    # 2. 检查 HIGH 规则（按优先级执行）
    if error_count >= 2:
        escalate_to_full_mode("repeated_errors")
    
    if topic_drift_detected():
        trigger_summary("topic_drift")
    
    # 3. 检查 MEDIUM 规则（如果还有资源）
    if not is_busy() and time_elapsed > 300:
        trigger_summary("time_elapsed")
    
    # 4. 记录 LOW 规则（后台任务）
    update_metrics()
```

---

## 调试与监控

### 🔍 查看当前触发状态

```python
from auto_summary import AutoSummarizer

summarizer = AutoSummarizer("memory")

# 获取监控结果
result = summarizer.monitor_context(current_text="...", task_id="qa_001")

print(result)
# 输出:
# {
#   "should_summarize": True,
#   "tokens": 5500,
#   "ratio": 1.1,
#   "threshold": 5000,
#   "reason": "INFO: 信息量超过阈值 (占比 110%)"
# }
```

### 📊 健康检查

```python
health = summarizer.check_memory_health()

print(health)
# 输出:
# {
#   "status": "healthy",
#   "checks": {
#     "store_exists": true,
#     "reflect_exists": true,
#     "size_ok": true,
#     "store_size_mb": 2.3,
#     "reflect_size_mb": 0.8
#   }
# }
```

### 📈 监控指标

追踪这些指标以优化触发规则：

| 指标 | 频率 | 目标 |
|------|------|------|
| 平均触发延迟 | 每轮 | < 50ms |
| 总结成功率 | 每次 | > 95% |
| 压缩率 | 每次 | 40-60% |
| 内存增长率 | 每小时 | < 1 MB/h |
| 规则命中率 | 每小时 | 记录用于优化 |

---

## 常见触发场景

### 场景 1: 长对话

```
时刻    | 事件                    | 触发检查        | 结果
--------|------------------------|----------------|----------
T=0     | 开始对话                | 无              | 继续
T=1000  | 10 条消息 (3000 token) | token check     | Lite 模式
T=1500  | 15 条消息 (4500 token) | token check     | Lite 模式
T=2000  | 20 条消息 (6000 token) | token check     | ✓ 总结
        |                        | time check      | (还未 5 分钟)
        | → 触发摘要              |                |
        | → 保存 L3               |                |
        | → 重置上下文            |                | token=0
T=2100  | 继续对话                | token check     | Lite 模式
```

### 场景 2: 反复错误

```
运行    | 任务         | 状态        | 门控检查        | 结果
--------|-------------|-----------|---------------|---------
Run 1   | 代码生成     | ❌ 失败     | error_count=1  | Lite 模式
Run 2   | 重试         | ❌ 失败     | error_count=2  | ✓ Full 模式
Run 3   | 深入分析     | ✅ 成功     | 使用 L3 洞察    | 成功
```

### 场景 3: 话题转变

```
消息序列:
1. "如何学习 Python?"          [Topic: Python]
2. "推荐一些资源"              [Topic: Python] (相似度 0.9)
3. "请用 Python 写个爬虫"      [Topic: Python] (相似度 0.85)
4. "我想学机器学习"            [Topic: ML] (相似度 0.4) 
   → ✓ 触发话题转变总结（相似度 < 0.5）
```

### 场景 4: 内存警告

```
时刻 | 内存使用 | 状态        | 检查结果
-----|---------|-----------|----------------
T=1  | 30 MB   | ✓ 正常    | OK
T=2  | 45 MB   | ✓ 正常    | OK
T=3  | 55 MB   | ⚠️ 警告   | 发出警告日志
T=4  | 60 MB   | ⚠️ 警告   | 建议总结
T=5  | 75 MB   | 🔴 临界   | 发出 CRITICAL 告警
T=5.5| 85 MB   | 🔴 临界   | → ✓ 强制总结 + 重置
T=6  | 20 MB   | ✓ 正常    | 恢复
```

---

## 配置调优

### 🎛️ 自定义阈值

编辑 `GLOBAL_AGENT_CONFIG.yaml`:

```yaml
global:
  auto_summary:
    global_token_threshold: 5000  # 改成 3000（更激进）
    
    summary_methods:
      - type: "token_count"
        triggers_at: 5000         # 改成 3000
```

### 📝 日志级别

```python
# 查看所有触发的规则
from load_memory import MemoryLoader

loader = MemoryLoader("memory")
reflect = loader.load_reflect(mode="full")

for run in reflect.get("run_evaluation", []):
    print(f"Rule: {run.data['gate_signals']}")
```

---

## 总结

| 规则 | 检查频率 | 严重性 | 执行操作 |
|------|---------|--------|---------|
| Token 阈值 | 实时 | HIGH | 触发总结 |
| 时间阈值 | 30秒 | MEDIUM | 触发总结 |
| 话题漂移 | 实时 | MEDIUM | 触发总结 |
| 内存压力 | 1秒 | CRITICAL | 强制总结 + 重置 |
| 高优先级 | 实时 | HIGH | 升级 Full-Mode |
| 连续错误 | 实时 | HIGH | 升级 Full-Mode |
| 调试模式 | 实时 | HIGH | 升级 Full-Mode |
| 定期巩固 | N轮 | MEDIUM | 更新 L1/L2/L3 |

**推荐开始配置：**
1. 设置 `global_token_threshold` 为你的目标窗口大小
2. 启用 `memory_pressure` 监控
3. 启用 `skill_tracking`
4. 每周检查一次 `health_check()` 结果

准备好了？使用 `AutoSummarizer` 类开始自动总结吧！ 🚀
