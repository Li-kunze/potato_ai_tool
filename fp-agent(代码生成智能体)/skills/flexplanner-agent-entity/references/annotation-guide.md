# 实体注解使用指南

## 类级别注解

### @Entity
标记为 JPA 实体类，必需。

```java
@Entity
public class XxxEntity extends AbstractEntity {
    ...
}
```

### @Table
指定数据库表名。

```java
@Entity
@Table(name = "ddmrp_buffer_result")  // 表名
public class XxxEntity {
    ...
}
```

### @DynamicInsert / @DynamicUpdate（AbstractEntity 实体）
动态 SQL，提高性能。

```java
@DynamicInsert  // 忽略 null 字段
@DynamicUpdate  // 只更新非 null 字段
public class XxxEntity extends AbstractEntity {
    ...
}
```

### @TypeDef（使用 JSONB 时）
定义自定义类型。

```java
@TypeDef(name = "jsonb", typeClass = StageJsonType.class)
public class XxxEntity {
    ...
}
```

## 字段级别注解

### @Id
标记主键字段，必需。

```java
@Id
private String id;
```

### @GeneratedValue
主键生成策略。

```java
// UUID 策略（推荐）
@GeneratedValue(generator = "xxx_uuid")
@GenericGenerator(name = "xxx_uuid", strategy = "uuid")

// 自增策略
@GeneratedValue(strategy = GenerationType.IDENTITY)
```

### @Column
字段映射配置。

```java
// 完整配置
@Column(name = "site_id", nullable = false, length = 40, unique = true)

// 简化配置
private String name;  // 自动映射 snake_case → camelCase

// 长字段
@Column(length = 256)
private String description;

// 小数
@Column(precision = 18, scale = 6)
private BigDecimal amount;

// 非 null
@Column(nullable = false)
private String id;

// 唯一
@Column(unique = true)
private String code;
```

### @Transient
不映射到数据库的字段。

```java
@Transient
private String calculateField;  // 不在表中
```

### @Version
乐观锁版本控制（独立实体）。

```java
@Version
@Column(name = "update_count")
private Integer updateCount;
```

## JSONB 注解

### @TypeDef + @Column

```java
import com.ymsl.flexplanner.dialect.type.StageJsonType;
import com.ymsl.flexplanner.model.JsonBinaryMap;

@Entity
@Table(name = "xxx")
@TypeDef(name = "jsonb", typeClass = StageJsonType.class)
public class XxxEntity extends AbstractEntity {

    @Column(name = "extend_list", columnDefinition = "jsonb")
    private JsonBinaryMap extendList;
}
```

## 日期时间注解

### @JsonFormat

```java
import com.fasterxml.jackson.annotation.JsonFormat;

@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
@Column(name = "create_time", length = 29)
private LocalDateTime createTime;
```

## Lombok 注解

| 注解 | 说明 | 适用场景 |
|-----|------|---------|
| @Getter | 生成 getter | 所有实体 |
| @Setter | 生成 setter | 所有实体 |
| @ToString | 生成 toString | 所有实体 |
| @Data | 同时生成 getter/setter/toString/hashCode/equals | 独立实体 |
| @ToString(callSuper = true) | 包含父类字段 | AbstractEntity 实体 |

## 注解顺序

```java
// 类注解顺序
@Entity
@Table(name = "xxx")
@DynamicInsert
@DynamicUpdate
@TypeDef(...)
@Setter
@Getter
@ToString(callSuper = true)

// 字段注解顺序
@Id
@GeneratedValue(...)
@Column(...)

// Lombok 注解通常放在最后
@Setter
@Getter
@ToString
```
