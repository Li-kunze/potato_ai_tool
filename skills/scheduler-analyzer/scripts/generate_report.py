#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成脚本

基于提取的调度信息生成完整的分析报告。

用法:
    python generate_report.py --tasks-file=<tasks.json> --output-file=<report.md>
    python generate_report.py --project-path=<path> --output-file=<report.md>

选项:
    --tasks-file        任务信息JSON文件
    --project-path      项目路径（直接分析）
    --output-file       输出报告文件
    --output-format     输出格式 (markdown/html)
    --template          报告模板 (full/compact)
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict


def load_tasks_data(tasks_file: str) -> List[Dict]:
    """加载任务数据"""
    with open(tasks_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_business_domains(tasks: List[Dict]) -> Dict[str, List[Dict]]:
    """按业务域分组"""
    domains = defaultdict(list)
    
    for task in tasks:
        domain = task.get('business_domain', '未分类')
        domains[domain].append(task)
    
    return dict(domains)


def analyze_dependencies(tasks: List[Dict]) -> Dict[str, Any]:
    """分析依赖统计"""
    stats = {
        'total_dependencies': 0,
        'service_count': 0,
        'repository_count': 0,
        'external_count': 0,
        'config_count': 0,
        'top_dependencies': defaultdict(int)
    }
    
    for task in tasks:
        for dep in task.get('dependencies', []):
            stats['total_dependencies'] += 1
            dep_type = dep.get('type', '')
            
            if 'Service' in dep_type or 'Biz' in dep_type:
                stats['service_count'] += 1
            elif 'Repository' in dep_type or 'Repo' in dep_type or 'Dao' in dep_type:
                stats['repository_count'] += 1
            elif 'Client' in dep_type or 'Api' in dep_type or 'Remote' in dep_type:
                stats['external_count'] += 1
            
            if dep.get('injection_type') == '@Value':
                stats['config_count'] += 1
            
            stats['top_dependencies'][dep_type] += 1
    
    # 排序
    stats['top_dependencies'] = dict(sorted(
        stats['top_dependencies'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10])
    
    return stats


def analyze_naming_patterns(tasks: List[Dict]) -> Dict[str, int]:
    """分析命名模式"""
    patterns = defaultdict(int)
    
    pattern_keywords = {
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
        'Api': 'API同步',
        'Get': '数据获取',
        'Update': '数据更新',
        'Insert': '数据插入',
        'Mrp': 'MRP相关',
        'Aps': 'APS相关',
        'Crp': 'CRP相关',
        'Ddmrp': 'DDMRP相关'
    }
    
    for task in tasks:
        class_name = task.get('class_name', '')
        for keyword, category in pattern_keywords.items():
            if keyword in class_name:
                patterns[category] += 1
                break
    
    return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))


