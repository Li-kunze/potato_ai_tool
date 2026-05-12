#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调度信息提取脚本

从Java项目中提取调度任务的基本信息，包括：
- 任务类列表
- 实现的接口/继承的类
- 注入的依赖
- 触发配置（如可获取）

用法:
    python extract_scheduler_info.py <project-path> [options]

选项:
    --framework-type    框架类型 (quartz/spring-scheduler/spring-batch/custom)
    --output-format     输出格式 (json/markdown/csv)
    --output-file       输出文件路径
    --include-pattern   包含的文件模式 (默认: *.java)
    --exclude-pattern   排除的文件模式
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class SchedulerTask:
    """调度任务信息"""
    class_name: str
    package: str
    file_path: str
    implements: List[str]
    extends: Optional[str]
    dependencies: List[Dict[str, str]]
    methods: List[str]
    annotations: List[str]
    business_domain: Optional[str] = None
    trigger_config: Optional[Dict] = None


def find_java_files(project_path: str, include_pattern: str = "*.java", 
                    exclude_patterns: Optional[List[str]] = None) -> List[Path]:
    """查找项目中的所有Java文件"""
    project = Path(project_path)
    java_files = list(project.rglob(include_pattern))
    
    if exclude_patterns:
        filtered_files = []
        for file in java_files:
            should_exclude = False
            for pattern in exclude_patterns:
                if pattern in str(file):
                    should_exclude = True
                    break
            if not should_exclude:
                filtered_files.append(file)
        java_files = filtered_files
    
    return java_files


def extract_package(content: str) -> Optional[str]:
    """提取包名"""
    match = re.search(r'package\s+([\w.]+);', content)
    return match.group(1) if match else None


def extract_class_name(content: str) -> Optional[str]:
    """提取类名"""
    # 匹配 public class ClassName 或 public class ClassName implements/extends
    match = re.search(r'public\s+class\s+(\w+)', content)
    return match.group(1) if match else None


def extract_implements(content: str) -> List[str]:
    """提取实现的接口"""
    implements = []
    
    # 匹配 implements Interface1, Interface2
    match = re.search(r'implements\s+([\w\s,]+)(?:\{|extends)', content)
    if match:
        interfaces = match.group(1)
        # 分割并清理
        for interface in interfaces.split(','):
            clean_interface = interface.strip()
            if clean_interface:
                implements.append(clean_interface)
    
    return implements


def extract_extends(content: str) -> Optional[str]:
    """提取继承的类"""
    match = re.search(r'extends\s+(\w+)', content)
    return match.group(1) if match else None


def extract_dependencies(content: str) -> List[Dict[str, str]]:
    """提取注入的依赖"""
    dependencies = []
    
    # 匹配 @Autowired 或 @Inject 字段
    autowired_pattern = r'(@Autowired|@Inject)\s+\n?\s*(private|protected|public)?\s+(\w+)\s+(\w+);'
    
    for match in re.finditer(autowired_pattern, content):
        annotation = match.group(1)
        field_type = match.group(3)
        field_name = match.group(4)
        
        dependencies.append({
            'type': field_type,
            'name': field_name,
            'injection_type': annotation
        })
    
    # 匹配 @Value 注入
    value_pattern = r'@Value\("([^"]+)"\)\s+\n?\s*(private|protected|public)?\s+(\w+)\s+(\w+);'
    
    for match in re.finditer(value_pattern, content):
        config_key = match.group(1)
        field_type = match.group(3)
        field_name = match.group(4)
        
        dependencies.append({
            'type': field_type,
            'name': field_name,
            'injection_type': '@Value',
            'config_key': config_key
        })
    
    return dependencies


def extract_methods(content: str) -> List[str]:
    """提取类的方法签名"""
    methods = []
    
    # 匹配方法定义 (简化版)
    method_pattern = r'(public|private|protected)\s+(\w+)\s+(\w+)\s*\([^)]*\)'
    
    for match in re.finditer(method_pattern, content):
        return_type = match.group(2)
        method_name = match.group(3)
        methods.append(f"{return_type} {method_name}()")
    
    return methods


def extract_annotations(content: str) -> List[str]:
    """提取类级别的注解"""
    annotations = []
    
    # 匹配类前的注解
    annotation_pattern = r'(@\w+(?:\([^)]*\))?)\s+\n?\s*public\s+class'
    
    for match in re.finditer(annotation_pattern, content):
        annotation = match.group(1)
        annotations.append(annotation)
    
    return annotations


