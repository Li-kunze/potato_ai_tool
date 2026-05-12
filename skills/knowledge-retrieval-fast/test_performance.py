#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试脚本
对比: 原 knowledge-retrieval-agent vs 新的 fast retriever
"""

import time
import sys
sys.path.insert(0, './scripts')

from retriever import quick_search, multi_search, get_stats, clear_cache

def test_single_query():
    """测试单次查询性能"""
    print("\n" + "="*60)
    print("测试1: 单次查询性能")
    print("="*60)
    
    query = "什么是DDMRP"
    
    # 第一次查询（冷启动）
    print(f"\n查询: {query}")
    print("第一次查询（冷启动）...")
    result1 = quick_search(query, n_results=5)
    print(f"  耗时: {result1['response_time']}, 缓存: {result1['cached']}")
    
    # 第二次查询（缓存命中）
    print("第二次查询（缓存命中）...")
    result2 = quick_search(query, n_results=5)
    print(f"  耗时: {result2['response_time']}, 缓存: {result2['cached']}")
    
    # 新查询
    print("新查询（不同内容）...")
    result3 = quick_search("什么是齐套分析", n_results=5)
    print(f"  耗时: {result3['response_time']}, 缓存: {result3['cached']}")

def test_multi_query():
    """测试多查询性能"""
    print("\n" + "="*60)
    print("测试2: 多查询并行检索")
    print("="*60)
    
    queries = [
        "DDMRP定义",
        "缓冲库存",
        "红黄绿三区",
        "齐套分析"
    ]
    
    print(f"\n查询列表: {queries}")
    result = multi_search(queries, n_results=3)
    print(f"耗时: {result['response_time']}")
    print(f"去重后结果数: {result['total_unique']}")

def test_stats():
    """测试统计信息"""
    print("\n" + "="*60)
    print("测试3: 统计信息")
    print("="*60)
    
    stats = get_stats()
    print(f"\n总文档数: {stats['total_documents']}")
    print(f"缓存条目: {stats['cache_entries']}")
    print(f"数据库路径: {stats['db_path']}")
    print(f"集合名称: {stats['collection']}")

def benchmark():
    """基准测试"""
    print("\n" + "="*60)
    print("基准测试: 10次连续查询")
    print("="*60)
    
    queries = [
        "什么是DDMRP",
        "什么是齐套分析",
        "速普用户登录",
        "缓冲库存设定",
        "传统MRP区别",
        "红黄绿三区",
        "补货建议",
        "齐套模拟",
        "库存水位",
        "需求驱动"
    ]
    
    times = []
    for i, query in enumerate(queries, 1):
        start = time.time()
        result = quick_search(query, n_results=3)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"{i:2d}. {query[:15]:15s} - {elapsed:.3f}s")
    
    print(f"\n平均耗时: {sum(times)/len(times):.3f}s")
    print(f"最快: {min(times):.3f}s")
    print(f"最慢: {max(times):.3f}s")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Knowledge Retrieval Fast - 性能测试")
    print("="*60)
    
    # 先显示统计信息
    test_stats()
    
    # 运行测试
    test_single_query()
    test_multi_query()
    benchmark()
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60)
