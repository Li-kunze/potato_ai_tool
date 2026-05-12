---
name: flexplanner-agent-service
description: 生成FlexPlanner项目的Service业务层代码。支持标准业务Service、批处理Service等类型。包含查询、保存、更新、删除等常用方法，使用@Repository注入、事务管理、并发控制等。此skill只包含Service生成核心逻辑（210行以内），详细方法模式、事务处理模板等存于references目录按需加载。适用场景: 用户需要生成Service业务层代码。Token优化: 主SKILL.md精简，详细模板按需加载references/。
---

# Service Agent 快速指南

## Service 类型

### 1. 标准业务 Service

**位置**: `com.ymsl.flexplanner.service` 或 `com.ymsl.flexplanner.service/{模块}/`

**命名**: `XxxService`

**注解**: `@Service`

**用途**: 处理核心业务逻辑、数据查询、保存更新等

### 2. 子包业务 Service

**位置**: `com.ymsl.flexplanner.service/{模块}/`

**命名**: `XxxService`

**用途**: 特定业务域的复杂业务逻辑

### 3. 批处理 Service

**位置**: `com.ymsl.flexplanner.service/batchService/`

**命名**: `XxxService`

**用途**: 定时批处理任务或通用服务方法

## 核心组件

### 依赖注入

| 注解 | 类型 | 用途 |
|-----|------|------|
| @Inject | Repository | 依赖注入 Repository 或其他 Service |
| @Service | 类 | 标记为 Spring Service |

```java
@Service
public class XxxService {

    @Inject
    private XxxRepository xxxRepository;

    @Inject
    private YyyService yyyService;
}
```

### 常用方法模式

| 模式 | 方法名 | 返回值 | 说明 |
|-----|-------|--------|------|
| 分页查询 | `getXxxList` | `Page<XxxModel>` | 分页查询列表 |
| 列表查询 | `getXxxListByCondition` | `List<XxxModel>` | 按条件查询列表 |
| 单个查询 | `getXxxById` | `XxxModel` | 查询单个对象 |
| Map 查询 | `getXxxMap` | `Map<String, XxxModel>` | 查询并转为 Map |
| 保存 | `saveXxx` | `RestBaseModel<XxxModel>` | 保存单个对象 |
| 批量保存 | `saveBatchXxx` | `RestBaseModel<List<XxxModel>>` | 批量保存对象 |
| 更新 | `updateXxx` | `RestBaseModel<XxxModel>` | 更新对象 |
| 删除 | `deleteXxx` | `void` 或 `RestBaseModel` | 删除对象 |
| 批量删除 | `deleteBatchXxx` | `void` 或 `RestBaseModel` | 批量删除对象 |

## 返回值类型

| 业务场景 | 返回值类型 | 说明 |
|---------|-----------|------|
| 分页查询 | `Page<T>` | Spring Data 分页对象 |
| 单个查询 | `RestBaseModel<T>` | 标准响应封装 |
| 列表查询 | `List<T>` | 简单列表数据 |
| 保存/更新 | `RestBaseModel<T>` | 包含状态和消息 |
| 删除操作 | `void` 或 `RestBaseModel` | 可选返回值 |
| 批量操作 | `RestBaseModel<T>` | 批量保存/删除 |
| 实体查询 | `Entity` | 直接返回实体 |
| Map 映射 | `Map<K,V>` | 键值对映射 |
| Boolean 检测 | `Boolean` | 是否存在判断 |

## 事务处理

| 注解 | 说明 | 使用场景 |
|-----|------|---------|
| @Transactional(rollbackFor = Exception.class) | 事务回滚（所有异常） | 创建、更新、删除操作 |
| @Transactional(rollbackFor = RuntimeException.class) | 事务回滚（运行时异常） | 默认配置 |
| @Transactional(readOnly = true) | 只读事务 | 查询操作 |