def generate_markdown_report(tasks: List[Dict], project_name: str = "Unknown") -> str:
    """生成Markdown格式报告"""
    lines = []
    
    # 标题
    lines.append(f"# 调度系统分析报告\n")
    lines.append(f"**项目**: {project_name}  ")
    lines.append(f"**分析日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append(f"**任务总数**: {len(tasks)}\n")
    
    # 执行摘要
    lines.append("## 1. 执行摘要\n")
    
    domains = analyze_business_domains(tasks)
    deps_stats = analyze_dependencies(tasks)
    naming_patterns = analyze_naming_patterns(tasks)
    
    lines.append("### 1.1 关键指标\n")
    lines.append(f"- **业务域数量**: {len(domains)}")
    lines.append(f"- **总依赖数**: {deps_stats['total_dependencies']}")
    lines.append(f"- **业务服务依赖**: {deps_stats['service_count']}")
    lines.append(f"- **数据访问依赖**: {deps_stats['repository_count']}")
    lines.append(f"- **外部接口依赖**: {deps_stats['external_count']}")
    lines.append(f"- **配置项数量**: {deps_stats['config_count']}\n")
    
    # 业务域分析
    lines.append("## 2. 业务域分析\n")
    
    for domain_name, domain_tasks in sorted(domains.items()):
        lines.append(f"### 2.{list(domains.keys()).index(domain_name) + 1} {domain_name}\n")
        lines.append(f"**任务数量**: {len(domain_tasks)}\n")
        
        lines.append("| 序号 | 任务名称 | 依赖数 | 方法数 |")
        lines.append("|-----|---------|--------|--------|")
        
        for i, task in enumerate(domain_tasks[:10], 1):  # 只显示前10个
            lines.append(f"| {i} | {task['class_name']} | {len(task.get('dependencies', []))} | {len(task.get('methods', []))} |")
        
        if len(domain_tasks) > 10:
            lines.append(f"| ... | ... ({len(domain_tasks) - 10} more) | ... | ... |")
        
        lines.append("")
    
    # 命名模式分析
    lines.append("## 3. 任务命名模式分析\n")
    lines.append("| 模式 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    
    total_tasks = len(tasks)
    for pattern, count in list(naming_patterns.items())[:10]:
        percentage = (count / total_tasks) * 100
        lines.append(f"| {pattern} | {count} | {percentage:.1f}% |")
    
    lines.append("")
    
    # 依赖分析
    lines.append("## 4. 依赖分析\n")
    
    lines.append("### 4.1 依赖类型分布\n")
    lines.append("```")
    lines.append(f"业务服务:    {'█' * int(deps_stats['service_count'] / max(deps_stats['total_dependencies'], 1) * 50)} {deps_stats['service_count']}")
    lines.append(f"数据访问:    {'█' * int(deps_stats['repository_count'] / max(deps_stats['total_dependencies'], 1) * 50)} {deps_stats['repository_count']}")
    lines.append(f"外部接口:    {'█' * int(deps_stats['external_count'] / max(deps_stats['total_dependencies'], 1) * 50)} {deps_stats['external_count']}")
    lines.append(f"配置注入:    {'█' * int(deps_stats['config_count'] / max(deps_stats['total_dependencies'], 1) * 50)} {deps_stats['config_count']}")
    lines.append("```\n")
    
    lines.append("### 4.2 常用依赖Top10\n")
    lines.append("| 排名 | 依赖类型 | 使用次数 |")
    lines.append("|-----|---------|---------|")
    
    for i, (dep_type, count) in enumerate(deps_stats['top_dependencies'].items(), 1):
        lines.append(f"| {i} | {dep_type} | {count} |")
    
    lines.append("")
    
    # 完整任务清单
    lines.append("## 5. 完整任务清单\n")
    lines.append("| 序号 | 任务名称 | 业务域 | 实现接口 | 依赖数 |")
    lines.append("|-----|---------|--------|---------|--------|")
    
    for i, task in enumerate(tasks, 1):
        implements = ', '.join(task.get('implements', [])[:2])  # 只显示前2个
        if len(task.get('implements', [])) > 2:
            implements += '...'
        lines.append(f"| {i} | {task['class_name']} | {task.get('business_domain', '-')} | {implements or '-'} | {len(task.get('dependencies', []))} |")
    
    lines.append("")
    
    # 附录
    lines.append("## 6. 附录\n")
    
    lines.append("### 6.1 任务详细信息\n")
    
    for task in tasks:
        lines.append(f"#### {task['class_name']}\n")
        lines.append(f"- **包名**: `{task['package']}`")
        lines.append(f"- **业务域**: {task.get('business_domain', '未识别')}")
        
        if task.get('implements'):
            lines.append(f"- **实现接口**: {', '.join(task['implements'])}")
        
        if task.get('extends'):
            lines.append(f"- **继承类**: {task['extends']}")
        
        if task.get('dependencies'):
            lines.append("- **依赖注入**:")
            for dep in task['dependencies']:
                if dep.get('injection_type') == '@Value':
                    lines.append(f"  - `{dep['name']}`: {dep['type']} (配置: `{dep.get('config_key', '-')}`)")
                else:
                    lines.append(f"  - `{dep['name']}`: {dep['type']}")
        
        lines.append("")
    
    return '\n'.join(lines)


def generate_html_report(tasks: List[Dict], project_name: str = "Unknown") -> str:
    """生成HTML格式报告"""
    # 简化版，实际使用可以引入模板引擎
    md_content = generate_markdown_report(tasks, project_name)
    
    # 简单的Markdown转HTML
    html_lines = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <title>调度系统分析报告</title>',
        '    <style>',
        '        body { font-family: Arial, sans-serif; margin: 40px; }',
        '        h1 { color: #333; }',
        '        h2 { color: #666; border-bottom: 2px solid #ddd; padding-bottom: 10px; }',
        '        table { border-collapse: collapse; width: 100%; margin: 20px 0; }',
        '        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }',
        '        th { background-color: #f2f2f2; }',
        '        tr:nth-child(even) { background-color: #f9f9f9; }',
        '        code { background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; }',
        '    </style>',
        '</head>',
        '<body>'
    ]
    
    # 简单转换
    for line in md_content.split('\n'):
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:]}</h4>')
        elif line.startswith('| '):
            # 表格处理
            if not html_lines[-1].startswith('<table'):
                html_lines.append('<table>')
            if '---|' not in line:
                html_lines.append('<tr>')
                for cell in line.split('|')[1:-1]:
                    if html_lines[-2] == '<table>':
                        html_lines.append(f'<th>{cell.strip()}</th>')
                    else:
                        html_lines.append(f'<td>{cell.strip()}</td>')
                html_lines.append('</tr>')
        elif line.startswith('- '):
            if not html_lines[-1].startswith('<ul'):
                html_lines.append('<ul>')
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('```'):
            if not html_lines[-1].startswith('<pre'):
                html_lines.append('<pre><code>')
            else:
                html_lines.append('</code></pre>')
        elif line.strip():
            html_lines.append(f'<p>{line}</p>')
    
    html_lines.extend(['</body>', '</html>'])
    
    return '\n'.join(html_lines)


