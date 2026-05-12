# Repository 接口模板

## JpaRepository 标准接口

```java
package com.ymsl.flexplanner.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.ymsl.flexplanner.entity.XxxEntity;
import com.ymsl.flexplanner.repository.XxxRepositoryCustom;

/**
 * 数据仓库接口
 *
 * @since YYYY/MM/DD
 * @author YourName
 */
@Repository
public interface XxxRepository extends JpaRepository<XxxEntity, String>, XxxRepositoryCustom {

    /**
     * 根据站点ID查询所有记录
     *
     * @param siteId 站点ID
     * @return 实体列表
     */
    List<XxxEntity> findAllBySiteId(String siteId);

    /**
     * 根据主键ID查询记录
     *
     * @param id 主键ID
     * @return Optional 实体
     */
    Optional<XxxEntity> findById(String id);

    /**
     * 根据条件查询记录
     *
     * @param siteId 站点ID
     * @param factoryId 工厂ID
     * @return 实体列表
     */
    List<XxxEntity> findAllBySiteIdAndFactoryId(String siteId, String factoryId);
}
```

## 常用命名查询方法

| 方法名 | 说明 | 示例 |
|-------|------|------|
| findAllByXxx | 查询所有符合条件的记录 | `findAllBySiteId(String siteId)` |
| findByXxx | 查询单个符合条件的记录 | `findById(String id)` |
| countByXxx | 统计符合条件的记录数 | `countBySiteId(String siteId)` |
| existsByXxx | 判断记录是否存在 | `existsById(String id)` |

## 主键类型

| 主键类型 | JpaRepository 继承 | 示例 |
|---------|-------------------|------|
| String | JpaRepository<XxxEntity, String> | 字符串主键 |
| Long | JpaRepository<XxxEntity, Long> | 数值主键 |
| Integer | JpaRepository<XxxEntity, Integer> | 整数主键 |

## 注解说明

| 注解 | 说明 | 是否必需 |
|-----|------|---------|
| @Repository | 标记为 Spring 组件 | 必需 |
| @Override | 覆盖父类方法 | 可选 |
