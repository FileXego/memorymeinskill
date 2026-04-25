#!/usr/bin/env python3
"""
快速启动脚本 - 在 Claude Code / Copilot 中使用
一键启动记忆系统，开始使用你的智能 Agent
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / '.github' / 'skills' / 'memory-agent-evolution'))

def quick_start():
    """快速启动记忆系统"""
    print("=" * 70)
    print("🚀 Memory Agent Evolution - 快速启动")
    print("=" * 70)
    print()
    
    try:
        # 1. 导入记忆系统
        print("📦 加载记忆系统...", end=" ")
        from scripts.load_memory import MemoryLoader
        from scripts.auto_summary import AutoSummarizer
        print("✓")
        
        # 2. 初始化 QA Agent
        print("💭 初始化 QA Agent...", end=" ")
        qa_loader = MemoryLoader(str(project_root / 'memory_local' / 'qa_agent'))
        qa_memories = qa_loader.load_store(mode='full')
        print("✓")
        
        # 3. 初始化 Code Agent
        print("💻 初始化 Code Agent...", end=" ")
        code_loader = MemoryLoader(str(project_root / 'memory_local' / 'code_agent'))
        code_memories = code_loader.load_store(mode='full')
        print("✓")
        
        # 4. 初始化 Debug Agent
        print("🐛 初始化 Debug Agent...", end=" ")
        debug_loader = MemoryLoader(str(project_root / 'memory_local' / 'debug_agent'))
        debug_memories = debug_loader.load_store(mode='full')
        print("✓")
        
        # 5. 初始化 Planning Agent
        print("📋 初始化 Planning Agent...", end=" ")
        planning_loader = MemoryLoader(str(project_root / 'memory_local' / 'planning_agent'))
        planning_memories = planning_loader.load_store(mode='full')
        print("✓")
        
        # 6. 初始化自动总结器
        print("🔄 初始化自动总结器...", end=" ")
        summarizer = AutoSummarizer(
            str(project_root / 'memory_local'),
            config_path=str(project_root / 'config' / 'local.yaml')
        )
        print("✓")
        
        # 7. 启动自动内存服务（后台）
        print("⚙️ 启动自动内存服务...", end=" ")
        from auto_memory_service import get_auto_memory_service
        auto_memory = get_auto_memory_service(agent_name='default')
        print("✓")
        
        print()
        print("=" * 70)
        print("✨ 所有系统已启动！")
        print("=" * 70)
        print()
        
        # 显示状态
        print("📊 系统状态:")
        print()
        print("  QA Agent:")
        print(f"    - L0 事件: {len(qa_memories.get('L0', []))} 条")
        print(f"    - L1 语义: {len(qa_memories.get('L1', []))} 条")
        print(f"    - L2 工作流: {len(qa_memories.get('L2', []))} 条")
        print(f"    - L3 洞察: {len(qa_memories.get('L3', []))} 条")
        print()
        print("  Code Agent:")
        print(f"    - 总大小: {get_dir_size(project_root / 'memory_local' / 'code_agent') / 1024:.1f} KB")
        print()
        print("  Debug Agent:")
        print(f"    - 总大小: {get_dir_size(project_root / 'memory_local' / 'debug_agent') / 1024:.1f} KB")
        print()
        print("  Planning Agent:")
        print(f"    - 总大小: {get_dir_size(project_root / 'memory_local' / 'planning_agent') / 1024:.1f} KB")
        print()
        
        print("=" * 70)
        print("🎯 你现在可以使用以下功能:")
        print("=" * 70)
        print()
        print("1️⃣  加载任何 Agent 的记忆:")
        print("   >>> qa_loader.load_store(mode='full')")
        print()
        print("2️⃣  自动总结对话:")
        print("   >>> summarizer.monitor_context(conversation)")
        print()
        print("3️⃣  保存新的洞察到 L3:")
        print("   >>> summarizer.save_to_memory(summary, task_id)")
        print()
        print("4️⃣  查看完整文档:")
        print("   - 中文: README_CN.md")
        print("   - 英文: README.md")
        print("   - 集成: AGENT_INTEGRATION_GUIDE.md")
        print("   - 本地: LOCAL_RUN_GUIDE.md")
        print()
        print("=" * 70)
        print()
        
        # 返回对象供后续使用
        return {
            'qa_loader': qa_loader,
            'code_loader': code_loader,
            'debug_loader': debug_loader,
            'planning_loader': planning_loader,
            'qa_memories': qa_memories,
            'code_memories': code_memories,
            'debug_memories': debug_memories,
            'planning_memories': planning_memories,
            'summarizer': summarizer,
            'auto_memory': auto_memory,
            'project_root': project_root,
        }
        
    except Exception as e:
        print(f"✗ 启动失败: {e}")
        print()
        print("💡 解决方案:")
        print("1. 运行: python init_dev.py")
        print("2. 安装依赖: pip install -r requirements.txt")
        print("3. 查看: LOCAL_RUN_GUIDE.md")
        import traceback
        traceback.print_exc()
        return None

def get_dir_size(path):
    """计算目录大小"""
    total = 0
    for entry in Path(path).rglob('*'):
        if entry.is_file():
            total += entry.stat().st_size
    return total

def interactive_mode(system):
    """交互式模式 - 让用户选择要执行的操作"""
    if not system:
        return
    
    while True:
        print()
        print("选择操作:")
        print("  1. 查看 QA Agent 记忆")
        print("  2. 查看 Code Agent 记忆")
        print("  3. 查看 Debug Agent 记忆")
        print("  4. 查看 Planning Agent 记忆")
        print("  5. 测试自动总结功能")
        print("  6. 保存新的洞察")
        print("  7. 退出")
        print()
        
        choice = input("请选择 (1-7): ").strip()
        
        if choice == '1':
            memories = system['qa_memories']
            print(f"\n📍 QA Agent 记忆总结:")
            print(f"   L0 事件: {len(memories.get('L0', []))} 条")
            print(f"   L1 语义: {len(memories.get('L1', []))} 条")
            print(f"   L2 工作流: {len(memories.get('L2', []))} 条")
            print(f"   L3 洞察: {len(memories.get('L3', []))} 条")
        
        elif choice == '2':
            memories = system['code_memories']
            print(f"\n💻 Code Agent 记忆总结:")
            print(f"   L0 事件: {len(memories.get('L0', []))} 条")
            print(f"   L1 语义: {len(memories.get('L1', []))} 条")
            print(f"   L2 工作流: {len(memories.get('L2', []))} 条")
            print(f"   L3 洞察: {len(memories.get('L3', []))} 条")
        
        elif choice == '3':
            memories = system['debug_memories']
            print(f"\n🐛 Debug Agent 记忆总结:")
            print(f"   L0 事件: {len(memories.get('L0', []))} 条")
            print(f"   L1 语义: {len(memories.get('L1', []))} 条")
            print(f"   L2 工作流: {len(memories.get('L2', []))} 条")
            print(f"   L3 洞察: {len(memories.get('L3', []))} 条")
        
        elif choice == '4':
            memories = system['planning_memories']
            print(f"\n📋 Planning Agent 记忆总结:")
            print(f"   L0 事件: {len(memories.get('L0', []))} 条")
            print(f"   L1 语义: {len(memories.get('L1', []))} 条")
            print(f"   L2 工作流: {len(memories.get('L2', []))} 条")
            print(f"   L3 洞察: {len(memories.get('L3', []))} 条")
        
        elif choice == '5':
            test_text = "这是一个测试对话。用户问了一个关于四层记忆系统的问题。系统回答了基本概念。用户又问了实现细节。系统解释了每一层的用途和工作流程。最后用户表示理解并准备开始使用。"
            result = system['summarizer'].monitor_context(test_text)
            print(f"\n🔄 自动总结测试结果:")
            print(f"   Token 数: {result['token_count']}")
            print(f"   阈值: {result['threshold']}")
            print(f"   应该总结: {result['should_summarize']}")
            print(f"   触发原因: {result.get('reason', 'N/A')}")
        
        elif choice == '6':
            insight = input("\n💭 输入新的洞察: ").strip()
            if insight:
                system['summarizer'].save_to_memory(
                    {'content': insight},
                    task_id='manual_input'
                )
                print("✓ 已保存到 L3 元认知层")
        
        elif choice == '7':
            print("\n👋 再见！")
            break
        
        else:
            print("⚠️  无效的选择，请重新选择。")

if __name__ == "__main__":
    # 快速启动系统
    system = quick_start()
    
    # 如果需要交互式模式，取消下面这行的注释
    # interactive_mode(system)
    
    # 否则直接返回系统对象给 Claude Code 使用
    if system:
        print("💡 在 Claude Code 或 Jupyter 中，你现在可以访问:")
        print()
        print("   qa_loader, code_loader, debug_loader, planning_loader")
        print("   qa_memories, code_memories, debug_memories, planning_memories")
        print("   summarizer")
        print()
        print("例如:")
        print("   >>> memories = summarizer.monitor_context('你的对话文本')")
        print("   >>> result = summarizer.run_consolidation_cycle(conversation)")
        print()
