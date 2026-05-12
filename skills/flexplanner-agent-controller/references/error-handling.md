# 错误处理模式

## 标准异常处理

```java
try {
    return service.method(params);
} catch (BusinessCodedException e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "操作失败: " + e.getMessage(), null);
} catch (Exception e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "系统错误: " + e.getMessage(), null);
}
```

## ReRunModel返回处理

```java
try {
    return apiSaveLogic.method(params);
} catch (BusinessCodedException e) {
    e.printStackTrace();
    return new ReRunModel();
}
```

## 异常类型

| 异常类型 | 包路径 | 用途 |
|---------|--------|------|
| `BusinessCodedException` | `com.a1.solid.base.exception` | 业务异常（带错误码） |
| `StageBusinessException` | `com.ymsl.flexplanner.exception` | 项目自定义业务异常 |
| `Exception` | `java.lang` | 通用异常 |

## 实际案例

### ApiItemInfoController
```java
try {
    return apiSaveLogic.saveAllItemInfo(siteId, factoryId, checkFlag);
} catch (BusinessCodedException e) {
    e.printStackTrace();
    return new ReRunModel();
}
```

### LCrpWorkCenterController
```java
try {
    model.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
    model.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
    Page<LCrpWorkCenterInfoModel> page = lCrpWorkCenterService.getWorkCenterInfo(model);
    return new RestBaseModel<>(200, "查询成功", page);
} catch (Exception e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "查询失败: " + e.getMessage(), null);
}
```

### ApiStockOutPriorityInfoController
```java
try {
    int count = insertDataLogic.insertData(jsonStrList, PjConstants.infType.XXX_INFO);
    return new RestBaseModel<>(200, count + "条数据同步成功！");
} catch (Exception e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "数据同步失败！");
}
```

### 抛出业务异常（UserController示例）
```java
UserModel userModel = userManageFacade.findUserByUserCode(uc.getSiteId(), uc.getUserCode());
if(userModel == null){
    throw new StageBusinessException("403", null, "系统不存在此用户，请联系系统管理员添加使用账号。");
}
```

## 常见错误消息

| 场景 | 错误消息 |
|------|---------|
| 查询失败 | `"查询失败: " + e.getMessage()` |
| 数据同步失败 | `"数据同步失败！"` |
| 系统错误 | `"系统错误: " + e.getMessage()` |
| 操作失败 | `"操作失败: " + e.getMessage()` |
| 成功消息 | `"查询成功"` 或 `"N条数据同步成功！"` |
