#!/bin/bash
# Memory Agent Evolution - 一键安装脚本
# 将 skill 安装到 Claude Code 的 skills 目录

echo "=================================="
echo "🚀 Memory Agent Evolution"
echo "   Skill 安装脚本"
echo "=================================="
echo

# 目标目录
SKILL_DIR="/c/Users/hp/.claude/skills/memory-agent-evolution"

# 检查目标目录是否存在
if [ -d "$SKILL_DIR" ]; then
    echo "⚠️  目标目录已存在: $SKILL_DIR"
    read -p "是否覆盖安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 安装已取消"
        exit 1
    fi
    echo "🗑️  删除旧版本..."
    rm -rf "$SKILL_DIR"
fi

# 创建目标目录
echo "📁 创建目标目录..."
mkdir -p "$SKILL_DIR"

# 1. 复制 skill 核心文件（包含 SKILL.md）
echo "📦 复制 Skill 核心文件..."
cp -r .github/skills/memory-agent-evolution/* "$SKILL_DIR/"

# 2. 复制配置文件
echo "⚙️  复制配置文件..."
mkdir -p "$SKILL_DIR/config"
cp config/default.yaml "$SKILL_DIR/config/default.yaml"

# 3. 复制核心脚本
echo "💻 复制核心脚本..."
cp quick_start.py "$SKILL_DIR/"
cp auto_memory_service.py "$SKILL_DIR/"
cp requirements.txt "$SKILL_DIR/"

# 4. 复制文档
echo "📚 复制文档..."
cp README.md "$SKILL_DIR/"
cp README_CN.md "$SKILL_DIR/"
cp STRUCTURE.md "$SKILL_DIR/" 2>/dev/null || true
cp INSTALL.md "$SKILL_DIR/" 2>/dev/null || true

# 5. 创建本地配置模板
echo "📝 创建本地配置模板..."
cat > "$SKILL_DIR/config/local.yaml.example" << 'EOFCONFIG'
# 本地配置示例
# 复制此文件为 local.yaml 并修改你的自定义设置

agents:
  qa_agent:
    auto_summary:
      token_threshold: 5000      # 调整为你需要的值

  code_agent:
    auto_summary:
      token_threshold: 8000
EOFCONFIG

# 检查安装结果
echo
echo "=================================="
echo "✅ 安装完成！"
echo "=================================="
echo
echo "📍 安装位置:"
echo "   $SKILL_DIR"
echo
echo "📊 已安装的文件:"
ls -lh "$SKILL_DIR" | tail -n +2 | awk '{print "   - " $9 " (" $5 ")"}'
echo
echo "📂 目录结构:"
echo "   - scripts/ (核心脚本)"
echo "   - config/ (配置文件)"
echo "   - memory/ (运行时记忆)"
echo "   - references/ (参考文档)"
echo "   - assets/ (模板文件)"
echo
echo "🎯 下一步:"
echo "   1. 在 Claude Code 中输入: /memory-agent-evolution"
echo "   2. 或运行测试: cd '$SKILL_DIR' && python quick_start.py"
echo
echo "📖 查看完整文档: cat '$SKILL_DIR/README_CN.md'"
echo
echo "=================================="