def main():
    parser = argparse.ArgumentParser(description='Generate scheduler analysis report')
    parser.add_argument('--tasks-file', help='Tasks JSON file')
    parser.add_argument('--project-path', help='Project path to analyze')
    parser.add_argument('--output-file', required=True, help='Output report file')
    parser.add_argument('--output-format', choices=['markdown', 'html'], default='markdown',
                       help='Output format')
    parser.add_argument('--project-name', default='Unknown', help='Project name')
    
    args = parser.parse_args()
    
    # 获取任务数据
    if args.tasks_file:
        print(f"Loading tasks from: {args.tasks_file}")
        tasks = load_tasks_data(args.tasks_file)
    elif args.project_path:
        print(f"Analyzing project: {args.project_path}")
        # 调用extract_scheduler_info.py进行分析
        import subprocess
        import tempfile
        
        temp_output = tempfile.mktemp(suffix='.json')
        cmd = [
            'python', 
            os.path.join(os.path.dirname(__file__), 'extract_scheduler_info.py'),
            args.project_path,
            '--output-format', 'json',
            '--output-file', temp_output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error analyzing project: {result.stderr}")
            return
        
        tasks = load_tasks_data(temp_output)
        os.remove(temp_output)
    else:
        print("Error: Either --tasks-file or --project-path must be provided")
        return
    
    print(f"Loaded {len(tasks)} tasks")
    
    # 生成报告
    print(f"Generating {args.output_format} report...")
    
    if args.output_format == 'markdown':
        report = generate_markdown_report(tasks, args.project_name)
    elif args.output_format == 'html':
        report = generate_html_report(tasks, args.project_name)
    
    # 保存报告
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report saved to: {args.output_file}")
    print("Done!")


if __name__ == '__main__':
    main()