```java
@Transactional(rollbackFor = Exception.class)
public RestBaseModel<XxxModel> saveXxx(XxxModel model) {
    // 业务逻辑
    xxxRepository.save(entity);
    return restModel;
}
```

## 并发控制

```java
// 使用 updateCounter 检查并发修改
if (model.getUpdateCounter() != entity.getUpdateCounter()) {
    message = "数据已被其他用户修改，请重新查询!";
    restModel.setStatus(PjConstants.HttpStatusSub.INITIAL);
    return restModel;
}
```

## 用户上下文

```java
import com.ymsl.flexplanner.security.auth.PJUserAccessor;

// 在 Service 方法中获取当前用户上下文
String siteId = PJUserAccessor.getUserDetail().getSiteId();
String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
String userCode = PJUserAccessor.getUserDetail().getUserCode();
String userId = PJUserAccessor.getUserDetail().getUserId();
```

## 权限检查模式

```java
// 获取用户权限信息
String userId = PJUserAccessor.getUserDetail().getUserId();
ScreendInfoModel screenInfoModel = sysRoleItemService.getItemAuthroityWithAclkeyByUser(
    siteId, factoryId, userId
);

// 权限校验
if (!screenInfoModel.getAllItemFlag() && CollectionUtils.isEmpty(screenInfoModel.getAclKeyList())) {
    return new RestBaseModel<>(PjConstants.HttpStatusSub.SUCCESS, "");
}

// 设置权限信息到查询模型
model.setAclKeyList(screenInfoModel.getAclKeyList());
model.setAllItemFlag(screenInfoModel.getAllItemFlag());
```

## 工具类方法

```java
import com.a1.solid.base.util.StringUtils;
import com.a1.solid.base.util.CollectionUtils;
import com.a1.solid.base.util.BeanUtils;

// 字符串工具
StringUtils.isNotBlankText(str)      // 不为空且不是空白
StringUtils.isBlankText(str)         // 为空或是空白
StringUtils.isEmpty(str)             // 为 null 或空串
StringUtils.isNotEmpty(str)          // 不为 null 且非空
StringUtils.isAllBlank(str1, str2)   // 全部为空白

// 集合工具
CollectionUtils.isEmpty(list)        // 为 null 或空
CollectionUtils.isNotEmpty(list)     // 不为 null 且非空

// 对象映射
BeanUtils.copyProperties(source, target)    // 对象属性复制
```

## 常用常量

```java
import com.ymsl.flexplanner.constants.PjConstants;

PjConstants.HttpStatusSub.SUCCESS   // 成功 (200)
PjConstants.HttpStatusSub.INITIAL  // 初始/失败 (0)
PjConstants.HttpStatusSub.ERROR    // 错误 (500)

PjConstants.STRING_ONE              // "1"
PjConstants.STRING_ZERO             // "0"
PjConstants.SITEID                 // "siteId"
PjConstants.FACTORYID              // "factoryId"
```

## 导入顺序

```java
// 1. Java 标准库
import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;

// 2. 第三方库
import javax.inject.Inject;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.data.domain.Page;

// 3. A1 SOLID 框架类
import com.a1.solid.base.util.CollectionUtils;
import com.a1.solid.base.util.StringUtils;
import com.a1.solid.base.util.BeanUtils;

// 4. 项目内部
import com.ymsl.flexplanner.constants.PjConstants;
import com.ymsl.flexplanner.entity.XxxEntity;
import com.ymsl.flexplanner.model.XxxModel;
import com.ymsl.flexplanner.model.RestBaseModel;
import com.ymsl.flexplanner.repository.XxxRepository;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
```

## 快速判断

```
Service 类型?
├─ 标准业务 → 主 service 包
├─ 特定模块 → service/{模块}/
└─ 批处理 → service/batchService/
```

## 详细指引

- 标准Service模式: `references/standard-service-patterns.md`
- 批量操作模式: `references/batch-operation-patterns.md`
- 事务处理: `references/transaction-handling.md`
- 权限检查: `references/permission-check.md`
