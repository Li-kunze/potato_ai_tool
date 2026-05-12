# Knowledge Base Manager V2 - 使用示例

## 示例1: 添加Word文档

```bash
# 添加单个Word文档
python scripts/kb_manager.py add "报告.docx" "工作报告,2024,销售"

# 输出示例
{
  "success": true,
  "doc_id": "doc_20240115143025_a1b2c3d4",
  "metadata": {
    "id": "doc_20240115143025_a1b2c3d4",
    "title": "报告.docx",
    "source": "报告.docx",
    "type": "word",
    "added_time": "2024-01-15T14:30:25",
    "tags": ["工作报告", "2024", "销售"],
    "file_metadata": {
      "title": "2024年度销售报告",
      "author": "张三",
      "paragraphs_count": 45,
      "tables_count": 3
    }
  }
}
```

## 示例2: 添加Excel文档

```bash
# 添加Excel文件（包含多个工作表）
python scripts/kb_manager.py add "数据分析.xlsx" "数据,分析,财务报表"

# 输出示例
{
  "success": true,
  "doc_id": "doc_20240115143110_e5f6g7h8",
  "metadata": {
    "id": "doc_20240115143110_e5f6g7h8",
    "title": "数据分析.xlsx",
    "type": "excel",
    "file_metadata": {
      "sheets": ["Sheet1", "销售数据", "财务报表"],
      "sheets_count": 3,
      "total_rows": 1250
    }
  }
}
```

## 示例3: 添加PDF文档

```bash
# 添加PDF文件
python scripts/kb_manager.py add "技术白皮书.pdf" "技术文档,架构设计"
```

## 示例4: 批量添加文件夹

```python
import os
from scripts.kb_manager import add_document

folder_path = "文档/"
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        result = add_document(file_path, tags=["批量导入"])
        print(f"Added: {filename} -> {result.get('doc_id', 'FAILED')}")
```

## 示例5: 搜索文档

```bash
# 按关键词搜索
python scripts/kb_manager.py search "销售"

# 按标签搜索
python scripts/kb_manager.py tag "工作报告"
```

## 示例6: 查看统计信息

```bash
python scripts/kb_manager.py stats

# 输出示例
{
  "total_documents": 25,
  "type_distribution": {
    "word": 8,
    "excel": 6,
    "pdf": 5,
    "markdown": 4,
    "text": 2
  },
  "total_tags": 15,
  "tags": ["工作报告", "数据分析", "技术文档", "财务报表", "会议纪要"]
}
```

## Python API 使用示例

```python
from scripts.kb_manager import add_document, search_documents, get_stats

# 添加文档
result = add_document(
    file_path="重要报告.docx",
    tags=["重要", "2024", "季度报告"],
    title="2024年Q1季度报告"
)

if result['success']:
    print(f"文档已添加，ID: {result['doc_id']}")
else:
    print(f"添加失败: {result['error']}")

# 搜索文档
results = search_documents("销售数据")
for doc in results:
    print(f"- {doc['title']} ({doc['id']})")

# 获取统计
stats = get_stats()
print(f"知识库共有 {stats['total_documents']} 个文档")
```

## 支持的文件类型

| 扩展名 | 类型 | 说明 |
|:-------|:-----|:-----|
| .docx | Word | 提取段落和表格 |
| .xlsx, .xls | Excel | 提取所有工作表 |
| .pptx, .ppt | PowerPoint | 提取幻灯片文本 |
| .pdf | PDF | 提取文本和表格 |
| .md | Markdown | 直接读取 |
| .txt, .csv, .json | 文本 | 直接读取 |
| .html, .htm | HTML | 直接读取 |

## 错误处理

常见错误及解决方案:

1. **文件不存在**
   ```
   {"success": false, "error": "File not found: xxx.docx"}
   ```
   解决方案: 检查文件路径是否正确

2. **不支持的文件类型**
   ```
   {"success": false, "error": "Unsupported file type: unknown"}
   ```
   解决方案: 将文件转换为支持的格式

3. **依赖缺失**
   ```
   ImportError: No module named 'docx'
   ```
   解决方案: 安装依赖 `pip install python-docx pandas pdfplumber python-pptx`
