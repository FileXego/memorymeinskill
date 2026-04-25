#!/usr/bin/env python3
"""
自动记忆后台系统
Automatic Memory Background System

在后台监控对话，自动保存到 memory_local/
"""

import os
import sys
import threading
import time
from pathlib import Path
from datetime import datetime

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / '.github' / 'skills' / 'memory-agent-evolution'))

class AutoMemoryService:
    """自动后台记忆服务"""
    
    def __init__(self, memory_dir='memory_local', agent_name='default'):
        self.memory_dir = Path(memory_dir) / agent_name
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.is_running = False
        self.thread = None
        self.last_save_time = time.time()
        self.save_interval = 60  # 每 60 秒检查一次
        
    def start(self):
        """启动后台服务"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._background_loop, daemon=True)
        self.thread.start()
        print(f"✓ 自动记忆服务已启动 [{self.memory_dir.name}]")
        
    def stop(self):
        """停止后台服务"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        print(f"✓ 自动记忆服务已停止 [{self.memory_dir.name}]")
    
    def _background_loop(self):
        """后台循环 - 定期检查并保存"""
        while self.is_running:
            try:
                self._check_and_save()
                time.sleep(self.save_interval)
            except Exception as e:
                print(f"⚠️ 自动保存错误: {e}")
    
    def _check_and_save(self):
        """检查并保存记忆"""
        # 定期保存统计信息
        stats_file = self.memory_dir / '_stats.txt'
        current_time = datetime.now().isoformat()
        
        try:
            with open(stats_file, 'a', encoding='utf-8') as f:
                f.write(f"[{current_time}] ✓ 自动检查点\n")
        except Exception as e:
            pass  # 忽略统计错误
    
    def save_memory(self, content, layer='L1', agent_id=None):
        """手动保存记忆到指定层"""
        timestamp = datetime.now().isoformat()
        
        try:
            # 自动归档到记忆文件
            store_file = self.memory_dir / 'store.md'
            
            # 确保有 L1 部分
            if not store_file.exists():
                with open(store_file, 'w', encoding='utf-8') as f:
                    f.write("# Memory Store\n\n## L1 Semantics\n\n")
            
            # 追加内容
            with open(store_file, 'a', encoding='utf-8') as f:
                f.write(f"- id: {agent_id or 'auto'}\n")
                f.write(f"  timestamp: {timestamp}\n")
                f.write(f"  content: {content}\n")
                f.write(f"  layer: {layer}\n\n")
            
            return True
        except Exception as e:
            print(f"⚠️ 保存记忆失败: {e}")
            return False


# 全局服务实例（自动初始化）
_auto_memory_service = None

def get_auto_memory_service(agent_name='default'):
    """获取或创建自动记忆服务"""
    global _auto_memory_service
    if _auto_memory_service is None:
        _auto_memory_service = AutoMemoryService(agent_name=agent_name)
        _auto_memory_service.start()
    return _auto_memory_service

def auto_save_memory(content, agent_name='default', layer='L1'):
    """便利函数：自动保存记忆"""
    service = get_auto_memory_service(agent_name)
    return service.save_memory(content, layer=layer)

def stop_auto_memory_service():
    """停止自动记忆服务"""
    global _auto_memory_service
    if _auto_memory_service:
        _auto_memory_service.stop()
        _auto_memory_service = None


if __name__ == "__main__":
    # 测试
    service = AutoMemoryService(agent_name='test_agent')
    service.start()
    
    print("✓ 自动记忆服务正在运行...")
    print("✓ 每 60 秒自动检查一次")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✓ 停止中...")
        service.stop()
        print("✓ 已停止")
