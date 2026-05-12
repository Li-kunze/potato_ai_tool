---
name: knowledge-retrieval-fast
description: 高性能知识库检索 Skill。直接连接 ChromaDB，无需子Agent，响应时间 < 1秒。适用于简单事实查询和快速检索场景。
---

# Knowledge Retrieval Fast - 高性能检索

## 定位

- **用途**: 快速知识库检索，响应时间 < 1秒
- **适用场景**: 简单事实查询、定义查询、快速查找
- **不适用**: 需要深度分析、多文档综合的复杂查询

## 性能对比

| 指标 | 原 knowledge-retrieval-agent | 本 skill |
|:-----|:-----------------------------|:---------|
| 响应时间 | 20-40秒 | **< 1秒** |
| 缓存命中 | 无 | **< 0.1秒** |
| 模型加载 | 每次5秒 | **一次性** |

## 使用方法

### 1. 简单查询（推荐）

```python
from skills.knowledge_retrieval_fast import quick_search

# 单次检索 - 0.5-0.9秒
results = quick_search("什么是DDMRP", n_results=5)
```

### 2. 多维度查询

```python
from skills.knowledge_retrieval_fast import multi_search

# 并行多查询 - 1-2秒
queries = ["DDMRP定义", "缓冲库存", "红黄绿三区"]
results = multi_search(queries, n_results=3)
```

### 3. 带缓存的查询

```python
from skills.knowledge_retrieval_fast import cached_search

# 第二次查询瞬间返回
cached_search("什么是DDMRP")  # 0.6秒
cached_search("什么是DDMRP")  # 0.001秒（缓存命中）
```

## 与原 Skill 的协作

```
用户提问
    ↓
判断问题复杂度
    ├─ 简单问题 → @knowledge-retrieval-fast (< 1秒)
    └─ 复杂问题 → @knowledge-retrieval-agent (深度分析)
```

## 配置参数

```yaml
# config.yaml
chroma_db_path: "./chroma_db"
collection_name: "flexplanner_kb"
cache_enabled: true
cache_size: 1000
n_results_default: 5
```

## 依赖

```bash
pip install chromadb
```

## 注意事项

1. **首次初始化**: 第一次调用会加载 ChromaDB（约0.5秒）
2. **缓存机制**: 相同查询自动缓存，重启后失效
3. **线程安全**: 单例模式，多线程安全
4. **资源占用**: 内存占用约 50-100MB
