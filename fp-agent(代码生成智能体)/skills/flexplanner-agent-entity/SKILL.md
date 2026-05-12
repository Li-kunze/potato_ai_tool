---
name: flexplanner-agent-entity
description: 生成FlexPlanner项目的Entity实体类。支持继承AbstractEntity（带审计字段、乐观锁）和独立实体（无审计字段）两种类型。根据数据库表结构生成完整JPA实体，包含字段映射、主键策略、注解、导入顺序等。此skill只包含Entity生成核心逻辑（200行以内），详细模板、类型映射、注解指南等存于references目录按需加载。适用场景: 用户提供数据库表结构，需要生成JPA实体类。Token优化: 主SKILL.md精简，详细模板按需加载references/。
---

# Entity Agent 快速指南

## 支持的Entity类型

### 1. 继承 AbstractEntity

**适用场景**: 需要审计字段的业务表

**继承的审计字段**:
- `createdBy` - 创建人员
- `dateCreated` - 创建时间
- `lastUpdatedBy` - 最后更新人员
- `lastUpdated` - 最后更新时间
- `updatePgmid` - 更新程序ID
- `updateCounter` - 更新计数器（乐观锁）

**注解配置**:
```java
@Entity
@Table(name = "table_name")
@DynamicInsert
@DynamicUpdate
@Setter
@Getter
@ToString(callSuper = true)
public class XxxEntity extends AbstractEntity implements Serializable {
    ...
}
```

### 2. 独立实体

**适用场景**: 字典表、配置表、简单查询表

**特点**: 不继承 AbstractEntity，直接实现 Serializable

**注解配置**:
```java
@Entity
@Table(name = "table_name")
@Setter
@Getter
public class XxxEntity implements Serializable {
    ...
    @Version
    private Integer updateCount;
}
```

## 核心规则

### 字段命名

| 数据库字段名 | Java 字段名 |
|-------------|-----------|
| site_id | siteId |
| factory_id | factoryId |
| item_key | itemKey |
| update_counter | updateCounter |
| create_author | createAuthor |
| date_created | dateCreated |

### 主键策略

| 策略 | 代码 | 适用场景 |
|-----|------|---------|
| UUID | @GeneratedValue(generator = "uuid", strategy = "uuid") | 字符串主键，推荐 |
| 自增 | @GeneratedValue(strategy = GenerationType.IDENTITY) | 数值主键 |
| 手动 | 无 @GeneratedValue | 自定义生成 |

### 数据库类型映射

| 数据库类型 | Java 类型 | @Column length/precision |
|-----------|----------|----------------------|
| VARCHAR | String | length = 具体长度 |
| CHAR | String | length = 具体长度 |
| TEXT | String | columnDefinition = "TEXT" |
| BIGINT | Long | - |
| INTEGER | Integer | - |
| SMALLINT | Integer/SmallInt | length = 1 |
| DECIMAL/NUMERIC | BigDecimal | precision = 18, scale = 6 |
| TIMESTAMP/DATETIME | LocalDateTime | length = 29 |
| DATE | java.sql.Date | length = 10 |
| BOOLEAN | Boolean | - |
| JSONB | JsonBinaryMap | columnDefinition = "jsonb" |

### Lombok 注解

| 注解 | 说明 |
|-----|------|
| @Getter | 生成 getter |
| @Setter | 生成 setter |
| @ToString(callSuper = true) | 继承时使用 |
| @Data | 简化类（独立实体可使用） |

### 导入顺序

```java
// 1. Java 标准库
import java.io.Serializable;
import java.time.LocalDateTime;

// 2. 第三方库
import javax.persistence.*;
import org.hibernate.annotations.*;

// 3. A1 SOLID 框架
import com.ymsl.flexplanner.model.JsonBinaryMap;

// 4. 项目内部
import com.ymsl.flexplanner.entity.AbstractEntity;

// 5. Lombok
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
```

### 常用注解

| 注解 | 说明 |
|-----|------|
| @Entity | 实体类 |
| @Table(name = "xxx") | 表名 |
| @Id | 主键 |
| @Column(name = "xxx") | 字段映射 |
| @GeneratedValue | 主键生成策略 |
| @Transient | 不映射到数据库 |
| @DynamicInsert | 动态插入 |
| @DynamicUpdate | 动态更新 |

### 特殊类型

#### JSONB 字段
```java
@TypeDef(name = "jsonb", typeClass = StageJsonType.class)
@Column(name = "extend_list", columnDefinition = "jsonb")
private JsonBinaryMap extendList;
```

#### 日期字段
```java
@JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8")
@Column(name = "create_time", length = 29)
private LocalDateTime createTime;
```

### 默认值

```java
private BigDecimal amount = BigDecimal.ZERO;
private Long count = 0L;
private Integer status = 0;
```

## 快速判断

```
需要审计字段吗?
├─ Yes → 继承 AbstractEntity
└─ No  → 独立实体

主键类型?
├─ 字符串 (推荐) → UUID 策略
├─ 数值 → IDENTITY 策略
└─ 自定义 → 手动指定
```

## 详细指引

- AbstractEntity 模板: `references/abstract-entity-template.md`
- 独立实体模板: `references/standalone-entity-template.md`
- 类型映射表: `references/type-mapping.md`
- 注解使用指南: `references/annotation-guide.md`
- JSONB 支持: `references/jsonb-support.md`
