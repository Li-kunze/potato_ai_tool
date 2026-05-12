# Repository Impl 实现类模板

```java
package com.ymsl.flexplanner.repository.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.data.domain.Page;

import com.a1.solid.jpa.query.JpaNativeQuerySupportRepository;
import com.a1.solid.base.util.StringUtils;
import com.a1.solid.base.util.CollectionUtils;
import com.ymsl.flexplanner.model.XxxModel;
import com.ymsl.flexplanner.model.SearchConditionForm;
import com.ymsl.flexplanner.repository.XxxRepositoryCustom;

/**
 * 数据仓库实现类
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
public class XxxRepositoryImpl extends JpaNativeQuerySupportRepository implements XxxRepositoryCustom {

    /**
     * 分页查询数据列表
     *
     * @param siteId 站点ID
     * @param factoryId 工厂ID
     * @param model 查询条件
     * @return 实体分页列表
     */
    @Override
    public Page<XxxModel> getXxxList(String siteId, String factoryId, SearchConditionForm model) {
        StringBuilder sql = new StringBuilder();
        StringBuilder sqlFormWhere = new StringBuilder();
        StringBuilder sqlCount = new StringBuilder();
        Map<String, Object> map = new HashMap<>();

        Pageable pageable = PageRequest.of(model.getCurrentPage() - 1, model.getCurrentPageSize());

        sql.append("SELECT ");
        sql.append("  dbr.buffer_id as bufferId, ");
        sql.append("  dbr.site_id as siteId, ");
        sql.append("  dbr.factory_id as factoryId, ");
        sql.append("  dbr.item_key as itemKey, ");
        sql.append("  dbr.buffer_model as bufferModel ");
        sqlFormWhere.append("FROM ddmrp_buffer_result dbr ");
        sqlFormWhere.append("WHERE dbr.site_id = :siteId ");
        sqlFormWhere.append("  AND dbr.factory_id = :factoryId ");

        if (StringUtils.isNotBlankText(model.getItemKey())) {
            sqlFormWhere.append("  AND dbr.item_key = :itemKey ");
            map.put("itemKey", model.getItemKey());
        }

        if (CollectionUtils.isNotEmpty(model.getBufferModelList())) {
            sqlFormWhere.append("  AND dbr.buffer_model IN :bufferModelList ");
            map.put("bufferModelList", model.getBufferModelList());
        }

        map.put("siteId", siteId);
        map.put("factoryId", factoryId);

        BigInteger queryDataCount = queryForSingle(sqlCount.toString(), map, PageEntityModel.class).getCount();
        
		if (queryDataCount.intValue() != 0) {
	        sqlFormWhere.append("ORDER BY dbr.operate_date DESC");

	        sql.append(sqlFormWhere);

	        List<XxxModel> detailModelList = queryForPagingList(sql.toString(), map, XxxModel.class, pageable);
			return new PageImpl<>(detailModelList, pageable, queryDataCount.intValue());
		} else {
			return new PageImpl<>(Collections.emptyList(), pageable, PjConstants.INT_ZERO);
		}
    }

    /**
     * 根据条件查询数据列表
     *
     * @param siteId 站点ID
     * @param form 查询条件
     * @return 实体列表
     */
    @Override
    public List<XxxModel> getXxxListByCondition(String siteId, SearchConditionForm form) {
        StringBuilder sql = new StringBuilder();
        Map<String, Object> map = new HashMap<>();

        sql.append("SELECT item_key, item_name, status ");
        sql.append("FROM items ");
        sql.append("WHERE site_id = :siteId ");

        map.put("siteId", siteId);

        return queryForList(sql.toString(), map, XxxModel.class);
    }

    /**
     * 根据ID查询数据
     *
     * @param siteId 站点ID
     * @param id ID
     * @return 实体
     */
    @Override
    public XxxModel getXxxById(String siteId, String id) {
        StringBuilder sql = new StringBuilder();
        Map<String, Object> map = new HashMap<>();

        sql.append("SELECT * ");
        sql.append("FROM xxx ");
        sql.append("WHERE site_id = :siteId ");
        sql.append("  AND id = :id ");

        map.put("siteId", siteId);
        map.put("id", id);

        return queryForSingle(sql.toString(), map, XxxModel.class);
    }
}
```

## 方法实现要点

### 1. 构建StringBuilder

```java
StringBuilder sql = new StringBuilder();
Map<String, Object> map = new HashMap<>();

sql.append("SELECT ... ");
sql.append("FROM ... ");
sql.append("WHERE ... ");
```

### 2. 字段别名映射

```java
sql.append("  dbr.buffer_id as bufferId, ");
sql.append("  dbr.item_key as itemKey, ");
sql.append("  dbr.buffer_model as bufferModel ");
```

### 3. 动态条件

```java
if (StringUtils.isNotBlankText(form.getItemKey())) {
    sql.append("  AND dbr.item_key = :itemKey ");
    map.put("itemKey", form.getItemKey());
}
```

### 4. 参数化查询

```java
// 单个参数
map.put("siteId", siteId);

// IN 查询
map.put("bufferModelList", form.getBufferModelList());
```

### 5. 查询方法选择

| 场景 | 方法 | 参数 |
|-----|------|------|
| 单条 | `queryForSingle(...)` | sql, map, resultType |
| 列表 | `queryForList(...)` | sql, map, resultType |
| 分页 | `queryForPagingList(...)` | sql, map, resultType, page, pageSize |

### 6. 工具类方法导入

```java
import com.a1.solid.base.util.StringUtils;
import com.a1.solid.base.util.CollectionUtils;
```

可用方法:
- `StringUtils.isNotBlankText(str)` - 是否非空且非空白
- `StringUtils.isBlankText(str)` - 是否空或空白
- `CollectionUtils.isEmpty(list)` - 是否空
- `CollectionUtils.isNotEmpty(list)` - 是否非空
