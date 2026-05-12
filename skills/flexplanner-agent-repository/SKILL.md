---
name: flexplanner-agent-repository
description: 生成FlexPlanner项目的Repository数据访问层。生成三层代码：JpaRepository接口、自定义接口、实现类。使用JpaNativeQuerySupportRepository，支持queryForSingle、queryForList、queryForPagingList等查询方法。此skill只包含Repository生成核心逻辑（240行以内），详细模板、查询模式、SQL示例等存于references目录按需加载。适用场景: 用户需要生成Repository层代码。Token优化: 主SKILL.md精简，详细模板按需加载references/。
---

# Repository Agent 快速指南

## Repository 三层结构

### 1. XxxRepository（标准接口）

**位置**: `com.ymsl.flexplanner.repository`

**继承**: `JpaRepository<Entity, 主键类型>, XxxRepositoryCustom`

**职责**: Spring Data JPA 提供的标准 CRUD 方法

**命名**: `XxxRepository`

```java
@Repository
public interface XxxRepository extends JpaRepository<XxxEntity, String>, XxxRepositoryCustom {
    
    // Spring Data JPA 自动生成的方法
    List<XxxEntity> findAllBySiteId(String siteId);
    Optional<XxxEntity> findById(String id);
}
```

### 2. XxxRepositoryCustom（自定义接口）

**位置**: `com.ymsl.flexplanner.repository`

**职责**: 自定义查询方法的声明

**命名**: `XxxRepositoryCustom`

```java
@Repository
public interface XxxRepositoryCustom {
    
    Page<XxxModel> getXxxList(String siteId, String factoryId, SearchConditionForm form);
    List<XxxModel> getXxxByCondition(String siteId, SearchConditionForm form);
}
```

### 3. XxxRepositoryImpl（实现类）

**位置**: `com.ymsl.flexplanner.repository.impl`

**继承**: `JpaNativeQuerySupportRepository implements XxxRepositoryCustom`

**职责**: 实现自定义接口，编写原生 SQL 查询

**命名**: `XxxRepositoryImpl`

## 核心方法

### JpaNativeQuerySupportRepository 方法

| 方法名 | 返回类型 | 说明 | 参数 |
|-------|---------|------|------|
| queryForSingle | T | 查询单个对象 | (sql, paramMap, resultType) |
| queryForList | List | 查询列表 | (sql, paramMap, resultType) |
| queryForPagingList | Page | 查询分页列表 | (sql, paramMap, resultType, page, pageSize) |

### 方法使用示例

#### queryForSingle - 查询单个对象

```java
public XxxModel getXxxDetail(String siteId, String itemId) {
    StringBuilder sql = new StringBuilder();
    Map<String, Object> map = new HashMap<>();
    
    sql.append("SELECT item_key, item_name, status FROM items ");
    sql.append("WHERE site_id = :siteId AND item_id = :itemId");
    
    map.put("siteId", siteId);
    map.put("itemId", itemId);
    
    return queryForSingle(sql.toString(), map, XxxModel.class);
}
```

#### queryForList - 查询列表

```java
public List<XxxModel> getXxxList(String siteId) {
    StringBuilder sql = new StringBuilder();
    Map<String, Object> map = new HashMap<>();
    
    sql.append("SELECT item_key, item_name, status FROM items ");
    sql.append("WHERE site_id = :siteId");
    
    map.put("siteId", siteId);
    
    return queryForList(sql.toString(), map, XxxModel.class);
}
```

#### queryForPagingList - 查询分页列表

```java
public Page<XxxModel> getXxxPage(SearchConditionForm form) {
    StringBuilder sql = new StringBuilder();
    Map<String, Object> map = new HashMap<>();
    
    sql.append("SELECT item_key, item_name, status FROM items ");
    sql.append("WHERE site_id = :siteId");
    
    map.put("siteId", form.getSiteId());
    
    return queryForPagingList(
        sql.toString(),
        map,
        XxxModel.class,
        form.getCurrentPage(),
        form.getCurrentPageSize()
    );
}
```

## 核心规则

### SQL 字段别名映射

SQL 查询时必须使用别名，将数据库字段名（下划线）映射到 Model 字段名（驼峰）
且sql使用数据表别名应使用驼峰命名法(ddmrp_buffer_result as dbr)：

```java
sql.append("SELECT ");
sql.append("  dbr.buffer_id as bufferId, ");      // buffer_id → bufferId
sql.append("  dbr.item_key as itemKey, ");        // item_key → itemKey
sql.append("  dbr.site_id as siteId, ");          // site_id → siteId
sql.append("  dbr.buffer_model as bufferModel "); // buffer_model → bufferModel
sql.append("FROM ddmrp_buffer_result dbr ");
```

### 动态条件处理

```java
if (StringUtils.isNotBlankText(form.getItemKey())) {
    sql.append("  AND dbr.item_key = :itemKey ");
    map.put("itemKey", form.getItemKey());
}

if (CollectionUtils.isNotEmpty(form.getBufferModelList())) {
    sql.append("  AND dbr.buffer_model IN :bufferModelList ");
    map.put("bufferModelList", form.getBufferModelList());
}
```

### 参数化查询

```java
// 使用 :paramName 格式
sql.append("WHERE site_id = :siteId");
map.put("siteId", siteId);

// IN 查询
sql.append("AND status IN :statusList");
map.put("statusList", Arrays.asList("1", "2"));
```

### 导入顺序

```java
// 1. Java 标准库
import java.util.List;
import java.util.Map;
import java.util.HashMap;

// 2. 第三方库
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Repository;

// 3. A1 SOLID 框架
import com.a1.solid.jpa.query.JpaNativeQuerySupportRepository;
import com.a1.solid.base.util.StringUtils;
import com.a1.solid.base.util.CollectionUtils;

// 4. 项目内部
import com.ymsl.flexplanner.entity.XxxEntity;
import com.ymsl.flexplanner.model.XxxModel;
import com.ymsl.flexplanner.repository.XxxRepositoryCustom;
```

### 注解使用

```java
@Repository  // 每个 Repository 接口都需要
public interface XxxRepository extends JpaRepository<XxxEntity, String>, XxxRepositoryCustom {
    ...
}

@Repository
public interface XxxRepositoryCustom {
    ...
}
```

## 命名规范

| Entity | Repository | RepositoryCustom | RepositoryImpl |
|--------|-----------|-------------------|--------------|
| DdmrpBufferResult | DdmrpBufferResultRepository | DdmrpBufferResultRepositoryCustom | DdmrpBufferResultRepositoryImpl |
| Items | ItemsRepository | ItemsRepositoryCustom | ItemsRepositoryImpl |
| CrpWorkCenter | CrpWorkCenterRepository | CrpWorkCenterRepositoryCustom | CrpWorkCenterRepositoryImpl |

## SQL 查询模式

### 常用模式

| 模式 | 代码示例 |
|-----|---------|
| 单表查询 | `SELECT * FROM table WHERE site_id = :siteId` |
| 多表连接 | `FROM a JOIN b ON a.id = b.a_id` |
| 列表查询 | `queryForList(...)` |
| 分页查询 | `queryForPagingList(..., currentPage, currentPageSize)` |
| 单条查询 | `queryForSingle(...)` |

## 详细指引

- Repository 接口模板: `references/repository-interface.md`
- Custom 接口模板: `references/repository-custom.md`
- Impl 实现类模板: `references/repository-impl.md`
- 查询模式: `references/query-patterns.md`
