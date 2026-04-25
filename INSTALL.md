# 🚀 Skill 安装指南

## 📍 安装位置

```
C:\Users\hp\.claude\skills\memory-agent-evolution\
```

---

## 📦 需要复制的文件

### 方法 1: 完整安装（推荐）

复制整个 skill 目录和配置：

```bash
# 1. 复制 skill 核心文件
cp -r .github/skills/memory-agent-evolution/ "C:\Users\hp\.claude\skills\memory-agent-evolution"

# 2. 创建配置目录
mkdir -p "C:\Users\hp\.claude\skills\memory-agent-evolution\config"

# 3. 复制配置文件
cp config/default.yaml "C:\Users\hp\.claude\skills\memory-agent-evolution\config\default.yaml"

# 4. 复制核心脚本
cp quick_start.py "C:\Users\hp\.claude\skills\memory-agent-evolution\"
cp auto_memory_service.py "C:\Users\hp\.claude\skills\memory-agent-evolution\"
cp requirements.txt "C:\Users\hp\.claude\skills\memory-agent-evolution\"

# 5. 复制文档（可选）
cp README.md "C:\Users\hp\.claude\skills\memory-agent-evolution\"
cp README_CN.md "C:\Users\hp\.claude\skills\memory-agent-evolution\"
```

### 方法 2: 一键安装脚本

```bash
# 运行安装脚本
./install_skill.sh
```

---

## 📁 安装后的目录结构

```
C:\Users\hp\.claude\skills\memory-agent-evolution\
├── SKILL.md                      ← Skill 定义（必需）⭐
├── README.md                     ← 文档
├── README_CN.md                  ← 中文文档
├── quick_start.py                ← 启动脚本
├── auto_memory_service.py        ← 后台服务
├── requirements.txt              ← 依赖
│
├── config/                       ← 配置
│   └── default.yaml
│
├── scripts/                      ← 核心脚本 ⭐
│   ├── init_memory_system.py
│   ├── load_memory.py
│   └── auto_summary.py
│
├── memory/                       ← 运行时记忆（自动创建）
│   ├── store.md
│   └── reflect.md
│
├── references/                   ← 参考文档
│   ├── integration-guide.md
│   ├── four-layer-memory-detail.md
│   └── threshold-rules.md
│
└── assets/                       ← 模板文件
    └── store-template.md
```

---

## ✅ 验证安装

### 1. 检查 Skill 是否被识别

```bash
# 在 Claude Code 中运行
/memory-agent-evolution
```

如果显示 skill 定义，说明安装成功！

### 2. 测试基本功能

```bash
cd "C:\Users\hp\.claude\skills\memory-agent-evolution"
python quick_start.py
```

应该看到所有 Agent 初始化成功。

---

## 🔧 常见问题

### Q: Skill 不显示在列表中？
**A**: 检查 `SKILL.md` 是否在根目录，且包含正确的 YAML frontmatter。

### Q: 脚本找不到模块？
**A**: 确保 `scripts/` 目录和所有 `.py` 文件都已复制。

### Q: 配置文件读取失败？
**A**: 检查 `config/default.yaml` 是否存在且格式正确。

### Q: 记忆文件在哪？
**A**: 记忆文件会自动创建在 `memory_local/`（如果使用本地模式）或 `memory/`（如果使用标准模式）。

---

## 🎯 推荐：使用本地记忆

为了保持私密性，建议使用 **当前项目目录** 作为记忆存储：

```
d:\memorymeinskill\
└── memory_local/          ← 私密记忆（不同步）
    ├── qa_agent/
    ├── code_agent/
    ├── debug_agent/
    └── planning_agent/
```

Skill 会自动在调用时使用这个目录。

---

## 🔄 更新 Skill

当有新版本时：

```bash
# 1. 备份当前记忆
cp -r memory/ memory_backup/

# 2. 重新复制 skill 文件
cp -r .github/skills/memory-agent-evolution/* "C:\Users\hp\.claude\skills\memory-agent-evolution\"

# 3. 恢复记忆
cp -r memory_backup/* memory/
```

---

**安装完成后，在 Claude Code 中输入 `/memory-agent-evolution` 即可使用！** 🎉
