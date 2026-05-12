# 结果汇总模板

## 成功完成

```markdown
## 代码生成完成

**功能模块**: XXX功能

**代码类型**: 完整 (后台 + 前台)

**生成文件总数**: 8-9 个

### 生成文件列表

**后台代码 (6-8个文件)**
1. ✅ flexplanner-domain/entity/XxxEntity.java
2. ✅ flexplanner-domain/model/XxxModel.java
3. ✅ flexplanner-domain/model/XxxConditionForm.java
4. ✅ flexplanner-domain/repository/XxxRepository.java
5. ✅ flexplanner-domain/repository/XxxRepositoryCustom.java
6. ✅ flexplanner-domain/repository/impl/XxxRepositoryImpl.java
7. ✅ flexplanner-domain/service/XxxService.java
8. ✅ flexplanner-web/web/app/api/ApiXxxController.java

**前台代码 (1个文件)**
9. ✅ flexplanner-web/src/main/webapp/views/XXX/XXX_01.html

### 依赖关系
```
Entity → Model → Repository → Service → Controller → Frontend
```

### 下一步操作
1. 运行构建: `./gradlew clean build`
2. 启动应用: `./gradlew bootRun`
3. 测试功能
```

## 部分完成

```markdown
## 代码生成部分完成

**成功生成**: 5/8 个文件

**生成文件列表**:
1. ✅ flexplanner-domain/entity/XxxEntity.java
2. ✅ flexplanner-domain/model/XxxModel.java
3. ✅ flexplanner-domain/repository/XxxRepository.java
4. ✅ flexplanner-domain/repository/XxxRepositoryCustom.java
5. ✅ flexplanner-domain/repository/impl/XxxRepositoryImpl.java

**失败文件**:
6. ❌ XxxService.java - 缺少方法定义
7. ❌ ApiXxxController.java - 缺少 API 路径定义
8. ❌ XXX_01.html - 缺少前台页面需求

### 建议
请补充需求文档中的 API 定义和前台页面需求。
```

## Agent 执行失败

```markdown
## Agent 执行失败

**失败 Agent**: xxx-agent

**错误信息**: [具体错误]

**原因分析**: [失败原因]

**建议操作**: [如何修复]

将继续执行其他 Agents...
```
