# Knowledge Base Manager V2 - 集成指南

本指南说明如何在 `knowledge-base-manager-agent` 中集成使用 `knowledge-base-manager-v2`。

## 集成架构

```
┌─────────────────────────────────────────────────────────────┐
│              knowledge-base-manager-agent                    │
│                      (父Agent)                               │
├─────────────────────────────────────────────────────────────┤
│  1. 接收用户请求: "添加 report.docx 到知识库"                  │
│  2. 检测文件类型: .docx → 复杂格式                            │
│  3. 调用 @knowledge-base-manager-v2                          │
│  4. 接收提取结果                                             │
│  5. 生成嵌入向量                                             │
│  6. 存储到向量数据库                                          │
│  7. 返回确认给用户                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              knowledge-base-manager-v2                       │
│                   (子工具/Skill)                             │
├─────────────────────────────────────────────────────────────┤
│  职责: 从复杂格式文件中提取结构化内容                          │
│  输入: 文件路径                                               │
│  输出: {content, metadata, structured_data}                  │
│  不处理: 向量嵌入、数据库存储                                  │
└─────────────────────────────────────────────────────────────┘
```

## 使用示例

### 示例1: 在Agent中调用

```python
# knowledge-base-manager-agent 的实现

def add_document_to_kb(file_path: str, tags: List[str] = None):
    """添加文档到知识库"""
    
    # Step 1: 检测文件类型
    file_ext = Path(file_path).suffix.lower()
    complex_formats = ['.docx', '.xlsx', '.xls', '.pptx', '.ppt', '.pdf']
    
    if file_ext in complex_formats:
        # Step 2: 调用 knowledge-base-manager-v2 提取内容
        result = call_skill(
            'knowledge-base-manager-v2',
            {'action': 'extract', 'file_path': file_path}
        )
        
        if not result['success']:
            return {
                'success': False,
                'error': f"内容提取失败: {result['error']}"
            }
        
        content = result['content']
        metadata = result['metadata']
        structured_data = result.get('structured_data')
        
    else:
        # 简单格式直接读取
        content = read_text_file(file_path)
        metadata = {
            'title': Path(file_path).stem,
            'type': 'text',
            'source': file_path
        }
    
    # Step 3: 生成嵌入向量（使用 rag-implementation skill）
    embedding = generate_embedding(content)
    
    # Step 4: 存储到向量数据库
    doc_id = save_to_vector_db(
        content=content,
        embedding=embedding,
        metadata=metadata,
        tags=tags or []
    )
    
    return {
        'success': True,
        'doc_id': doc_id,
        'metadata': metadata
    }
```

### 示例2: 批量处理文件夹

```python
def batch_add_documents(folder_path: str, tags: List[str] = None):
    """批量添加文件夹中的文档"""
    
    results = []
    
    # 调用 knowledge-base-manager-v2 批量提取
    extract_results = call_skill(
        'knowledge-base-manager-v2',
        {
            'action': 'batch_extract',
            'folder_path': folder_path,
            'recursive': True
        }
    )
    
    for result in extract_results:
        if result['success']:
            # 生成嵌入并存储
            embedding = generate_embedding(result['content'])
            doc_id = save_to_vector_db(
                content=result['content'],
                embedding=embedding,
                metadata=result['metadata'],
                tags=tags or []
            )
            results.append({
                'file': result['metadata']['source'],
                'status': 'success',
                'doc_id': doc_id
            })
        else:
            results.append({
                'file': result['metadata']['source'],
                'status': 'failed',
                'error': result['error']
            })
    
    return results
```

### 示例3: 处理不同格式的特殊逻辑

```python
def process_with_format_specific_logic(file_path: str):
    """根据格式执行特殊处理"""
    
    result = call_skill(
        'knowledge-base-manager-v2',
        {'action': 'extract', 'file_path': file_path}
    )
    
    if not result['success']:
        return result
    
    metadata = result['metadata']
    structured_data = result.get('structured_data', {})
    
    # 根据格式类型执行特殊处理
    if metadata['type'] == 'excel':
        # Excel特殊处理: 为每个工作表生成单独的嵌入
        for sheet_name, sheet_data in structured_data['sheets'].items():
            sheet_content = f"{sheet_name}\n{sheet_data['text']}"
            embedding = generate_embedding(sheet_content)
            save_to_vector_db(
                content=sheet_content,
                embedding=embedding,
                metadata={**metadata, 'sheet': sheet_name}
            )
    
    elif metadata['type'] == 'powerpoint':
        # PPT特殊处理: 为每个幻灯片生成单独的嵌入
        for slide in structured_data['slides']:
            slide_content = f"Slide {slide['slide_number']}\n{slide['text']}"
            embedding = generate_embedding(slide_content)
            save_to_vector_db(
                content=slide_content,
                embedding=embedding,
                metadata={**metadata, 'slide': slide['slide_number']}
            )
    
    else:
        # 默认处理: 整个文档作为一个条目
        embedding = generate_embedding(result['content'])
        save_to_vector_db(
            content=result['content'],
            embedding=embedding,
            metadata=metadata
        )
```

## 返回数据结构

### 成功返回

```json
{
    "success": true,
    "content": "纯文本内容，用于生成嵌入向量...",
    "metadata": {
        "title": "文档标题",
        "source": "/path/to/file.docx",
        "file_name": "file.docx",
        "type": "word",
        "author": "作者名",
        "created": "2024-01-15T10:30:00",
        "paragraphs_count": 45,
        "tables_count": 3,
        "word_count": 5000
    },
    "structured_data": {
        "paragraphs": ["段落1", "段落2", ...],
        "tables": [
            [["单元格1", "单元格2"], ["单元格3", "单元格4"]]
        ]
    }
}
```

### 失败返回

```json
{
    "success": false,
    "error": "Word extraction failed: ...",
    "content": "",
    "metadata": {
        "source": "/path/to/file.docx",
        "type": "word"
    }
}
```

## 错误处理建议

```python
def safe_extract(file_path: str) -> Dict:
    """安全提取，带错误处理"""
    
    try:
        result = call_skill(
            'knowledge-base-manager-v2',
            {'action': 'extract', 'file_path': file_path}
        )
        
        if not result['success']:
            # 提取失败，记录日志
            log_error(f"提取失败: {file_path}, 错误: {result['error']}")
            
            # 尝试备用方法: 转为文本文件
            if try_convert_to_text(file_path):
                return extract_as_text(file_path)
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': f'调用skill失败: {str(e)}',
            'content': '',
            'metadata': {'source': file_path}
        }
```

## 依赖项

确保环境中安装以下依赖:

```bash
pip install python-docx pandas openpyxl python-pptx pdfplumber
```

## 注意事项

1. **不要重复处理**: `knowledge-base-manager-v2` 只负责提取，父Agent负责存储
2. **错误传递**: 所有提取错误应返回给父Agent处理
3. **元数据保留**: 保留 `metadata` 和 `structured_data` 用于展示和调试
4. **纯文本优先**: `content` 字段必须是纯文本，便于生成嵌入
