# 事务处理

## 事务注解

### @Transactional（默认）

```java
@Transactional
public RestBaseModel<XxxModel> saveXxx(XxxModel model) {
    // 默认只回滚 RuntimeException
}
```

### @Transactional(rollbackFor = Exception.class)

```java
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<XxxModel> saveXxx(XxxModel model) {
    // 所有 Exception 都回滚
    // 这是推荐的配置
}
```

### @Transactional(readOnly = true)

```java
@Transactional(readOnly = true)
public Page<XxxModel> getXxxInfo(XxxConditionForm model) {
    // 只读事务，提高性能
    return xxxRepository.getXxxInfo(model);
}
```

## 事务使用场景

| 场景 | 注解 | 说明 |
|-----|------|------|
| 创建操作 | `@Transactional(rollbackFor = Exception.class)` | 事务安全最重要 |
| 更新操作 | `@Transactional(rollbackFor = Exception.class)` | 需要回滚 |
| 删除操作 | `@Transactional(rollbackFor = Exception.class)` | 需要回滚 |
| 批量操作 | `@Transactional(rollbackFor = Exception.class)` | 原子操作 |
| 查询操作 | `@Transactional(readOnly = true)` | 提高性能 |

## 并发控制

```java
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<XxxModel> updateXxx(XxxModel model) {
    XxxEntity entity = xxxRepository.findById(model.getId()).get();
    
    // 乐观锁校验
    if (model.getUpdateCounter() != entity.getUpdateCounter()) {
        return new RestBaseModel<>(
            PjConstants.HttpStatusSub.INITIAL,
            "数据已被其他用户修改，请重新查询!"
        );
    }
    
    BeanUtils.copyProperties(model, entity);
    xxxRepository.save(entity);
    
    return new RestBaseModel<>(PjConstants.HttpStatusSub.SUCCESS, "更新成功");
}
```

## 事务传播级别

| 传播级别 | 说明 |
|---------|------|
| REQUIRED（默认） | 如果存在事务则加入，否则新建 |
| REQUIRES_NEW | 总是新建事务，挂起当前事务 |
| SUPPORTS | 如果存在事务 则加入，否则无需事务 |

```java
@Transactional(rollbackFor = Exception.class)
public void saveBatch(List<XxxModel> list) {
    // REQUIRED 级别
    xxxRepository.saveAll(list);
}

@Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRES_NEW)
public void writeLog(XxxModel model) {
    // REQUIRES_NEW 级别
    xxxRepository.save(model);
}
```
