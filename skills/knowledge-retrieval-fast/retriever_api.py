#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Retrieval Fast - API 接口
为主协调器提供简单的检索接口
"""

import sys
import os

# 添加脚本路径
scripts_path = os.path.join(os.path.dirname(__file__), 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)

from retriever import quick_search, multi_search, get_stats

def search_knowledge_base(query: str, n_results: int = 5) -> dict:
    """
    搜索知识库 - 主协调器调用接口
    
    Args:
        query: 查询文本
        n_results: 返回结果数量，默认5条
    
    Returns:
        {
            "success": bool,
            "response_time": str,
            "results": [
                {
                    "id": str,
                    "content": str,
                    "metadata": dict,
                    "similarity": float
                }
            ]
        }
    """
    result = quick_search(query, n_results)
    
    if result["success"]:
        return {
            "success": True,
            "response_time": result["response_time"],
            "cached": result.get("cached", False),
            "results": result["data"]["results"]
        }
    else:
        return {
            "success": False,
            "error": result.get("error", "未知错误"),
            "response_time": result["response_time"]
        }

def search_multiple(queries: list, n_results: int = 3) -> dict:
    """
    多查询搜索 - 用于复杂问题
    
    Args:
        queries: 查询文本列表
        n_results: 每个查询返回结果数
    
    Returns:
        {
            "success": bool,
            "response_time": str,
            "total_unique": int,
            "results": [...]
        }
    """
    return multi_search(queries, n_results)

def get_knowledge_base_stats() -> dict:
    """获取知识库统计信息"""
    return get_stats()


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("Knowledge Retrieval Fast - API 测试")
    print("=" * 60)
    
    # 测试1: 简单查询
    print("\n[测试1] 简单查询")
    result = search_knowledge_base("什么是DDMRP")
    print(f"成功: {result['success']}")
    print(f"耗时: {result['response_time']}")
    print(f"结果数: {len(result.get('results', []))}")
    
    # 测试2: 缓存命中
    print("\n[测试2] 缓存命中")
    result = search_knowledge_base("什么是DDMRP")
    print(f"缓存: {result.get('cached', False)}")
    print(f"耗时: {result['response_time']}")
    
    # 测试3: 统计信息
    print("\n[测试3] 统计信息")
    stats = get_knowledge_base_stats()
    print(f"总文档数: {stats.get('total_documents', 0)}")
    print(f"缓存条目: {stats.get('cache_entries', 0)}")
