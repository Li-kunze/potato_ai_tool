# 齐套SP常见问题

## Q1: 齐套模拟的推演天数在哪里配置？

在 mst_code 表中配置，code_id = "SIM_DAYS"。

## Q2: 如何判断一个排程单是否齐套？

查看 fullkit_schedule_info 表的 fullkit_flag 字段：
- 1 = 已齐套
- 0 = 未齐套

## Q3: 齐套模拟的结果存储在哪里？

结果存储在 fullkit_material_shortage_result 表中。

## Q4: 为什么排程单会被推迟？

当物料不满足齐套条件时(期初库存 + 来料数量 < 需求数量)，排程单开工日期会自动推迟一天。

## Q5: 如何重新运行齐套模拟？

调用主入口SP: SELECT * FROM simulate_for_fullkit("工厂ID", CURRENT_DATE);

## Q6: 齐套模拟会修改哪些数据？

- fullkit_schedule_info: 更新齐套标识和开工日期
- fullkit_material_shortage_info: 更新缺料日期
- fullkit_init_inv_info: 扣减库存
- fullkit_supply_info: 标记已扣减的到货
- fullkit_material_shortage_result: 生成结果

## Q7: 模拟过程中出错如何排查？

查看SP返回的错误信息：
- rn_status = -1: SQL错误
- rn_status = -2: 程序逻辑错误
- rs_err_code: 业务错误代码

## Q8: 期初库存是如何计算的？

由 inv_info_for_fullkit SP生成，包括仓库现有库存、在途库存等。

## Q9: 来料信息是如何获取的？

由 supply_info_for_fullkit SP生成，来源包括采购订单、生产订单等。

