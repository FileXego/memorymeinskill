@echo off
REM 本地启动脚本 for Windows
REM 自动检查和安装依赖，然后启动记忆系统

echo.
echo ================================================
echo 🚀 Memory Agent Evolution - Windows 启动脚本
echo ================================================
echo.

REM 检查 Python
echo 🔍 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未找到！请先安装 Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python 已安装

REM 检查和安装依赖
echo 🔍 检查依赖...
python -c "import yaml" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  PyYAML 缺失，正在安装...
    pip install pyyaml -q
    echo ✓ PyYAML 已安装
) else (
    echo ✓ PyYAML 已安装
)

REM 初始化本地环境
echo.
echo 📁 初始化本地环境...
python init_dev.py

REM 运行快速启动脚本
echo.
echo 🚀 启动记忆系统...
python quick_start.py

echo.
echo ================================================
echo ✨ 启动完成！
echo ================================================
echo.
pause
