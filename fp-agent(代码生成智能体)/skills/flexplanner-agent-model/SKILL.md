---
name: flexplanner-agent-model
description: 生成FlexPlanner项目的Model/DTO类（数据传输对象）。支持查询条件表单、数据传输对象、业务聚合模型三种类型。根据Entity或需求生成简洁的Model类，包含正确的Lombok注解、字段类型、序列化ID等。此skill只包含Model生成核心逻辑（170行以内），详细模板、字段映射等存于references目录按需加载。适用场景: 用户提供字段列表，需要生成Model类。Token优化: 主SKILL.md精简，详细模板按需加载references/。
---

# Model Agent 快速指南

## 支持的Model类型

### 1. 查询条件表单

**命名**: `XxxConditionForm` 或 `XxxSearchConditionForm`

**用途**: 前端查询条件封装，传递给后台进行分页查询

**字段特点**:
- 包含 siteId, factoryId 等基础查询条件
- 可包含条件字段（如 itemKey, status）
- 可包含分页信息（currentPage, currentPageSize）

### 2. 数据传输对象

**命名**: `XxxModel` 或 `XxxInfoModel`

**用途**: Entity 对应的 Model，在不同层之间传递数据

**字段特点**:
- 字段与 Entity 基本一致（去掉 JPA 注解）
- 使用 Lombok 简化代码
- 扁平化嵌套对象

### 3. 业务聚合模型

**命名**: `XxxModel` 或 `XxxVO`

**用途**: 组合多个实体数据，用于复杂业务场景

**字段特点**:
- 包含来自多个实体的字段
- 包含计算字段或统计字段
- 可能包含嵌套对象或List

## 核心规则

### Lombok 注解选择

| 注解 | 说明 | 使用场景 |
|-----|------|---------|
| @Data | 生成所有方法 | 大多数 Model |
| @Getter / @Setter | 单独生成 getter/setter | 需要特殊处理 |
| @AllArgsConstructor | 生成全参构造器 | VO 模型 |
| @NoArgsConstructor | 生成无参构造器 | VO 模型 |
| @ToString | 生成 toString | 需要自定义 toString |

### 字段类型

| 业务场景 | Java 类型 | 示例 |
|---------|---------|------|
| 字符串 | String | `private String itemKey;` |
| 整数 | Integer / Long | `private Integer status;` |
| 小数 | BigDecimal | `private BigDecimal amount;` |
| 日期 | Date / LocalDateTime | `private Date createDate;` |
| 列表 | List | `private List<String> aclKeyList;` |
| Map | Map | `private Map<String, Object> extendMap;` |
| 布尔 | Boolean | `private Boolean allItemFlag;` |
| 嵌套对象 | XxxModel | `private ItemInfoModel itemInfo;` |

### 常用字段

```java
// 基础查询字段
private String siteId;
private String factoryId;
private String moduleId;

// 分页相关字段
private Integer currentPage = 1;
private Integer currentPageSize = 20;
private String sortField;
private String sortOrder = "ASC";

// 权限相关字段
private List<String> aclKeyList;
private Boolean allItemFlag;
private String userId;
private String userCode;

// 批量操作字段
private List<XxxModel> updateList;
private List<XxxModel> insertList;
private List<XxxModel> deleteList;
```

### 默认值初始化

```java
@Data
public class XxxModel implements Serializable {
    
    private List<String> aclKeyList = new ArrayList<>();
    private Boolean allItemFlag = Boolean.FALSE;
    
    private BigDecimal amount = BigDecimal.ZERO;
    private Integer count = 0;
}
```

### 导入顺序

```java
// 1. Java 标准库
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.List;
import java.util.ArrayList;

// 2. 第三方库
import lombok.Data;

// 3. 项目内部
import com.ymsl.flexplanner.model.XxxModel;
```

### 命名规范

| 需求 | Model 类名 |
|-----|----------|
| Entity → 基础 Model | DdmrpBufferResult → DdmrpBufferResultModel |
| Items → InfoModel | Items → ItemsInfoModel |
| CrpWorkCenter → Model | CrpWorkCenter → CrpWorkCenterModel |
| 查询条件 | XxxConditionForm / XxxSearchConditionForm |
| 详情展示 | XxxDetailModel / XxxInfoModel |
| 批量保存 | SaveXxxModel / XxxRequestModel |

## 快速判断

```
Model 类型?
├─ 查询表单 → XxxConditionForm
├─ 数据传输 → XxxModel / XxxInfoModel
└─ 业务聚合 → XxxVO
```

## 详细指引

- 表单模板: `references/condition-form-template.md`
- DTO 模板: `references/dto-template.md`
- VO 模板: `references/vo-template.md`
- 字段类型: `references/field-types.md`