def infer_business_domain(class_name: str, package: str, implements: List[str]) -> Optional[str]:
    """推断业务域"""
    # 基于类名推断
    domain_keywords = {
        'Sync': '数据同步',
        'Import': '数据导入',
        'Export': '数据导出',
        'Cal': '计算处理',
        'Calc': '计算处理',
        'Compute': '计算处理',
        'Process': '数据处理',
        'Handle': '业务处理',
        'Clean': '数据清理',
        'Clear': '数据清理',
        'Delete': '数据删除',
        'Archive': '数据归档',
        'Notice': '通知告警',
        'Alert': '通知告警',
        'Mail': '邮件通知',
        'Control': '控制协调',
        'Manager': '控制协调',
        'Schedule': '调度控制',
        'Batch': '批处理',
        'Mrp': '物料需求计划',
        'Aps': '高级计划排程',
        'Crp': '能力需求计划',
        'Ddmrp': '需求驱动MRP',
        'WorkOrder': '工单管理',
        'Inventory': '库存管理',
        'Demand': '需求管理',
        'Supply': '供应管理',
        'Bom': '物料清单',
        'Routing': '工艺路线'
    }
    
    for keyword, domain in domain_keywords.items():
        if keyword in class_name:
            return domain
    
    # 基于包名推断
    package_keywords = {
        'sync': '数据同步',
        'batch': '批处理',
        'job': '调度任务',
        'task': '任务处理',
        'mrp': '物料需求计划',
        'aps': '高级计划排程',
        'crp': '能力需求计划'
    }
    
    package_lower = package.lower()
    for keyword, domain in package_keywords.items():
        if keyword in package_lower:
            return domain
    
    return None


