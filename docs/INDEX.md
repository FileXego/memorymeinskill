# 📚 完整文档索引

本文件夹包含 Memory Agent Evolution 的所有详细文档。

---

## 🚀 快速开始

**第一次使用？从这里开始：**

```bash
python quick_start.py
```

然后打开 Claude Code - 系统自动激活！

---

## 📖 文档导航

### 入门文档
- **[README_CN.md](../README_CN.md)** - 完整中文说明（2000+ 行）
- **[LOCAL_RUN_GUIDE.md](../LOCAL_RUN_GUIDE.md)** - 本地运行完整指南

### 集成和开发
- **[AGENT_INTEGRATION_GUIDE.md](../AGENT_INTEGRATION_GUIDE.md)** - 如何在你的项目中集成
- **[CLAUDE_CODE_INTEGRATION.yaml](../CLAUDE_CODE_INTEGRATION.yaml)** - IDE 集成配置

### 配置管理
- **[config.local.yaml](../config.local.yaml)** - 本地开发参数
- **[GLOBAL_AGENT_CONFIG.yaml](../GLOBAL_AGENT_CONFIG.yaml)** - 生产级配置

### 架构规范
- **[SKILL.md](../.github/skills/memory-agent-evolution/SKILL.md)** - 核心架构（900+ 行）
- **[references/four-layer-memory-detail.md](../.github/skills/memory-agent-evolution/references/four-layer-memory-detail.md)** - 四层记忆深度解析
- **[references/threshold-rules.md](../.github/skills/memory-agent-evolution/references/threshold-rules.md)** - 触发规则参考

### 项目信息
- **[PROJECT_COMPLETION_SUMMARY.md](../PROJECT_COMPLETION_SUMMARY.md)** - 第一阶段完成总结
- **[LOCAL_DEPLOYMENT_COMPLETE.md](../LOCAL_DEPLOYMENT_COMPLETE.md)** - 本地部署完成指南
- **[FINAL_COMPLETION_REPORT.txt](../FINAL_COMPLETION_REPORT.txt)** - 最终完成报告

---

## 🎯 按用户类型推荐

### 👨‍💼 想快速开始的人
1. 阅读本页面
2. 运行 `python quick_start.py`
3. 打开 Claude Code
4. 完成！

### 👨‍💻 开发者
1. 阅读 README_CN.md 理解概念
2. 查看 AGENT_INTEGRATION_GUIDE.md 了解集成
3. 运行 quick_start.py
4. 在项目中导入 MemoryLoader
5. 开始使用

### 👨‍⚙️ 系统管理员  
1. 阅读 LOCAL_RUN_GUIDE.md 了解部署
2. 配置 config.local.yaml
3. 为所有项目设置 GLOBAL_AGENT_CONFIG.yaml
4. 配置 CLAUDE_CODE_INTEGRATION.yaml
5. 监控 memory_local/ 使用

### 🔬 研究者
1. 阅读 SKILL.md 了解架构
2. 查看 four-layer-memory-detail.md 理论
3. 查看 threshold-rules.md 了解触发机制
4. 研究 scripts/ 中的实现代码
5. 扩展和改进

---

## 🔍 文件结构

```
memorymeinskill/
├── README.md                           ← 项目首页（简洁）
├── docs/                               ← 完整文档（你在这里）
│   └── 本文件 (INDEX.md)
├── .instructions.md                    ← Claude Code 自动激活 ⚡
├── memory_local/                       ← 私密记忆存储 🔒
├── quick_start.py                      ← 启动脚本
├── auto_memory_service.py              ← 自动保存服务
├── config.local.yaml                   ← 本地配置
├── .github/skills/
│   └── memory-agent-evolution/
│       ├── SKILL.md                    ← 核心架构
│       ├── scripts/
│       │   ├── load_memory.py
│       │   └── auto_summary.py
│       └── references/
│           ├── four-layer-memory-detail.md
│           ├── threshold-rules.md
│           └── integration-guide.md
└── 其他文档和配置文件
```

---

## 💡 常见场景

### 场景 1: "我想快速开始"
```bash
python quick_start.py
# 打开 Claude Code
# 一切自动进行！
```

### 场景 2: "我想在现有项目中集成"
1. 阅读 AGENT_INTEGRATION_GUIDE.md
2. 复制 quick_start.py 中的代码到你的项目
3. 导入 MemoryLoader
4. 完成！

### 场景 3: "我想调整参数"
编辑 `config.local.yaml`，例如：
```yaml
agents:
  code_agent:
    auto_summary:
      token_threshold: 3000  # 更敏感的总结
```

### 场景 4: "我想理解底层原理"
按这个顺序阅读：
1. README_CN.md
2. SKILL.md
3. four-layer-memory-detail.md
4. threshold-rules.md

---

## 🆘 常见问题

| 问题 | 答案 | 文档 |
|------|------|------|
| 如何启动? | `python quick_start.py` | [README.md](../README.md) |
| 如何集成? | 查看 AGENT_INTEGRATION_GUIDE.md | [链接](../AGENT_INTEGRATION_GUIDE.md) |
| 记忆在哪? | `memory_local/` 文件夹 | [LOCAL_RUN_GUIDE.md](../LOCAL_RUN_GUIDE.md) |
| 如何配置? | 编辑 config.local.yaml | [链接](../config.local.yaml) |
| 如何删除记忆? | `rm -rf memory_local` | [LOCAL_RUN_GUIDE.md](../LOCAL_RUN_GUIDE.md) |
| 支持哪些 IDE? | Claude Code, VS Code, Jupyter | [README.md](../README.md) |

---

## 📞 技术支持

遇到问题？

1. **首先检查**: 是否运行了 `python quick_start.py`?
2. **然后查看**: LOCAL_RUN_GUIDE.md 的故障排查部分
3. **最后阅读**: 相关的详细文档

---

## 🎯 快速链接

- 🚀 [快速开始](../README.md#-一分钟快速开始)
- 🔧 [配置参数](../config.local.yaml)
- 💾 [本地存储](../LOCAL_RUN_GUIDE.md#-本地项目结构)
- 📖 [完整中文文档](../README_CN.md)
- 🏗️ [架构规范](../.github/skills/memory-agent-evolution/SKILL.md)

---

**最后更新**: 2026-04-25  
**版本**: 1.0 - 自动激活版  
**状态**: ✅ 生产就绪
