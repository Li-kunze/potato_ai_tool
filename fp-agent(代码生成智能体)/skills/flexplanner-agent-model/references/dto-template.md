# 数据传输对象模板

```java
package com.ymsl.flexplanner.model;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

import lombok.Data;

/**
 * 数据传输对象
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
@Data
public class XxxModel implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * ID
     */
    private String id;

    /**
     * 站点ID
     */
    private String siteId;

    /**
     * 工厂ID
     */
    private String factoryId;

    /**
     * 物料编号
     */
    private String itemKey;

    /**
     * 物料名称
     */
    private String itemName;

    /**
     * 缓冲管理方式
     */
    private String bufferModel;

    /**
     * 绿区调整系数
     */
    private BigDecimal greenAdjustFactor;

    /**
     * 黄区调整系数
     */
    private BigDecimal yellowAdjustFactor;

    /**
     * 更新计数
     */
    private Long updateCounter;

    /**
     * 创建时间
     */
    private Date dateCreated;

    /**
     * 最后更新时间
     */
    private Date lastUpdated;
}
```

## 特点

- 字段与 Entity 基本一致（去掉 JPA 注解）
- 使用 `@Data` 注解
- 扁平化嵌套对象
