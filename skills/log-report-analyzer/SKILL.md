---
name: log-report-analyzer
description: "Generate user login and feature access analysis reports from PostgreSQL database. Analyzes temp_login_log and temp_operation_log tables to create Excel reports with login statistics, top users, and feature usage analysis. Supports configurable user mapping, URL/function filtering, and customizable report parameters."
---

# Log Report Analyzer Skill

生成用户登录及功能访问分析报告的自动化工具。

## 功能

- 查询近30天的用户登录数据
- 分析高频功能访问情况
- 生成带样式的 Excel 报告
- 支持自定义用户映射
- 自动排除共通方法和指定URL/功能

## 使用方法

在 opencode 中直接对话执行：

```
@log-report-analyzer 生成报告
```

或带参数执行：

```
@log-report-analyzer 生成报告 --db-host=10.191.41.157 --db-port=5433 --db-name=flexplanner_all --db-user=flexplanner --db-password=flexplanner@2025
```

## 配置文件

首次运行会在当前目录生成 `log_analyzer_config.yaml` 配置文件：

```yaml
# 数据库配置
database:
  host: "10.191.41.157"
  port: "5433"
  name: "flexplanner_all"
  user: "flexplanner"
  password: "flexplanner@2025"

# 用户映射（用户代码: 中文名称）
user_mapping:
  "APS01": "排产员"
  "DDMRP001": "缓冲计划员"
  # ... 其他用户

# 排除规则
excluded_url_prefixes:
  - "/flexplanner/plugins"
  - "/flexplanner/webetl"
  # ... 其他URL前缀

excluded_function_prefixes:
  - "CommonController."
  - "IndexController."
  # ... 其他功能前缀

# 报告配置
report:
  days: 30  # 统计天数
  top_n: 10  # TOP N 数量
```

## 输出文件

生成 Excel 文件，包含以下 Sheet：

1. **用户登录明细** - 每日登录情况
2. **登录次数TOP10** - 按总登录次数排序
3. **高频功能分析** - 业务功能访问统计（含使用最多的人名）

## 依赖

- Python 3.7+
- psycopg2
- pandas
- openpyxl
- pyyaml
