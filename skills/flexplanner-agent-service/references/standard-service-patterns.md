# 标准Service方法模式

## 模式1: 分页查询方法

```java
/**
 * 获取业务信息列表
 *
 * @param model 查询条件模型
 * @return 业务信息分页列表
 */
public Page<XxxModel> getXxxInfo(XxxConditionForm model) {
    return xxxRepository.getXxxInfo(model);
}
```

## 模式2: 单个保存/更新方法

```java
/**
 * 保存业务信息
 *
 * @param model 业务模型
 * @param siteId 站点ID
 * @return 保存结果
 */
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<XxxModel> saveXxx(XxxModel model, String siteId) {
    int status = PjConstants.HttpStatusSub.SUCCESS;
    String message = "保存成功!";
    RestBaseModel<XxxModel> restModel = new RestBaseModel<>();

    if (StringUtils.isBlankText(model.getItemKey())) {
        status = PjConstants.HttpStatusSub.INITIAL;
        message = "物料编号不能为空!";
        restModel.setStatus(status);
        restModel.setMessage(message);
        return restModel;
    }

    XxxEntity entity;
    if (StringUtils.isNotEmpty(model.getId())) {
        entity = xxxRepository.findById(model.getId()).get();
        BeanUtils.copyProperties(model, entity);
    } else {
        entity = new XxxEntity();
        BeanUtils.copyProperties(model, entity);
        entity.setSiteId(siteId);
    }

    xxxRepository.save(entity);

    restModel.setStatus(status);
    restModel.setMessage(message);
    return restModel;
}
```

## 模式3: 批量保存/删除方法

```java
/**
 * 批量保存业务信息
 *
 * @param model 保存模型
 * @param siteId 站点ID
 * @return 保存结果
 */
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<SaveItemsModel> saveBatchItems(SaveItemsModel model, String siteId) {
    ...
}
```

## 模式4: Map获取方法

```java
/**
 * 获取业务信息Map
 *
 * @param siteId 站点ID
 * @param factoryId 工厂ID
 * @return Map<key, entity>
 */
public Map<String, XxxModel> getXxxMap(String siteId, String factoryId) {
    Map<String, XxxModel> result = new HashMap<>();
    
    List<XxxEntity> entityList = xxxRepository.findAllBySiteIdAndFactoryId(siteId, factoryId);
    
    if (CollectionUtils.isNotEmpty(entityList)) {
        for (XxxEntity entity : entityList) {
            XxxModel model = new XxxModel();
            BeanUtils.copyProperties(entity, model);
            result.put(entity.getItemKey(), model);
        }
    }
    
    return result;
}
```

## 模式5: Boolean检测方法

```java
/**
 * 检查数据是否存在
 *
 * @param model 查询模型
 * @return true-存在, false-不存在
 */
public Boolean checkDataExist(XxxModel model) {
    Boolean result = Boolean.FALSE;
    
    XxxEntity entity = xxxRepository.findAllBySiteIdAndFactoryIdAndCode(
        model.getSiteId(), model.getFactoryId(), model.getCode()
    );
    
    if (entity != null && StringUtils.isNotEmpty(entity.getCode())) {
        result = Boolean.TRUE;
    }
    
    return result;
}
```

## 模式6: 简单保存方法

```java
/**
 * 更新或新增数据
 *
 * @param model 业务模型
 */
@Transactional(rollbackFor = Exception.class)
public void updateOrNewData(XxxModel model) {
    XxxEntity entity = new XxxEntity();
    
    if (StringUtils.isNotEmpty(model.getId())) {
        entity = xxxRepository.findById(model.getId()).get();
        entity.setActiveStatus(model.getActiveStatus());
        entity.setDesc(model.getDesc());
    } else {
        BeanUtils.copyProperties(model, entity);
    }
    
    xxxRepository.save(entity);
}
```
