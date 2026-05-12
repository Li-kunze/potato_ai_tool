# SQL 查询模式

## 单表查询

```java
sql.append("SELECT item_key, item_name, status ");
sql.append("FROM items ");
sql.append("WHERE site_id = :siteId ");
sql.append("  AND factory_id = :factoryId ");
```

## 多表连接（JOIN）

```java
sql.append("SELECT i.item_key, i.item_name, b.buffer_model ");
sql.append("FROM items i ");
sql.append("LEFT JOIN ddmrp_buffer_result b ");
sql.append("  ON i.item_key = b.item_key ");
sql.append("WHERE i.site_id = :siteId ");
```

## 聚合查询

```java
sql.append("SELECT item_key, SUM(quantity) as totalQuantity ");
sql.append("FROM xxx ");
sql.append("WHERE site_id = :siteId ");
sql.append("GROUP BY item_key ");
```

## 分页查询

```java
// 在 queryForPagingList 中自动完成分页
queryForPagingList(sql, map, XxxModel.class, currentPage, currentPageSize);
```

## IN 查询

```java
sql.append("AND status IN :statusList ");
map.put("statusList", Arrays.asList("1", "2", "3"));
```

## 条件查询（动态）

```java
if (StringUtils.isNotBlankText(form.getItemKey())) {
    sql.append("AND item_key = :itemKey ");
    map.put("itemKey", form.getItemKey());
}

if (CollectionUtils.isNotEmpty(form.getStatusList())) {
    sql.append("AND status IN :statusList ");
    map.put("statusList", form.getStatusList());
}
```

## 排序（ORDER BY）

```java
sql.append("ORDER BY item_key ");
sql.append("LIMIT :pageSize ");
sql.append("OFFSET :offset ");
```

## CTE（WITH）

```java
sql.append("WITH t_all AS ( ");
sql.append("  SELECT * FROM xxx WHERE site_id = :siteId ");
sql.append("), ");
sql.append("t_total AS ( ");
sql.append("  SELECT COUNT(*) FROM t_all ");
sql.append(") ");
sql.append("SELECT * FROM t_all ");
```

## DISTINCT

```java
sql.append("SELECT DISTINCT item_key ");
sql.append("FROM xxx ");
```

## CASE WHEN

```java
sql.append("SELECT ");
sql.append("  CASE ");
sql.append("    WHEN status = '1' THEN '正常' ");
sql.append("    WHEN status = '0' THEN '停用' ");
sql.append("    ELSE '未知' ");
sql.append("  END as statusName ");
sql.append("FROM xxx ");
```

## 子查询

```java
sql.append("SELECT * FROM items ");
sql.append("WHERE item_key IN ( ");
sql.append("  SELECT DISTINCT item_key FROM xxx WHERE site_id = :siteId ");
sql.append(") ");
```

## 模糊查询（LIKE）

```java
sql.append("AND item_name LIKE :itemName ");
map.put("itemName", "%" + form.getItemName() + "%");
```

## 日期范围查询

```java
sql.append("AND create_date BETWEEN :dateFrom AND :dateTo ");
map.put("dateFrom", form.getDateFrom());
map.put("dateTo", form.getDateTo());
```
