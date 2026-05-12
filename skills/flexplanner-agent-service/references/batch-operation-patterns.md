# 批量操作模式

## 批量保存

```java
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<SaveItemsModel> saveBatchItems(SaveItemsModel model, String siteId) {
    int status = PjConstants.HttpStatusSub.SUCCESS;
    String message = "保存成功!";
    RestBaseModel<SaveItemsModel> restModel = new RestBaseModel<>();

    List<XxxModel> updateList = model.getUpdateList();
    List<XxxModel> insertList = model.getInsertList();
    List<XxxModel> deleteList = model.getDeleteList();

    List<XxxEntity> updateEntities = new ArrayList<>();
    List<XxxEntity> insertEntities = new ArrayList<>();
    List<XxxEntity> deleteEntities = new ArrayList<>();

    // 处理更新列表
    if (CollectionUtils.isNotEmpty(updateList)) {
        List<String> idList = new ArrayList<>();
        for (XxxModel modelItem : updateList) {
            idList.add(modelItem.getId());
        }

        List<XxxEntity> entities = xxxRepository.findAllById(idList);
        Map<String, XxxEntity> entityMap = new HashMap<>();
        for (XxxEntity entity : entities) {
            entityMap.put(entity.getId(), entity);
        }

        for (XxxModel modelItem : updateList) {
            if (entityMap.containsKey(modelItem.getId())) {
                XxxEntity entity = entityMap.get(modelItem.getId());

                // 并发校验
                if (modelItem.getUpdateCounter() != entity.getUpdateCounter()) {
                    message = "数据已被其他用户修改，请重新查询!";
                    status = PjConstants.HttpStatusSub.INITIAL;
                    break;
                }

                BeanUtils.copyProperties(modelItem, entity);
                updateEntities.add(entity);
            }
        }
    }

    // 处理新增列表
    if (CollectionUtils.isNotEmpty(insertList) && status == PjConstants.HttpStatusSub.SUCCESS) {
        for (XxxModel modelItem : insertList) {
            XxxEntity entity = new XxxEntity();
            BeanUtils.copyProperties(modelItem, entity);
            entity.setSiteId(siteId);
            insertEntities.add(entity);
        }
    }

    // 处理删除列表
    if (CollectionUtils.isNotEmpty(deleteList) && status == PjConstants.HttpStatusSub.SUCCESS) {
        List<String> idList = new ArrayList<>();
        for (XxxModel modelItem : deleteList) {
            idList.add(modelItem.getId());
        }
        deleteEntities = xxxRepository.findAllById(idList);
    }

    // 执行数据库操作
    if (status == PjConstants.HttpStatusSub.SUCCESS) {
        if (CollectionUtils.isNotEmpty(updateEntities)) {
            xxxRepository.saveAll(updateEntities);
        }
        if (CollectionUtils.isNotEmpty(insertEntities)) {
            xxxRepository.saveAll(insertEntities);
        }
        if (CollectionUtils.isNotEmpty(deleteEntities)) {
            xxxRepository.deleteInBatch(deleteEntities);
        }
    }

    restModel.setStatus(status);
    restModel.setMessage(message);
    return restModel;
}
```

## 批量删除

```java
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<String> deleteBatchItems(List<String> idList) {
    RestBaseModel<String> restModel = new RestBaseModel<>();
    
    if (CollectionUtils.isEmpty(idList)) {
        restModel.setStatus(PjConstants.HttpStatusSub.INITIAL);
        restModel.setMessage("删除列表不能为空");
        return restModel;
    }

    List<XxxEntity> entities = xxxRepository.findAllById(idList);
    if (CollectionUtils.isNotEmpty(entities)) {
        xxxRepository.deleteInBatch(entities);
        restModel.setStatus(PjConstants.HttpStatusSub.SUCCESS);
        restModel.setMessage("删除成功");
    } else {
        restModel.setStatus(PjConstants.HttpStatusSub.INITIAL);
        restModel.setMessage("未找到要删除的记录");
    }

    return restModel;
}
```
