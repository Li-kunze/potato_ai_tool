# 分页查询完整模板

## 基础分页查询

```java
/**
 * xxx信息查询
 *
 * @param model 查询条件
 * @return 查询结果
 */
@PostMapping(value = "/getInfo.json")
@ResponseBody
public RestBaseModel<Page<XxxInfoModel>> getInfo(@RequestBody XxxInfoModel model) {
    try {
        model.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
        model.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
        Page<XxxInfoModel> page = xxxService.getInfo(model);
        return new RestBaseModel<>(200, "查询成功", page);
    } catch (Exception e) {
        e.printStackTrace();
        return new RestBaseModel<>(500, "查询失败: " + e.getMessage(), null);
    }
}
```

## 接口URL命名规范

| URL示例 | 说明 |
|---------|------|
| `/getInfo.json` | 通用查询接口 |
| `/getDataByPage.json` | 分页查询接口 |
| `/getAllStockOut.json` | 获取全部数据 |
| `/getWorkCenterInfo.json` | 获取工作中心信息 |
| `/api/getOrders` | API风格（无.json后缀） |
| `/api/getAllStockOut.json` | API风格 + .json后缀 |

## 响应模型

```java
// Page<T> 包装的查询结果
RestBaseModel<Page<XxxInfoModel>>

// List<T> 包装的查询结果
RestBaseModel<List<XxxModel>>

// Entity 直接返回
Page<XxxInfoModel>

// List 直接返回
List<XxxModel>

// Map 返回
RestBaseModel<Map<String, Object>>
```

## 状态码说明

| 状态码 | 说明 | 用法 |
|--------|------|------|
| 200 | 成功 | `new RestBaseModel<>(200, "查询成功", page)` |
| 500 | 失败 | `new RestBaseModel<>(500, "查询失败", null)` |

## 实际案例

### LCrpWorkCenterController
```java
@PostMapping(value = "/getWorkCenterInfo.json")
@ResponseBody
public RestBaseModel<Page<LCrpWorkCenterInfoModel>> getWorkCenterInfo(@RequestBody LCrpWorkCenterInfoModel model) {
    try {
        model.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
        model.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
        Page<LCrpWorkCenterInfoModel> page = lCrpWorkCenterService.getWorkCenterInfo(model);
        return new RestBaseModel<>(200, "查询成功", page);
    } catch (Exception e) {
        e.printStackTrace();
        return new RestBaseModel<>(500, "查询失败: " + e.getMessage(), null);
    }
}
```

### MstCategoryInfoController
```java
@RequestMapping(value = "/getDataByPage.json", method = RequestMethod.POST)
@ResponseBody
public Page<CategoryInfoModel> getDataByPage(@RequestBody CategoryInfoModel categoryInfoModel) {
    categoryInfoModel.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
    categoryInfoModel.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
    return mstCategoryInfoService.getDataByPage(categoryInfoModel);
}
```

### StockOutController
```java
@PostMapping(value = "/api/getAllStockOut.json")
@ResponseBody
public RestBaseModel<Page<StockOutModel>> getAllStockOut(@RequestBody BaseInfoModel model) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    return esService.getAllStockOut(siteId, factoryId, model);
}
```
