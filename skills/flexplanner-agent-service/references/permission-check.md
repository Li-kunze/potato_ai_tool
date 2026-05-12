# 权限检查模式

## 完整权限检查流程

```java
/**
 * 获取业务信息列表（带权限检查）
 *
 * @param model 查询条件模型
 * @return 业务信息分页列表
 */
public RestBaseModel<Page<XxxModel>> getXxxList(BaseInfoModel model) {
    RestBaseModel<Page<XxxModel>> restModel = new RestBaseModel<>();

    // 1. 获取用户权限信息
    String userId = PJUserAccessor.getUserDetail().getUserId();
    ScreendInfoModel screenInfoModel = sysRoleItemService.getItemAuthroityWithAclkeyByUser(
        model.getSiteId(), model.getFactoryId(), userId
    );

    // 2. 权限校验
    if (!screenInfoModel.getAllItemFlag() && CollectionUtils.isEmpty(screenInfoModel.getAclKeyList())) {
        return new RestBaseModel<>(PjConstants.HttpStatusSub.SUCCESS, "", null);
    }

    // 3. 设置权限信息到查询模型
    model.setAclKeyList(screenInfoModel.getAclKeyList());
    model.setAllItemFlag(screenInfoModel.getAllItemFlag());

    // 4. 执行查询
    Page<XxxModel> result = xxxRepository.getXxxList(model);

    return new RestBaseModel<>(PjConstants.HttpStatusSub.SUCCESS, "M.W.00000", result);
}
```

## 权限过滤模式

```java
// 在Repository实现类中添加权限过滤
if (!form.getAllItemFlag() && CollectionUtils.isNotEmpty(form.getAclKeyList())) {
    sql.append("AND item_key IN :aclKeyList ");
    map.put("aclKeyList", form.getAclKeyList());
}
```

## 权限字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
|aclKeyList | `List<String>` | ACL 权限列表 |
|allItemFlag | `Boolean` | 是否拥有全部数据权限 |
|userId | `String` | 当前用户ID |
|userCode | `String` | 当前用户代码 |
|siteId | `String` | 站点ID |
|factoryId | `String` | 工厂ID |
