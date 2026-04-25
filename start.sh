#!/bin/bash
# 本地启动脚本 for macOS/Linux
# 自动检查和安装依赖，然后启动记忆系统

echo ""
echo "================================================"
echo "🚀 Memory Agent Evolution - macOS/Linux 启动脚本"
echo "================================================"
echo ""

# 检查 Python
echo "🔍 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未找到！请先安装 Python 3.8+"
    exit 1
fi
echo "✓ Python 已安装"

# 检查和安装依赖
echo "🔍 检查依赖..."
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "⚠️  PyYAML 缺失，正在安装..."
    pip3 install pyyaml -q
    echo "✓ PyYAML 已安装"
else
    echo "✓ PyYAML 已安装"
fi

# 初始化本地环境
echo ""
echo "📁 初始化本地环境..."
python3 init_dev.py

# 运行快速启动脚本
echo ""
echo "🚀 启动记忆系统..."
python3 quick_start.py

echo ""
echo "================================================"
echo "✨ 启动完成！"
echo "================================================"
echo ""
