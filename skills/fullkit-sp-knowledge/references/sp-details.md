# 齐套存储过程详细代码

## 1. simulate_for_fullkit.sql (主入口)

```sql
CREATE OR REPLACE FUNCTION spreadjs.simulate_for_fullkit(ps_site_id character varying, cur_date date)
 RETURNS TABLE(rn_status integer, rs_sql_code character varying, rs_err_code character varying, rs_err_msg character varying)
 LANGUAGE plpgsql
AS $function$
DECLARE
    pre_record          RECORD;
    core_record            RECORD;

BEGIN
    rn_status := 0;
    rs_sql_code := " ";
    rs_err_code := " ";
    rs_err_msg := " ";

    IF ps_site_id IS NULL OR TRIM(ps_site_id) = "" THEN
        rs_err_code := "E.DHP10002";
        rs_err_msg := "Argument Error : [ps_site_id] = " || COALESCE(ps_site_id, "NULL");
        RAISE EXCEPTION " ";
    END IF;
   
    select * into pre_record from simulate_for_fullkit_pre(ps_site_id, cur_date);
    rn_status := pre_record.rn_status;
    rs_sql_code := pre_record.rs_sql_code;
    rs_err_code := pre_record.rs_err_code;
    rs_err_msg := pre_record.rs_err_msg;
    
    IF rn_status = 0 THEN
        NULL;
    ELSE
        RAISE EXCEPTION " ";
    END IF;
    
    select * into core_record from simulate_for_fullkit_core(ps_site_id, cur_date);
    rn_status := core_record.rn_status;
    rs_sql_code := core_record.rs_sql_code;
    rs_err_code := core_record.rs_err_code;
    rs_err_msg := core_record.rs_err_msg;
    
    IF rn_status = 0 THEN
        NULL;
    ELSE
        RAISE EXCEPTION " ";
    END IF;
    
    RETURN NEXT;
    RETURN;
    
EXCEPTION
    WHEN RAISE_EXCEPTION THEN
        IF rn_status <> 0 THEN
            NULL;
        ELSE
            rn_status := -2;
            rs_sql_code := " ";
        END IF;
        RETURN NEXT;
        RETURN;

    WHEN OTHERS THEN
        rn_status := -1;
        rs_sql_code := SQLSTATE;
        rs_err_code := " ";
        rs_err_msg := SQLERRM;
        RETURN NEXT;
        RETURN;
END;
$function$;
```

## 2. simulate_for_fullkit_pre.sql (预处理)

负责初始化数据，包括清空临时表、生成排程信息、期初库存、物料需求和到货信息。

主要调用以下子SP:
- schedule_info_for_fullkit: 生成排程信息
- inv_info_for_fullkit: 生成期初库存
- shortage_info_for_fullkit: 生成物料需求
- supply_info_for_fullkit: 生成到货信息

## 3. simulate_for_fullkit_core.sql (核心处理)

负责执行齐套模拟推演计算，包括:
- 读取系统参数(SIM_DAYS, SIM_DATE)
- 按天循环推演
- 每天处理排程单，判断齐套状态
- 齐套则扣减库存，不齐套则推迟开工日期
- 生成最终结果表

### 核心算法:
```
结余库存 = 期初库存 + 来料数量 - 需求数量
IF 结余库存 >= 0 THEN 齐套 ELSE 不齐套
```

