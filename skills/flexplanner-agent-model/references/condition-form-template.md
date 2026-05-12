# 查询条件表单模板

```java
package com.ymsl.flexplanner.model;

import java.io.Serializable;
import java.util.List;

import lombok.Data;

/**
 * 查询条件表单
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
@Data
public class XxxConditionForm implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 站点ID
     */
    private String siteId;

    /**
     * 工厂ID
     */
    private String factoryId;

    /**
     * 模块ID
     */
    private String moduleId;

    /**
     * 物料编号（查询条件）
     */
    private String itemKey;

    /**
     * 物料名称（查询条件）
     */
    private String itemName;

    /**
     * 状态（查询条件）
     */
    private String status;

    /**
     * ACL 权限列表
     */
    private List<String> aclKeyList;

    /**
     * 全部项标志
     */
    private Boolean allItemFlag = Boolean.FALSE;

    /**
     * 当前页码
     */
    private Integer currentPage = 1;

    /**
     * 每页大小
     */
    private Integer currentPageSize = 20;

    /**
     * 排序字段
     */
    private String sortField;

    /**
     * 排序方向
     */
    private String sortOrder = "ASC";
}
```

## 特点

- 使用 `@Data` 注解
- 设置默认值（currentPage = 1, currentPageSize = 20）
- 包含基础查询字段、分页字段、权限字段
