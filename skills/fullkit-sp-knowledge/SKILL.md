---
name: fullkit-sp-knowledge
description: FlexPlanner项目齐套(预计齐套)存储过程知识库。包含齐套模拟相关的PostgreSQL存储过程说明、数据流、表结构和业务逻辑。用于回答齐套SP相关问题、维护SP代码、理解齐套业务逻辑。当用户询问齐套、预计齐套、fullkit、simulate_for_fullkit相关问题时使用此技能。
---

# 齐套SP知识库

## 概述

齐套(Fullkit)是FlexPlanner项目中的核心功能，用于模拟计算排程单的物料齐套情况。通过推演未来若干天的物料供需情况，判断排程单是否能按期开工。

## 存储过程架构

齐套模拟采用三层架构设计：

### 1. 主入口SP: simulate_for_fullkit

**文件**: `simulate_for_fullkit.sql`

**职责**: 协调调用pre和core两个子SP，是整个齐套模拟的入口点。

**调用链**:
```
simulate_for_fullkit
├── simulate_for_fullkit_pre
└── simulate_for_fullkit_core
```

**参数**:
- `ps_site_id`: 工厂ID
- `cur_date`: 当前日期

**返回值**:
- `rn_status`: 状态码 (0=成功, -1=SQL错误, -2=程序错误)
- `rs_sql_code`: SQL错误代码
- `rs_err_code`: 业务错误代码
- `rs_err_msg`: 错误消息

### 2. 预处理SP: simulate_for_fullkit_pre

**文件**: `simulate_for_fullkit_pre.sql`

**职责**: 初始化齐套模拟所需的基础数据。

**处理步骤**:
1. 清空临时表 `fullkit_material_shortage_temp`
2. 删除历史结果 `fullkit_material_shortage_result`
3. 分析表性能优化
4. 生成排程信息 (`schedule_info_for_fullkit`)
5. 生成期初库存 (`inv_info_for_fullkit`)
6. 生成物料需求信息 (`shortage_info_for_fullkit`)
7. 生成到货信息 (`supply_info_for_fullkit`)

### 3. 核心处理SP: simulate_for_fullkit_core

**文件**: `simulate_for_fullkit_core.sql`

**职责**: 执行齐套模拟推演计算。

**核心逻辑**:
1. 读取系统参数(模拟天数`SIM_DAYS`、模拟日期`SIM_DATE`)
2. 按天循环推演(外层循环)
3. 每天循环处理排程单(内层循环)
4. 对每个排程单:
   - 计算物料需求与供给
   - 判断齐套状态(AMPLE/STOCKOUT)
   - 齐套: 扣减库存，标记齐套标识
   - 不齐套: 推迟开工日期到第二天
5. 生成缺料结果表

## 数据表说明

### 输入表

| 表名 | 说明 |
|------|------|
| `fullkit_schedule_info` | 排程信息表，包含计划开工日期 |
| `fullkit_init_inv_info` | 期初库存表 |
| `fullkit_material_shortage_info` | 物料需求信息表 |
| `fullkit_supply_info` | 到货信息表 |

### 临时/结果表

| 表名 | 说明 |
|------|------|
| `fullkit_material_shortage_temp` | 临时缺料信息表，记录每天推演结果 |
| `fullkit_material_shortage_result` | 最终缺料结果表 |

### 系统参数表

| 参数代码 | 说明 |
|----------|------|
| `SIM_DAYS` | 齐套模拟推演天数 |
| `SIM_DATE` | 齐套模拟日期 |
| `FULLKIT_SIMULATE_DATE` | 当前模拟日期记录 |

## 关键字段说明

### 齐套标识 (is_ample)
- `AMPLE`: 物料充足，齐套
- `STOCKOUT`: 物料短缺，不齐套

### 扣减标识 (deduction_flag)
- `Y`: 已扣减
- `N`: 未扣减

### 齐套标记 (fullkit_flag)
- `1`: 已齐套
- `0`: 未齐套

## 业务规则

1. **齐套判断逻辑**: 期初库存 + 来料 - 使用量 >= 0
2. **不齐套处理**: 开工日期顺延一天，物料需求日期相应推迟
3. **库存扣减**: 齐套的排程单会扣减对应物料的库存
4. **来料扣减**: 齐套时标记已使用的到货记录

## 参考文档

- **SP完整代码**: 参见 `references/sp-details.md`
- **数据流图**: 参见 `references/data-flow.md`
- **常见问题**: 参见 `references/faq.md`

