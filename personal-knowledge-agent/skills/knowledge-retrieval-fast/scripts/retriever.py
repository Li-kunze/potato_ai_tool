#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高性能知识库检索模块
目标: 检索时间 < 1秒
"""

import chromadb
import hashlib
import time
from typing import List, Dict, Any, Optional
from functools import lru_cache

class FastRetriever:
    """高性能检索器 - 单例模式"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls, db_path: str = "./chroma_db", collection_name: str = "flexplanner_kb"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "flexplanner_kb"):
        if FastRetriever._initialized:
            return
        
        self.db_path = db_path
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.query_cache = {}
        self._init_db()
        FastRetriever._initialized = True
    
    def _init_db(self):
        """初始化数据库连接"""
        try:
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.collection = self.client.get_collection(self.collection_name)
            print(f"[FastRetriever] 知识库已加载，文档数: {self.collection.count()}")
        except Exception as e:
            print(f"[FastRetriever] 初始化失败: {e}")
            raise
    
    def _get_cache_key(self, query: str, n_results: int) -> str:
        """生成缓存键"""
        key = f"{query}:{n_results}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def search(self, query: str, n_results: int = 5, use_cache: bool = True) -> Dict[str, Any]:
        """
        快速检索
        
        Args:
            query: 查询文本
            n_results: 返回结果数量
            use_cache: 是否使用缓存
        
        Returns:
            检索结果字典
        """
        start_time = time.time()
        cache_key = self._get_cache_key(query, n_results) if use_cache else None
        
        # 检查缓存
        if use_cache and cache_key in self.query_cache:
            elapsed = time.time() - start_time
            return {
                "success": True,
                "cached": True,
                "response_time": f"{elapsed:.3f}s",
                "data": self.query_cache[cache_key]
            }
        
        # 执行检索
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # 格式化结果
            formatted = {
                "query": query,
                "total": len(results["ids"][0]),
                "results": []
            }
            
            for i in range(len(results["ids"][0])):
                formatted["results"].append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity": round(1 - results["distances"][0][i], 4)
                })
            
            # 写入缓存
            if use_cache:
                self.query_cache[cache_key] = formatted
            
            elapsed = time.time() - start_time
            return {
                "success": True,
                "cached": False,
                "response_time": f"{elapsed:.3f}s",
                "data": formatted
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": f"{time.time() - start_time:.3f}s"
            }
    
    def search_multi(self, queries: List[str], n_results: int = 3) -> Dict[str, Any]:
        """多查询并行检索"""
        start_time = time.time()
        all_results = []
        seen_ids = set()
        
        for query in queries:
            result = self.search(query, n_results, use_cache=True)
            if result["success"]:
                for r in result["data"]["results"]:
                    if r["id"] not in seen_ids:
                        seen_ids.add(r["id"])
                        all_results.append(r)
        
        # 按相似度排序
        all_results.sort(key=lambda x: x["similarity"], reverse=True)
        
        elapsed = time.time() - start_time
        return {
            "success": True,
            "response_time": f"{elapsed:.3f}s",
            "total_unique": len(all_results),
            "results": all_results
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.query_cache.clear()
        return {"success": True, "message": "缓存已清空"}
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "success": True,
            "total_documents": self.collection.count() if self.collection else 0,
            "cache_entries": len(self.query_cache),
            "db_path": self.db_path,
            "collection": self.collection_name
        }


# 全局单例
_retriever: Optional[FastRetriever] = None

def get_retriever(db_path: str = "./chroma_db", collection_name: str = "flexplanner_kb") -> FastRetriever:
    """获取检索器单例"""
    global _retriever
    if _retriever is None:
        _retriever = FastRetriever(db_path, collection_name)
    return _retriever


# 便捷函数 - 使用正确的默认路径
DEFAULT_DB_PATH: str = "D:/potato_project/flexplanner_seat7(active)/chroma_db"

def quick_search(query: str, n_results: int = 5, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """快速检索"""
    return get_retriever(db_path).search(query, n_results)

def multi_search(queries: List[str], n_results: int = 3, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """多查询检索"""
    return get_retriever(db_path).search_multi(queries, n_results)

def cached_search(query: str, n_results: int = 5, db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """带缓存的检索"""
    return get_retriever(db_path).search(query, n_results, use_cache=True)

def clear_cache(db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """清空缓存"""
    return get_retriever(db_path).clear_cache()

def get_stats(db_path: str = DEFAULT_DB_PATH) -> Dict[str, Any]:
    """获取统计信息"""
    return get_retriever(db_path).get_stats()
