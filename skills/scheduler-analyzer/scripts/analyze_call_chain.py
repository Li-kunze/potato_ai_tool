#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调用链分析脚本

分析调度任务的调用链，包括：
- Service层调用
- Repository/DAO操作
- 外部接口调用
- 数据流向

用法:
    python analyze_call_chain.py <task-file> [options]
    python analyze_call_chain.py <project-path> --task-class=<class-name> [options]

选项:
    --depth             分析深度 (默认: 3)
    --output-format     输出格式 (json/markdown/mermaid)
    --output-file       输出文件路径
    --include-private   是否包含私有方法
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class MethodCall:
    """方法调用信息"""
    method_name: str
    target_class: Optional[str]
    target_type: str  # 'service', 'repository', 'external', 'internal', 'unknown'
    line_number: int
    arguments: List[str] = field(default_factory=list)
    

@dataclass
class DataOperation:
    """数据操作信息"""
    operation_type: str  # 'SELECT', 'INSERT', 'UPDATE', 'DELETE'
    table_name: Optional[str]
    method_name: str
    line_number: int
    

@dataclass
class CallChainNode:
    """调用链节点"""
    class_name: str
    method_name: str
    method_type: str  # 'execute', 'business', 'data', 'private'
    calls: List[MethodCall] = field(default_factory=list)
    data_operations: List[DataOperation] = field(default_factory=list)
    line_number: int = 0


def extract_method_content(content: str, method_name: str) -> Optional[str]:
    """提取方法体内容"""
    # 匹配方法定义
    pattern = rf'(public|private|protected)\s+[\w<>\[\]]+\s+{method_name}\s*\([^)]*\)\s*\{{'
    match = re.search(pattern, content)
    
    if not match:
        return None
    
    start_pos = match.end() - 1
    brace_count = 0
    end_pos = start_pos
    
    for i, char in enumerate(content[start_pos:]):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos = start_pos + i + 1
                break
    
    return content[start_pos:end_pos]


def extract_service_calls(content: str, class_name: str) -> List[MethodCall]:
    """提取Service层调用"""
    calls = []
    
    # 匹配 service.methodName() 或 service.methodName(args)
    service_pattern = r'(\w+)\.(\w+)\s*\(([^)]*)\)'
    
    for match in re.finditer(service_pattern, content):
        variable = match.group(1)
        method = match.group(2)
        args = match.group(3)
        
        # 排除常见非业务调用
        if method in ['toString', 'equals', 'hashCode', 'getClass', 'clone', 'notify', 'wait']:
            continue
        
        # 推断目标类型
        target_type = 'unknown'
        if any(keyword in variable.lower() for keyword in ['service', 'biz', 'business']):
            target_type = 'service'
        elif any(keyword in variable.lower() for keyword in ['repository', 'repo', 'dao', 'mapper']):
            target_type = 'repository'
        elif any(keyword in variable.lower() for keyword in ['client', 'api', 'remote', 'feign']):
            target_type = 'external'
        elif variable == 'this' or variable == class_name.lower():
            target_type = 'internal'
        
        calls.append(MethodCall(
            method_name=method,
            target_class=variable,
            target_type=target_type,
            line_number=content[:match.start()].count('\n') + 1,
            arguments=[arg.strip() for arg in args.split(',') if arg.strip()]
        ))
    
    return calls


def extract_data_operations(content: str) -> List[DataOperation]:
    """提取数据操作"""
    operations = []
    
    # 基于Repository方法命名约定推断
    repo_patterns = [
        (r'\.(find|get|query|select|search)[\w]*\(', 'SELECT'),
        (r'\.(save|insert|add|create)[\w]*\(', 'INSERT'),
        (r'\.(update|modify|edit)[\w]*\(', 'UPDATE'),
        (r'\.(delete|remove|clear)[\w]*\(', 'DELETE'),
    ]
    
    for pattern, op_type in repo_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            method_name = match.group(0).strip('.(')
            operations.append(DataOperation(
                operation_type=op_type,
                table_name=None,  # 需要进一步分析
                method_name=method_name,
                line_number=content[:match.start()].count('\n') + 1
            ))
    
    return operations


def infer_table_name(repo_class_name: str) -> Optional[str]:
    """从Repository类名推断表名"""
    # 移除后缀
    table_name = repo_class_name.replace('Repository', '').replace('Repo', '').replace('Dao', '').replace('Mapper', '')
    
    # 驼峰转下划线
    import re
    table_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', table_name).lower()
    
    return table_name if table_name else None


