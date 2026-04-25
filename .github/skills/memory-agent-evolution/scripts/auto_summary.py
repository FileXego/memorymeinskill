#!/usr/bin/env python3
"""
Auto-Summary Module for Memory-Agent-Evolution Skill

自动总结与记忆巩固机制
自动检测信息量，超过阈值时：
1. 触发摘要生成
2. 提取关键信息到 L3（元认知）
3. 压缩上下文
4. 保存到 store.md 和 reflect.md
5. 清空当前上下文并继续

Usage:
    from auto_summary import AutoSummarizer
    
    summarizer = AutoSummarizer("memory", config_path="GLOBAL_AGENT_CONFIG.yaml")
    
    # 监控信息量
    summarizer.monitor_context(current_tokens=5500, task_id="qa_001")
    
    # 手动触发总结
    conversation_history = [...]
    summary = summarizer.summarize_conversation(conversation_history)
    summarizer.save_to_memory(summary)

Version: 1.0.0
Last Updated: 2026-04-25
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import re


class AutoSummarizer:
    """自动总结与记忆巩固引擎"""
    
    def __init__(self, memory_dir: str = "memory", config_path: Optional[str] = None):
        """
        初始化自动总结器
        
        Args:
            memory_dir: 内存目录路径
            config_path: 全局配置文件路径（可选）
        """
        self.memory_dir = Path(memory_dir)
        self.store_path = self.memory_dir / "store.md"
        self.reflect_path = self.memory_dir / "reflect.md"
        
        self.config = self._load_config(config_path) if config_path else self._default_config()
        
        # 运行时统计
        self.context_tokens = 0
        self.run_count = 0
        self.last_summary_time = datetime.now()
        self.last_summary_tokens = 0
    
    def _default_config(self) -> Dict[str, Any]:
        """默认配置"""
        return {
            "auto_summary": {
                "global_token_threshold": 5000,
                "summary_methods": ["extractive", "abstractive"],
                "post_summary_actions": [
                    "save_to_memory",
                    "compress_tokens",
                    "update_reflect",
                    "reset_context"
                ]
            },
            "memory_policy": {
                "l0_retention_days": 30,
                "l1_confidence_threshold": 0.6,
                "l2_success_threshold": 0.7,
                "l3_update_frequency": 50
            },
            "performance": {
                "cache_enabled": True,
                "cache_ttl_seconds": 300,
                "max_memory_size_mb": 100
            }
        }
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载 YAML 配置文件"""
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config or self._default_config()
        except ImportError:
            print("⚠️  PyYAML not installed. Using default config.")
            return self._default_config()
        except FileNotFoundError:
            print(f"⚠️  Config file {config_path} not found. Using default config.")
            return self._default_config()
    
    def estimate_tokens(self, text: str) -> int:
        """
        估计文本的 token 数（简单实现）
        
        实际使用时可替换为真实 tokenizer（如 tiktoken）
        
        Args:
            text: 输入文本
            
        Returns:
            估计的 token 数
        """
        # 简单启发式：平均每个单词 1.3 个 token，加上标点符号
        words = len(text.split())
        chars = len(text)
        
        # 混合估计：词数权重 0.7，字符权重 0.3
        estimated = int(words * 1.3 * 0.7 + chars * 0.003 * 0.3)
        
        return max(estimated, 1)
    
    def monitor_context(self, 
                       current_text: Optional[str] = None,
                       token_count: Optional[int] = None,
                       task_id: str = "unknown") -> Dict[str, Any]:
        """
        监控当前上下文信息量
        
        Args:
            current_text: 当前上下文文本
            token_count: 显式指定的 token 数（如果不提供 text）
            task_id: 任务 ID
            
        Returns:
            监控结果 {
                'should_summarize': bool,
                'tokens': int,
                'ratio': float,
                'reason': str
            }
        """
        # 计算 token 数
        if current_text:
            tokens = self.estimate_tokens(current_text)
        else:
            tokens = token_count or self.context_tokens
        
        self.context_tokens = tokens
        
        # 获取阈值
        threshold = self.config.get("auto_summary", {}).get("global_token_threshold", 5000)
        ratio = tokens / threshold if threshold > 0 else 0
        
        should_summarize = tokens > threshold
        reason = ""
        
        if should_summarize:
            if tokens > threshold * 1.5:
                reason = "CRITICAL: 信息量超过阈值 150%"
            else:
                reason = f"INFO: 信息量超过阈值 (占比 {ratio:.1%})"
        
        self.run_count += 1
        
        return {
            "should_summarize": should_summarize,
            "tokens": tokens,
            "ratio": ratio,
            "threshold": threshold,
            "reason": reason,
            "run_count": self.run_count,
            "task_id": task_id
        }
    
    def summarize_conversation(self, 
                              conversation: List[Dict[str, str]],
                              method: str = "extractive") -> Dict[str, Any]:
        """
        生成对话摘要
        
        Args:
            conversation: 对话历史 [{"role": "user", "content": "..."}, ...]
            method: 摘要方法 ("extractive" 或 "abstractive")
            
        Returns:
            摘要数据 {
                'summary': str,
                'key_points': [str],
                'method': str,
                'tokens_before': int,
                'tokens_after': int,
                'compression_ratio': float
            }
        """
        if method == "extractive":
            return self._extractive_summary(conversation)
        elif method == "abstractive":
            return self._abstractive_summary(conversation)
        else:
            return self._extractive_summary(conversation)
    
    def _extractive_summary(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        提取式摘要：选择最重要的句子
        
        策略：
        1. 提取所有用户消息（通常最重要）
        2. 保留前 3 个和最后 2 个助手响应
        3. 按时间顺序重新排列
        """
        user_messages = [
            msg.get("content", "")
            for msg in conversation
            if msg.get("role") == "user"
        ]
        
        assistant_messages = [
            msg.get("content", "")
            for msg in conversation
            if msg.get("role") == "assistant"
        ]
        
        # 保留关键响应
        kept_assistant = assistant_messages[:3] + assistant_messages[-2:]
        
        original_text = "\n".join([
            f"用户: {msg}" for msg in user_messages
        ] + [
            f"助手: {msg}" for msg in kept_assistant
        ])
        
        # 提取最重要的要点（使用句号分割）
        key_points = [
            sentence.strip()
            for sentence in re.split(r'[。!?；]', original_text)
            if len(sentence.strip()) > 20
        ][:5]  # 最多 5 个要点
        
        original_tokens = self.estimate_tokens(original_text)
        summary_tokens = original_tokens // 2  # 估计摘要为原始的 50%
        
        return {
            "summary": original_text,
            "key_points": key_points,
            "method": "extractive",
            "tokens_before": original_tokens,
            "tokens_after": summary_tokens,
            "compression_ratio": summary_tokens / original_tokens if original_tokens > 0 else 0
        }
    
    def _abstractive_summary(self, conversation: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        抽象式摘要：生成新的摘要文本
        
        注意：这是一个简化实现，不使用 LLM
        实际使用时应集成 summarization 模型
        """
        # 构建聊天记录
        text_parts = []
        for msg in conversation:
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "").strip()
            if content:
                text_parts.append(f"[{role}] {content[:100]}")  # 截断到 100 字
        
        full_text = "\n".join(text_parts)
        
        # 简化实现：列出主题
        key_points = self._extract_topics(full_text)
        
        abstract = f"本次交互包含以下主题: {', '.join(key_points[:3])}"
        
        original_tokens = self.estimate_tokens(full_text)
        summary_tokens = self.estimate_tokens(abstract)
        
        return {
            "summary": abstract,
            "key_points": key_points,
            "method": "abstractive",
            "tokens_before": original_tokens,
            "tokens_after": summary_tokens,
            "compression_ratio": summary_tokens / original_tokens if original_tokens > 0 else 0
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """从文本提取主题（简化实现）"""
        # 简单的关键词提取（实际应使用 NLP）
        keywords = [
            "问题", "代码", "错误", "调试", "优化", "设计",
            "算法", "数据", "性能", "安全", "测试", "部署",
            "用户", "功能", "需求", "文档", "架构"
        ]
        
        found_topics = [kw for kw in keywords if kw in text]
        
        return found_topics[:5] if found_topics else ["一般讨论"]
    
    def save_to_memory(self, 
                      summary: Dict[str, Any],
                      task_id: str = "unknown",
                      category: str = "consolidated") -> Dict[str, Any]:
        """
        保存摘要到记忆系统
        
        Args:
            summary: 摘要数据（来自 summarize_conversation）
            task_id: 任务 ID
            category: 分类 ("consolidated", "error_analysis", "pattern", ...)
            
        Returns:
            保存结果 {
                'saved': bool,
                'l3_id': str,
                'timestamp': str,
                'size': int
            }
        """
        if not self.store_path.exists():
            return {
                "saved": False,
                "error": f"store.md not found at {self.store_path}"
            }
        
        # 生成 L3 记录
        l3_id = f"l3_{task_id}_{int(time.time())}"
        timestamp = datetime.now().isoformat()
        
        l3_record = {
            "id": l3_id,
            "category": category,
            "timestamp": timestamp,
            "content": summary.get("summary", ""),
            "key_points": summary.get("key_points", []),
            "compression_ratio": summary.get("compression_ratio", 0),
            "method": summary.get("method", "unknown"),
            "tokens_before": summary.get("tokens_before", 0),
            "tokens_after": summary.get("tokens_after", 0)
        }
        
        # 追加到 store.md
        try:
            with open(self.store_path, 'a', encoding='utf-8') as f:
                f.write("\n\n")
                f.write(f"## L3 MetaInsight - {l3_id}\n\n")
                f.write(f"- **category**: {category}\n")
                f.write(f"- **timestamp**: {timestamp}\n")
                f.write(f"- **summary**: {summary.get('summary', '')[:200]}...\n")
                f.write(f"- **compression**: {summary.get('compression_ratio', 0):.1%}\n")
                f.write(f"- **method**: {summary.get('method', 'unknown')}\n")
            
            # 更新 reflect.md 的遥测
            self._update_reflect_telemetry(l3_id, summary)
            
            return {
                "saved": True,
                "l3_id": l3_id,
                "timestamp": timestamp,
                "size": len(str(l3_record))
            }
        
        except IOError as e:
            return {
                "saved": False,
                "error": str(e)
            }
    
    def _update_reflect_telemetry(self, l3_id: str, summary: Dict[str, Any]) -> None:
        """更新 reflect.md 中的遥测数据"""
        if not self.reflect_path.exists():
            return
        
        try:
            with open(self.reflect_path, 'r', encoding='utf-8') as f:
                reflect_content = f.read()
            
            # 简单追加遥测记录
            telemetry_entry = (
                f"\n- **consolidation** run #{self.run_count} | "
                f"L3:{l3_id} | "
                f"ratio:{summary.get('compression_ratio', 0):.1%} | "
                f"method:{summary.get('method', 'unknown')} | "
                f"time:{datetime.now().isoformat()}"
            )
            
            with open(self.reflect_path, 'a', encoding='utf-8') as f:
                f.write(telemetry_entry)
        
        except Exception as e:
            print(f"⚠️  Failed to update reflect.md: {e}")
    
    def reset_context(self) -> Dict[str, Any]:
        """
        重置上下文窗口
        
        Returns:
            重置结果 {
                'context_cleared': bool,
                'previous_tokens': int,
                'new_tokens': int
            }
        """
        previous_tokens = self.context_tokens
        
        self.context_tokens = 0
        self.last_summary_time = datetime.now()
        self.last_summary_tokens = 0
        
        return {
            "context_cleared": True,
            "previous_tokens": previous_tokens,
            "new_tokens": self.context_tokens,
            "reset_time": datetime.now().isoformat()
        }
    
    def check_memory_health(self) -> Dict[str, Any]:
        """
        检查内存系统健康状态
        
        Returns:
            健康检查结果
        """
        health = {
            "timestamp": datetime.now().isoformat(),
            "status": "healthy",
            "checks": {}
        }
        
        # 检查文件存在性
        store_exists = self.store_path.exists()
        reflect_exists = self.reflect_path.exists()
        
        health["checks"]["store_exists"] = store_exists
        health["checks"]["reflect_exists"] = reflect_exists
        
        if not store_exists or not reflect_exists:
            health["status"] = "degraded"
            return health
        
        # 检查文件大小
        store_size_mb = self.store_path.stat().st_size / (1024 * 1024)
        reflect_size_mb = self.reflect_path.stat().st_size / (1024 * 1024)
        max_size = self.config.get("performance", {}).get("max_memory_size_mb", 100)
        
        health["checks"]["store_size_mb"] = store_size_mb
        health["checks"]["reflect_size_mb"] = reflect_size_mb
        health["checks"]["size_ok"] = (store_size_mb + reflect_size_mb) < max_size
        
        if (store_size_mb + reflect_size_mb) > max_size:
            health["status"] = "warning"
            health["warning"] = f"Memory size ({store_size_mb + reflect_size_mb:.1f}MB) exceeds limit ({max_size}MB)"
        
        # 检查最后更新时间
        store_age_hours = (datetime.now() - datetime.fromtimestamp(self.store_path.stat().st_mtime)).total_seconds() / 3600
        health["checks"]["store_age_hours"] = store_age_hours
        
        return health
    
    def run_consolidation_cycle(self,
                               conversation: List[Dict[str, str]],
                               task_id: str = "unknown") -> Dict[str, Any]:
        """
        运行完整的巩固循环
        
        Args:
            conversation: 完整对话历史
            task_id: 任务 ID
            
        Returns:
            巩固结果
        """
        print(f"\n🔄 Starting consolidation cycle for task {task_id}")
        
        result = {}
        
        # 步骤 1: 生成摘要
        print("  → 生成摘要...")
        summary = self.summarize_conversation(conversation, method="extractive")
        result["summary"] = summary
        print(f"    ✓ 压缩率: {summary['compression_ratio']:.1%}")
        
        # 步骤 2: 保存到记忆
        print("  → 保存到记忆...")
        save_result = self.save_to_memory(summary, task_id=task_id)
        result["save"] = save_result
        if save_result.get("saved"):
            print(f"    ✓ 保存到 L3: {save_result['l3_id']}")
        
        # 步骤 3: 重置上下文
        print("  → 重置上下文...")
        reset_result = self.reset_context()
        result["reset"] = reset_result
        print(f"    ✓ 上下文已清空 (释放 {reset_result['previous_tokens']} token)")
        
        # 步骤 4: 健康检查
        print("  → 健康检查...")
        health = self.check_memory_health()
        result["health"] = health
        print(f"    ✓ 系统状态: {health['status']}")
        
        print("✅ 巩固循环完成\n")
        
        return result


# ========================================
# 使用示例
# ========================================

def example_basic_usage():
    """基础使用示例"""
    summarizer = AutoSummarizer(memory_dir="memory")
    
    # 监控上下文
    result = summarizer.monitor_context(
        current_text="这是一个很长的对话..." * 100,
        task_id="qa_001"
    )
    
    print(f"监控结果: {result}")
    
    if result["should_summarize"]:
        # 模拟对话
        conversation = [
            {"role": "user", "content": "什么是 Python?"},
            {"role": "assistant", "content": "Python 是一种编程语言..."},
            {"role": "user", "content": "如何学习 Python?"},
            {"role": "assistant", "content": "可以通过官方教程..."}
        ]
        
        # 生成摘要
        summary = summarizer.summarize_conversation(conversation)
        print(f"摘要: {summary['summary'][:100]}...")
        
        # 保存到记忆
        save_result = summarizer.save_to_memory(summary, task_id="qa_001")
        print(f"保存结果: {save_result}")


def example_monitoring():
    """监控示例"""
    summarizer = AutoSummarizer(memory_dir="memory")
    
    # 模拟多次上下文增长
    for i in range(1, 6):
        tokens = i * 1500
        result = summarizer.monitor_context(token_count=tokens)
        
        print(f"Round {i}: {result['tokens']} tokens, should_summarize={result['should_summarize']}")
        
        if result["should_summarize"]:
            print(f"  → 原因: {result['reason']}")


if __name__ == "__main__":
    print("=" * 60)
    print("Auto-Summary Module Demo")
    print("=" * 60)
    
    # 运行示例
    # example_basic_usage()
    # example_monitoring()
    
    print("\n✅ Module loaded successfully!")
    print("导入使用: from auto_summary import AutoSummarizer")
