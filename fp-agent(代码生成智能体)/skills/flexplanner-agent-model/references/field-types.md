# Model 字段类型说明

## 字段类型列表

| 业务场景 | Java 类型 | 示例 | 备注 |
|---------|---------|------|------|
| 字符串 | String | `private String itemKey;` | 普通文本 |
| 整数 | Integer | `private Integer status;` | 状态、数量（小范围） |
| 长整数 | Long | `private Long count;` | 数量（大范围） |
| 小数 | BigDecimal | `private BigDecimal amount;` | 金额、比例 |
| 日期 | Date | `private Date createDate;` | 日期时间 |
| 日期时间 | LocalDateTime | `private LocalDateTime updateTime;` | LocalDateTime |
| 布尔 | Boolean | `private Boolean allItemFlag;` | 标志位 |
| 列表 | List<String> | `private List<String> aclKeyList;` | 权限列表、ID列表 |
| 映射 | Map<String, Object> | `private Map<String, Object> extendMap;` | 扩展属性 |
| 嵌套对象 | XxxModel | `private ItemInfoModel itemInfo;` | 关联对象 |

## 特殊字段类型

### 权限相关

```java
// ACL 权限列表
private List<String> aclKeyList;

// 全部项标志
private Boolean allItemFlag;

// 用户ID
private String userId;

// 用户代码
private String userCode;
```

### 分页相关

```java
// 当前页码
private Integer currentPage = 1;

// 每页大小
private Integer currentPageSize = 20;

// 排序字段
private String sortField;

// 排序方向
private String sortOrder = "ASC";

// 总记录数（查询返回）
private Long totalRecords;

// 总页数（查询返回）
private Integer totalPages;
```

### 批量操作相关

```java
// 更新列表
private List<XxxModel> updateList;

// 新增列表
private List<XxxModel> insertList;

// 删除列表
private List<XxxModel> deleteList;
```

## 默认值设置

```java
// 初始化空列表
private List<String> aclKeyList = new ArrayList<>();

// 布尔默认值
private Boolean allItemFlag = Boolean.FALSE;

// 数值默认值
private BigDecimal amount = BigDecimal.ZERO;
private Integer count = 0;
private Long quantity = 0L;

// 分页默认值
private Integer currentPage = 1;
private Integer currentPageSize = 20;
```

## 类型转换

| Entity 类型 | Model 类型 | 说明 |
|-----------|----------|------|
| LocalDateTime | Date / LocalDateTime | 保留或转换 |
| Long | Long / Integer | 根据实际使用 |
| BigDecimal | BigDecimal | 精度保持 |
| JsonBinaryMap | Map<String, Object> | JSONB 转换为 Map |
