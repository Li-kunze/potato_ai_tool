# AbstractEntity 模板

```java
package com.ymsl.flexplanner.entity;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import org.hibernate.annotations.DynamicInsert;
import org.hibernate.annotations.DynamicUpdate;
import org.hibernate.annotations.GenericGenerator;

import com.ymsl.flexplanner.entity.AbstractEntity;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

/**
 * 实体名称描述
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
@Entity
@Table(name = "table_name")
@DynamicInsert
@DynamicUpdate
@Setter
@Getter
@ToString(callSuper = true)
public class XxxEntity extends AbstractEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * ID（主键）
     */
    @Id
    @GeneratedValue(generator = "table_name_uuid")
    @GenericGenerator(name = "table_name_uuid", strategy = "uuid")
    @Column(name = "id", unique = true, nullable = false, length = 40)
    private String id;

    /**
     * 字段说明
     */
    @Column(name = "site_id", nullable = false, length = 40)
    private String siteId;

    /**
     * 字段说明
     */
    @Column(name = "factory_id", nullable = false, length = 40)
    private String factoryId;

    /**
     * 字段说明
     */
    @Column(name = "item_key", nullable = false, length = 100)
    private String itemKey;

    /**
     * 字段说明（小数）
     */
    @Column(name = "amount", precision = 18, scale = 6)
    private BigDecimal amount = BigDecimal.ZERO;

    /**
     * 字段说明（整数）
     */
    @Column(name = "quantity")
    private Long quantity = 0L;

    /**
     * 字段说明（时间）
     */
    @Column(name = "create_date", length = 29)
    private LocalDateTime createDate;
}
```

## 关键注解说明

| 注解 | 作用 |
|-----|------|
| `@DynamicInsert` | 动态插入，忽略 null 字段 |
| `@DynamicUpdate` | 动态更新，只更新修改的字段 |
| `@Setter` | Lombok 自动生成 setter |
| `@Getter` | Lombok 自动生成 getter |
| `@ToString(callSuper = true)` | 包含父类字段 |
| `serialVersionUID = 1L` | 序列化版本号 |