def analyze_task_file(file_path: Path) -> Optional[SchedulerTask]:
    """分析单个任务文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        package = extract_package(content)
        class_name = extract_class_name(content)
        
        if not class_name:
            return None
        
        implements = extract_implements(content)
        extends = extract_extends(content)
        dependencies = extract_dependencies(content)
        methods = extract_methods(content)
        annotations = extract_annotations(content)
        
        # 推断业务域
        business_domain = infer_business_domain(class_name, package or '', implements)
        
        return SchedulerTask(
            class_name=class_name,
            package=package or '',
            file_path=str(file_path),
            implements=implements,
            extends=extends,
            dependencies=dependencies,
            methods=methods,
            annotations=annotations,
            business_domain=business_domain
        )
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None


def filter_scheduler_tasks(tasks: List[SchedulerTask], 
                          framework_type: Optional[str] = None) -> List[SchedulerTask]:
    """过滤出调度任务"""
    scheduler_tasks = []
    
    # 调度相关的接口/基类关键字
    scheduler_keywords = [
        'Job', 'Task', 'Executor', 'Scheduler',
        'JobExecutor', 'TaskExecutor', 'JobTask',
        'Batch', 'Schedule'
    ]
    
    for task in tasks:
        is_scheduler = False
        
        # 检查实现的接口
        for impl in task.implements:
            for keyword in scheduler_keywords:
                if keyword in impl:
                    is_scheduler = True
                    break
            if is_scheduler:
                break
        
        # 检查继承的类
        if not is_scheduler and task.extends:
            for keyword in scheduler_keywords:
                if keyword in task.extends:
                    is_scheduler = True
                    break
        
        # 检查注解
        if not is_scheduler:
            for annotation in task.annotations:
                if 'Scheduled' in annotation or 'Job' in annotation:
                    is_scheduler = True
                    break
        
        # 检查包名
        if not is_scheduler:
            package_keywords = ['batch', 'job', 'task', 'scheduler']
            for keyword in package_keywords:
                if keyword in task.package.lower():
                    is_scheduler = True
                    break
        
        if is_scheduler:
            scheduler_tasks.append(task)
    
    return scheduler_tasks


def output_json(tasks: List[SchedulerTask], output_file: Optional[str] = None):
    """输出JSON格式"""
    data = [asdict(task) for task in tasks]
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"Output written to: {output_file}")
    else:
        print(json_str)


def output_markdown(tasks: List[SchedulerTask], output_file: Optional[str] = None):
    """输出Markdown格式"""
    lines = []
    lines.append("# 调度任务清单\n")
    lines.append(f"**任务总数**: {len(tasks)}\n")
    lines.append("## 任务列表\n")
    lines.append("| 序号 | 类名 | 业务域 | 实现接口 | 依赖数 | 方法数 |")
    lines.append("|-----|------|--------|---------|--------|--------|")
    
    for i, task in enumerate(tasks, 1):
        implements_str = ', '.join(task.implements) if task.implements else '-'
        lines.append(f"| {i} | {task.class_name} | {task.business_domain or '-'} | {implements_str} | {len(task.dependencies)} | {len(task.methods)} |")
    
    lines.append("\n## 详细信息\n")
    
    for task in tasks:
        lines.append(f"\n### {task.class_name}\n")
        lines.append(f"- **包名**: `{task.package}`")
        lines.append(f"- **文件路径**: `{task.file_path}`")
        lines.append(f"- **业务域**: {task.business_domain or '未识别'}")
        
        if task.implements:
            lines.append(f"- **实现接口**: {', '.join(task.implements)}")
        
        if task.extends:
            lines.append(f"- **继承类**: {task.extends}")
        
        if task.annotations:
            lines.append(f"- **注解**: {', '.join(task.annotations)}")
        
        if task.dependencies:
            lines.append("- **依赖注入**:")
            for dep in task.dependencies:
                if dep.get('injection_type') == '@Value':
                    lines.append(f"  - `{dep['name']}`: {dep['type']} (配置: {dep.get('config_key', '-')})")
                else:
                    lines.append(f"  - `{dep['name']}`: {dep['type']}")
        
        lines.append("")
    
    markdown_str = '\n'.join(lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_str)
        print(f"Output written to: {output_file}")
    else:
        print(markdown_str)


def output_csv(tasks: List[SchedulerTask], output_file: Optional[str] = None):
    """输出CSV格式"""
    import csv
    
    fieldnames = ['class_name', 'package', 'business_domain', 'implements', 'extends', 'dependency_count', 'file_path']
    
    if output_file:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for task in tasks:
                writer.writerow({
                    'class_name': task.class_name,
                    'package': task.package,
                    'business_domain': task.business_domain or '',
                    'implements': ', '.join(task.implements),
                    'extends': task.extends or '',
                    'dependency_count': len(task.dependencies),
                    'file_path': task.file_path
                })
        print(f"Output written to: {output_file}")
    else:
        print(','.join(fieldnames))
        for task in tasks:
            print(f"{task.class_name},{task.package},{task.business_domain or ''},"
                  f"{'|'.join(task.implements)},{task.extends or ''},{len(task.dependencies)},{task.file_path}")


def main():
    parser = argparse.ArgumentParser(description='Extract scheduler information from Java project')
    parser.add_argument('project_path', help='Path to Java project')
    parser.add_argument('--framework-type', choices=['quartz', 'spring-scheduler', 'spring-batch', 'custom'],
                       help='Framework type')
    parser.add_argument('--output-format', choices=['json', 'markdown', 'csv'], default='markdown',
                       help='Output format')
    parser.add_argument('--output-file', help='Output file path')
    parser.add_argument('--include-pattern', default='*.java', help='File include pattern')
    parser.add_argument('--exclude-pattern', nargs='+', help='File exclude patterns')
    
    args = parser.parse_args()
    
    print(f"Analyzing project: {args.project_path}")
    print("Finding Java files...")
    
    java_files = find_java_files(args.project_path, args.include_pattern, args.exclude_pattern)
    print(f"Found {len(java_files)} Java files")
    
    print("Analyzing task files...")
    all_tasks = []
    for i, file_path in enumerate(java_files, 1):
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(java_files)}")
        task = analyze_task_file(file_path)
        if task:
            all_tasks.append(task)
    
    print(f"Analyzed {len(all_tasks)} classes")
    
    print("Filtering scheduler tasks...")
    scheduler_tasks = filter_scheduler_tasks(all_tasks, args.framework_type)
    print(f"Found {len(scheduler_tasks)} scheduler tasks")
    
    print(f"\nGenerating {args.output_format} output...")
    if args.output_format == 'json':
        output_json(scheduler_tasks, args.output_file)
    elif args.output_format == 'markdown':
        output_markdown(scheduler_tasks, args.output_file)
    elif args.output_format == 'csv':
        output_csv(scheduler_tasks, args.output_file)
    
    print("Done!")


if __name__ == '__main__':
    main()
