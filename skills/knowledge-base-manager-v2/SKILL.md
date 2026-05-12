---
name: knowledge-base-manager-v2
description: 文档内容提取工具。专门用于从复杂格式文件(docx/xlsx/pptx/pdf)中提取结构化文本内容。作为knowledge-base-manager-agent的子工具使用，不负责向量存储，只负责内容提取和格式转换。
---

# Knowledge Base Manager V2 - 文档提取工具

**定位**: `knowledge-base-manager-agent` 的子工具  
**职责**: 从复杂格式文件中提取结构化内容  
**不处理**: 向量嵌入、数据库存储（由父Agent处理）

## 使用场景

当 `knowledge-base-manager-agent` 检测到以下文件格式时调用本技能：
- `.docx` - Word文档
- `.xlsx/.xls` - Excel表格
- `.pptx` - PowerPoint演示文稿
- `.pdf` - PDF文件

## 工作流程

```
knowledge-base-manager-agent
    ├── 检测文件类型
    ├── 如果是复杂格式 → 调用 @knowledge-base-manager-v2
    │       ├── 提取文本内容
    │       ├── 提取元数据（标题、作者、页数等）
    │       └── 返回结构化数据
    ├── 生成嵌入向量
    ├── 存储到向量数据库
    └── 返回确认
```

## 调用方式

### 1. 提取单个文件

```python
from scripts.document_extractor import extract_document

result = extract_document("report.docx")

# 返回结构:
{
    "success": True,
    "content": "提取的文本内容...",
    "metadata": {
        "title": "文档标题",
        "author": "作者",
        "type": "word",
        "pages": 10,
        "word_count": 5000
    },
    "structured_data": {
        "paragraphs": [...],
        "tables": [...]
    }
}
```

### 2. 批量提取文件夹

```python
from scripts.document_extractor import batch_extract

results = batch_extract("文档/", recursive=True)
```

## 输出格式规范

### 标准返回结构

```json
{
    "success": true/false,
    "content": "纯文本内容（用于生成嵌入）",
    "metadata": {
        "title": "文档标题",
        "source": "原始文件路径",
        "type": "word/excel/powerpoint/pdf",
        "author": "作者（如有）",
        "created": "创建时间（如有）",
        "pages": 页数/幻灯片数/工作表数,
        "word_count": 字数统计
    },
    "structured_data": {
        // 格式特定的结构化数据
        "paragraphs": [],  // Word文档段落
        "tables": [],      // 表格数据
        "sheets": {}       // Excel工作表
    },
    "error": "错误信息（如果success为false）"
}
```

## 各格式提取详情

### Word (.docx)

```python
{
    "content": "所有段落文本拼接",
    "structured_data": {
        "paragraphs": ["段落1", "段落2", ...],
        "tables": [
            [["单元格1", "单元格2"], ["单元格3", "单元格4"]]
        ]
    },
    "metadata": {
        "title": "文档属性中的标题",
        "author": "文档属性中的作者",
        "paragraphs_count": 45,
        "tables_count": 3
    }
}
```

### Excel (.xlsx)

```python
{
    "content": "所有工作表的文本表示拼接",
    "structured_data": {
        "sheets": {
            "Sheet1": {
                "headers": ["列1", "列2"],
                "data": [{"列1": "值1", "列2": "值2"}]
            }
        }
    },
    "metadata": {
        "sheets": ["Sheet1", "Sheet2"],
        "sheets_count": 2,
        "total_rows": 150
    }
}
```

### PowerPoint (.pptx)

```python
{
    "content": "所有幻灯片文本拼接",
    "structured_data": {
        "slides": [
            {"slide_number": 1, "text": "幻灯片1内容"},
            {"slide_number": 2, "text": "幻灯片2内容"}
        ]
    },
    "metadata": {
        "slides_count": 10
    }
}
```

### PDF

```python
{
    "content": "所有页面文本拼接",
    "structured_data": {
        "pages": [
            {"page_number": 1, "text": "页面1内容"}
        ],
        "tables": [
            {"page": 1, "data": [[...]]}
        ]
    },
    "metadata": {
        "pages_count": 20,
        "tables_count": 5
    }
}
```

## 错误处理

| 错误类型 | 返回结构 |
|:---------|:---------|
| 文件不存在 | `{"success": false, "error": "File not found: xxx.docx"}` |
| 格式不支持 | `{"success": false, "error": "Unsupported file type: xxx"}` |
| 提取失败 | `{"success": false, "error": "Extraction failed: ..."}` |
| 文件损坏 | `{"success": false, "error": "Corrupted file: ..."}` |

## 依赖安装

```bash
pip install python-docx pandas openpyxl python-pptx pdfplumber
```

## 与 knowledge-base-manager-agent 集成示例

```python
# knowledge-base-manager-agent 内部逻辑

def add_document(file_path, tags=None):
    # 1. 检测文件类型
    file_type = detect_file_type(file_path)
    
    # 2. 如果是复杂格式，调用 knowledge-base-manager-v2
    if file_type in ['word', 'excel', 'powerpoint', 'pdf']:
        # 调用本skill
        result = call_skill('knowledge-base-manager-v2', {
            'action': 'extract',
            'file_path': file_path
        })
        
        if not result['success']:
            return result  # 返回错误
        
        content = result['content']
        metadata = result['metadata']
    else:
        # 简单格式直接处理
        content = read_text_file(file_path)
        metadata = {'type': file_type}
    
    # 3. 生成嵌入向量（本skill不处理）
    embedding = generate_embedding(content)
    
    # 4. 存储到向量数据库（本skill不处理）
    doc_id = save_to_vector_db(content, embedding, metadata, tags)
    
    return {'success': True, 'doc_id': doc_id}
```

## 注意事项

1. **单一职责**: 本skill只负责内容提取，不处理存储
2. **纯文本输出**: `content` 字段必须是纯文本，便于生成嵌入
3. **保留结构化数据**: `structured_data` 可用于展示，但不用于嵌入
4. **错误透明**: 所有错误必须返回给父Agent处理
