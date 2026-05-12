# 齐套数据流说明

## 整体数据流

```
输入参数: ps_site_id, cur_date
    │
    ▼
┌──────────────────────────────┐
│ simulate_for_fullkit         │
│ (主入口SP)                    │
└───────────┬──────────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
┌──────────┐  ┌──────────┐
│   pre    │  │   core   │
│ (预处理)  │  │ (核心)   │
└────┬─────┘  └────┬─────┘
     │             │
     ▼             ▼
┌──────────┐  ┌──────────┐
│数据准备  │  │推演计算  │
└──────────┘  └──────────┘
```

## 预处理阶段

1. 清空临时表和历史数据
2. 生成排程信息 -> fullkit_schedule_info
3. 生成期初库存 -> fullkit_init_inv_info
4. 生成物料需求 -> fullkit_material_shortage_info
5. 生成到货信息 -> fullkit_supply_info

## 核心处理阶段

1. 读取系统参数(SIM_DAYS, SIM_DATE)
2. 外层循环: 按天推演
3. 内层循环: 处理当天排程单
4. 对每个排程单:
   - 计算物料供需情况
   - 判断齐套状态(AMPLE/STOCKOUT)
   - 齐套: 扣减库存，标记齐套标识
   - 不齐套: 推迟开工日期到第二天
5. 生成缺料结果表 -> fullkit_material_shortage_result

## 齐套判断逻辑

```
结余库存 = 期初库存 + 来料数量 - 需求数量

IF 结余库存 >= 0 THEN
    is_ample = "AMPLE" (齐套)
ELSE
    is_ample = "STOCKOUT" (不齐套)
END IF
```

## 数据表关系

- fullkit_schedule_info: 排程主表
- fullkit_material_shortage_info: 物料需求表
- fullkit_init_inv_info: 期初库存表
- fullkit_supply_info: 到货信息表
- fullkit_material_shortage_temp: 临时结果表
- fullkit_material_shortage_result: 最终结果表

