# 数据库类型映射表

## 完整映射

| 数据库类型 | Java 类型 | @Column 配置 | 示例 |
|-----------|---------|-------------|------|
| VARCHAR | String | length = 40 | `@Column(name = "status", length = 1)` |
| CHAR | String | length = 20 | `@Column(name = "code", length = 20)` |
| TEXT | String | columnDefinition = "TEXT" | `@Column(name = "desc", columnDefinition = "TEXT")` |
| BIGINT | Long | - | `@Column(name = "count")` |
| INTEGER | Integer | - | `@Column(name = "status")` |
| SMALLINT | Integer | length = 1 | `@Column(name = "flag", length = 1)` |
| DECIMAL | BigDecimal | precision = 18, scale = 6 | `@Column(name = "amount", precision = 18, scale = 6)` |
| NUMERIC | BigDecimal | precision = 18, scale = 6 | 同上 |
| TIMESTAMP | LocalDateTime | length = 29 | `@Column(name = "create_time", length = 29)` |
| DATETIME | LocalDateTime | length = 29 | 同上 |
| DATE | java.sql.Date | length = 10 | `@Column(name = "birth_date", length = 10)` |
| BOOLEAN | Boolean | - | `@Column(name = "is_active")` |
| JSONB | JsonBinaryMap | columnDefinition = "jsonb" | `@Column(name = "extend_data", columnDefinition = "jsonb")` |

## 长度规范

| 类型 | 常用长度 | 说明 |
|-----|---------|------|
| 字符串 (普通) | 40, 100, 200 | ID、名称等 |
| 字符串 (长文本) | 256, 500 | 描述、备注等 |
| 字符串 (超长) | TEXT, columnDefinition = "TEXT" | 大文本 |
| 日期时间 | 29 | 格式: yyyy-MM-dd HH:mm:ss |
| 日期 | 10 | 格式: yyyy-MM-dd |
| 小数 | precision = 18, scale = 6 | 常见精度 |

## 特殊处理

### JSONB 类型

```java
// 添加类级别注解
@TypeDef(name = "jsonb", typeClass = StageJsonType.class)

// 字段配置
@Column(name = "extend_data", columnDefinition = "jsonb")
private JsonBinaryMap extendData;
```

### 日期格式化

```java
import com.fasterxml.jackson.annotation.JsonFormat;

@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
@Column(name = "create_time", length = 29)
private LocalDateTime createTime;
```

### 省略注解

| 场景 | 可省略的 @Column |
|-----|---------------|
| 主键 | name |
| 字段名与列名相同 | name |
| 精度/默认值 | length/precision/scale |
