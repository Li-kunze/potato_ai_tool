# 独立实体模板

```java
package com.ymsl.flexplanner.entity;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.Version;

import lombok.Getter;
import lombok.Setter;

/**
 * 实体名称描述
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
@Entity
@Table(name = "table_name")
@Setter
@Getter
public class XxxEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * ID（主键）
     */
    @Id
    @Column(name = "code_dbid", unique = true, nullable = false, length = 40)
    private String codeDbid;

    /**
     * 字段说明
     */
    @Column(name = "code")
    private String code;

    /**
     * 字段说明
     */
    @Column(name = "description")
    private String description;

    /**
     * 字段说明
     */
    @Column(name = "status")
    private String status;

    /**
     * 更新计数
     */
    @Version
    @Column(name = "update_count")
    private Integer updateCount;

    /**
     * 创建人
     */
    @Column(name = "created_by")
    private String createdBy;

    /**
     * 创建时间
     */
    @Column(name = "date_created")
    private LocalDateTime dateCreated;

    /**
     * 最后更新人
     */
    @Column(name = "last_updated_by")
    private String lastUpdatedBy;

    /**
     * 最后更新时间
     */
    @Column(name = "last_updated")
    private LocalDateTime lastUpdated;
}
```

## 关键差异

| 特性 | 继承 AbstractEntity | 独立实体 |
|-----|------------------|---------|
| 继承 | extends AbstractEntity | implements Serializable |
| 审计字段 | 继承获得 | 手动定义 |
| 乐观锁 | updateCounter | updateCount (@Version) |
| 注解 | @DynamicInsert, @DynamicUpdate | 可选 |
| 适用场景 | 业务表 | 字典表、配置表 |