def analyze_task_file(file_path: Path, depth: int = 3, include_private: bool = False) -> Optional[Dict]:
    """分析任务文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取类名
        class_match = re.search(r'public\s+class\s+(\w+)', content)
        if not class_match:
            return None
        
        class_name = class_match.group(1)
        
        # 提取注入的依赖
        dependencies = {}
        autowired_pattern = r'(@Autowired|@Inject)\s+\n?\s*private\s+(\w+)\s+(\w+);'
        for match in re.finditer(autowired_pattern, content):
            dep_type = match.group(2)
            dep_name = match.group(3)
            dependencies[dep_name] = dep_type
        
        # 分析方法
        methods_to_analyze = []
        
        # 查找execute方法
        execute_pattern = r'public\s+\w+\s+execute\s*\([^)]*\)'
        if re.search(execute_pattern, content):
            methods_to_analyze.append(('execute', 'execute'))
        
        # 查找其他public方法
        if include_private:
            method_pattern = r'(?:public|private)\s+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)'
        else:
            method_pattern = r'public\s+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)'
        
        for match in re.finditer(method_pattern, content):
            method_name = match.group(1)
            if method_name not in ['execute', 'getClass', 'hashCode', 'equals', 'toString', 'clone', 'notify', 'wait']:
                methods_to_analyze.append((method_name, 'business'))
        
        # 分析每个方法
        call_chain = []
        for method_name, method_type in methods_to_analyze:
            method_content = extract_method_content(content, method_name)
            if method_content:
                calls = extract_service_calls(method_content, class_name)
                data_ops = extract_data_operations(method_content)
                
                # 推断表名
                for op in data_ops:
                    for call in calls:
                        if call.target_type == 'repository':
                            table = infer_table_name(dependencies.get(call.target_class, ''))
                            if table:
                                op.table_name = table
                
                call_chain.append({
                    'class_name': class_name,
                    'method_name': method_name,
                    'method_type': method_type,
                    'calls': [
                        {
                            'method_name': c.method_name,
                            'target_class': c.target_class,
                            'target_type': c.target_type,
                            'line_number': c.line_number,
                            'arguments': c.arguments
                        }
                        for c in calls
                    ],
                    'data_operations': [
                        {
                            'operation_type': op.operation_type,
                            'table_name': op.table_name,
                            'method_name': op.method_name,
                            'line_number': op.line_number
                        }
                        for op in data_ops
                    ]
                })
        
        return {
            'class_name': class_name,
            'file_path': str(file_path),
            'dependencies': dependencies,
            'call_chain': call_chain
        }
    
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None


def generate_mermaid_diagram(analysis_result: Dict) -> str:
    """生成Mermaid流程图"""
    lines = []
    lines.append("```mermaid")
    lines.append("graph TD")
    lines.append("")
    
    class_name = analysis_result['class_name']
    lines.append(f"    {class_name}[{class_name}]")
    
    # 收集所有节点
    nodes = set()
    edges = []
    
    for method in analysis_result['call_chain']:
        method_node = f"{class_name}_{method['method_name']}"
        nodes.add((method_node, method['method_name'], method['method_type']))
        edges.append((class_name, method_node))
        
        for call in method['calls']:
            if call['target_type'] == 'service':
                target = f"Service_{call['target_class']}"
                nodes.add((target, call['target_class'], 'service'))
                edges.append((method_node, target))
            elif call['target_type'] == 'repository':
                target = f"Repo_{call['target_class']}"
                nodes.add((target, call['target_class'], 'repository'))
                edges.append((method_node, target))
            elif call['target_type'] == 'external':
                target = f"Ext_{call['target_class']}"
                nodes.add((target, call['target_class'], 'external'))
                edges.append((method_node, target))
    
    # 添加节点定义
    lines.append("    %% 节点定义")
    for node_id, node_name, node_type in nodes:
        if node_type == 'execute':
            lines.append(f"    {node_id}[{node_name}]")
        elif node_type == 'service':
            lines.append(f"    {node_id}[[{node_name}]]")
        elif node_type == 'repository':
            lines.append(f"    {node_id}[({node_name})]")
        elif node_type == 'external':
            lines.append(f"    {node_id}[/{node_name}/]")
        else:
            lines.append(f"    {node_id}[{node_name}]")
    
    lines.append("")
    lines.append("    %% 调用关系")
    for source, target in edges:
        lines.append(f"    {source} --> {target}")
    
    lines.append("```")
    
    return '\n'.join(lines)


def output_json(analysis_result: Dict, output_file: Optional[str] = None):
    """输出JSON格式"""
    json_str = json.dumps(analysis_result, ensure_ascii=False, indent=2)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"Output written to: {output_file}")
    else:
        print(json_str)


def output_markdown(analysis_result: Dict, output_file: Optional[str] = None):
    """输出Markdown格式"""
    lines = []
    lines.append(f"# 调用链分析: {analysis_result['class_name']}\n")
    
    lines.append("## 概览\n")
    lines.append(f"- **类名**: {analysis_result['class_name']}")
    lines.append(f"- **文件路径**: `{analysis_result['file_path']}`")
    lines.append(f"- **依赖数**: {len(analysis_result['dependencies'])}\n")
    
    if analysis_result['dependencies']:
        lines.append("## 依赖注入\n")
        lines.append("| 变量名 | 类型 | 推断用途 |")
        lines.append("|--------|------|---------|")
        
        for dep_name, dep_type in analysis_result['dependencies'].items():
            purpose = '未知'
            if 'Service' in dep_type or 'Biz' in dep_type:
                purpose = '业务逻辑'
            elif 'Repository' in dep_type or 'Dao' in dep_type or 'Mapper' in dep_type:
                purpose = '数据访问'
            elif 'Client' in dep_type or 'Api' in dep_type or 'Remote' in dep_type:
                purpose = '外部接口'
            
            lines.append(f"| {dep_name} | {dep_type} | {purpose} |")
        
        lines.append("")
    
    lines.append("## 方法调用链\n")
    
    for method in analysis_result['call_chain']:
        lines.append(f"### {method['method_name']} ({method['method_type']})\n")
        
        if method['calls']:
            lines.append("**服务调用**:")
            lines.append("")
            lines.append("| 目标类 | 方法 | 类型 | 行号 |")
            lines.append("|--------|------|------|------|")
            
            for call in method['calls']:
                type_map = {
                    'service': '业务服务',
                    'repository': '数据访问',
                    'external': '外部接口',
                    'internal': '内部调用',
                    'unknown': '未知'
                }
                call_type = type_map.get(call['target_type'], call['target_type'])
                lines.append(f"| {call['target_class']} | {call['method_name']} | {call_type} | {call['line_number']} |")
            
            lines.append("")
        
        if method['data_operations']:
            lines.append("**数据操作**:")
            lines.append("")
            lines.append("| 操作类型 | 表名 | 方法 | 行号 |")
            lines.append("|---------|------|------|------|")
            
            for op in method['data_operations']:
                table = op['table_name'] or '未知'
                lines.append(f"| {op['operation_type']} | {table} | {op['method_name']} | {op['line_number']} |")
            
            lines.append("")
    
    lines.append("## 调用关系图\n")
    lines.append(generate_mermaid_diagram(analysis_result))
    
    markdown_str = '\n'.join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_str)
        print(f"Output written to: {output_file}")
    else:
        print(markdown_str)


def main():
    parser = argparse.ArgumentParser(description='Analyze call chain of scheduler task')
    parser.add_argument('path', help='Path to task file or project')
    parser.add_argument('--task-class', help='Task class name (when path is project)')
    parser.add_argument('--depth', type=int, default=3, help='Analysis depth')
    parser.add_argument('--output-format', choices=['json', 'markdown', 'mermaid'], default='markdown',
                       help='Output format')
    parser.add_argument('--output-file', help='Output file path')
    parser.add_argument('--include-private', action='store_true', help='Include private methods')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    result = None
    
    if path.is_file():
        # 分析单个文件
        print(f"Analyzing file: {path}")
        result = analyze_task_file(path, args.depth, args.include_private)
    else:
        # 在项目中查找类
        if not args.task_class:
            print("Error: --task-class is required when path is a directory")
            return
        
        print(f"Searching for class {args.task_class} in {path}")
        
        # 查找文件
        found = False
        for java_file in path.rglob('*.java'):
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if f'class {args.task_class}' in content or f'class {args.task_class} ' in content:
                print(f"Found in: {java_file}")
                result = analyze_task_file(java_file, args.depth, args.include_private)
                found = True
                break
        
        if not found:
            print(f"Error: Class {args.task_class} not found")
            return
        
        if not result:
            print("Error: Failed to analyze task")
            return
    
    if not result:
        print("Error: Failed to analyze task")
        return
    
    print(f"\nGenerating {args.output_format} output...")
    
    if args.output_format == 'json':
        output_json(result, args.output_file)
    elif args.output_format == 'markdown':
        output_markdown(result, args.output_file)
    elif args.output_format == 'mermaid':
        diagram = generate_mermaid_diagram(result)
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(diagram)
            print(f"Output written to: {args.output_file}")
        else:
            print(diagram)
    
    print("Done!")


if __name__ == '__main__':
    main()
