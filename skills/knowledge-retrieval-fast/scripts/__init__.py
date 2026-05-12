#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Retrieval Fast - 高性能检索模块
"""

from .retriever import (
    FastRetriever,
    get_retriever,
    quick_search,
    multi_search,
    cached_search,
    clear_cache,
    get_stats
)

__all__ = [
    "FastRetriever",
    "get_retriever",
    "quick_search",
    "multi_search",
    "cached_search",
    "clear_cache",
    "get_stats"
]
