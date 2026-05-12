# JSONB 支持

## 依赖

确保项目中已引入：
- StageJsonType 类
- JsonBinaryMap 类

## 实体配置

### 类级别注解

```java
import com.ymsl.flexplanner.dialect.type.StageJsonType;
import com.ymsl.flexplanner.model.JsonBinaryMap;

@Entity
@Table(name = "table_name")
@TypeDef(name = "jsonb", typeClass = StageJsonType.class)
@Setter
@Getter
@ToString(callSuper = true)
public class XxxEntity extends AbstractEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    ...
}
```

### 字段配置

```java
/**
 * 扩展列表（JSONB 字段）
 */
@Type(type = "jsonb")
@Column(name = "extend_list", columnDefinition = "jsonb")
private JsonBinaryMap extendList;
```

## 类包结构

```java
// 导入路径
import com.ymsl.flexplanner.dialect.type.StageJsonType;
import com.ymsl.flexplanner.model.JsonBinaryMap;
```

## JSONB 字段特性

- 支持 PostgreSQL JSONB 类型
- 存储结构化 JSON 数据
- 可通过 JPA Query 查询
- 常用字段名：`extend_list`, `extend_data`, `extend_attr`
