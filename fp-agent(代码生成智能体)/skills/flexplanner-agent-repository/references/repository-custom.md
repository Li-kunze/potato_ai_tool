# Repository Custom 接口模板

```java
package com.ymsl.flexplanner.repository;

import java.util.List;

import org.springframework.data.domain.Page;

import com.ymsl.flexplanner.model.XxxModel;
import com.ymsl.flexplanner.model.SearchConditionForm;

/**
 * 自定义数据仓库接口
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
@Repository
public interface XxxRepositoryCustom {

    /**
     * 分页查询数据列表
     *
     * @param model 查询条件
     * @return 实体分页列表
     */
    Page<XxxModel> getXxxList(String siteId, String factoryId, SearchConditionForm model);

    /**
     * 根据条件查询数据列表
     *
     * @param siteId 站点ID
     * @param form 查询条件
     * @return 实体列表
     */
    List<XxxModel> getXxxListByCondition(String siteId, SearchConditionForm form);

    /**
     * 根据ID查询数据
     *
     * @param siteId 站点ID
     * @param id ID
     * @return 实体
     */
    XxxModel getXxxById(String siteId, String id);
}
```

## 方法命名规范

| 方法名 | 返回类型 | 说明 |
|-------|---------|------|
| getXxxList | Page | 分页查询列表 |
| getXxxListByCondition | List | 按条件查询列表 |
| getXxxById | XxxModel | 查询单个对象 |
| getXxxMap | Map | 查询并转为 Map |

## 返回类型

| 业务场景 | 返回类型 | 示例 |
|---------|-------|------|
| 分页查询 | Page | `Page<XxxModel>` |
| 列表查询 | List | `List<XxxModel>` |
| 单个查询 | Model | `XxxModel` |
| 映射查询 | Map | `Map<String, XxxModel>` |
| 布尔查询 | Boolean | 检查是否存在 |
