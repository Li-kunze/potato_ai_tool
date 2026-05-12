# 任务拆解规则

## 解析 Markdown 需求文档

### 提取关键字段

| 字段 | 位置 | 说明 |
|-----|------|------|
| 代码类型 | 根据需求 | 后台/前台/完整 |
| 表结构 | 后台代码必需 | 表名、字段列表 |
| Entity 类型 | 后台代码必需 | 继承/独立 |
| API 定义 | 后台代码必需 | 路径前缀、方法列表 |
| 前台页面 | 前台/完整代码需 | 页面类型、路径 |

### 任务拆解规则

#### 后台代码 → 5个任务

1. **Entity生成任务**
   - 输入: 表名、字段列表、Entity类型、主键策略
   - 输出: Entity.java

2. **Model生成任务**
   - 输入: Model类型、字段列表
   - 输出: Model.java (2个: InfoModel + ConditionForm)

3. **Repository生成任务**
   - 输入: Entity名、包名、主键类型
   - 输出: Repository.java + Custom.java + Impl.java (3个文件)

4. **Service生成任务**
   - 输入: Repository名、Model名、方法列表
   - 输出: Service.java

5. **Controller生成任务**
   - 输入: Service名、Model名、API前缀、方法列表
   - 输出: Controller.java

#### 前台代码 → 1个任务

6. **Frontend生成任务**
   - 输入: 页面类型、路径、Grid列定义
   - 输出: XXX.html

#### 完整代码 → 6个任务

后台5个 + 前台1个 = 6个任务

## 任务依赖关系

```
Entity → Model → Repository → Service → Controller → Frontend
```

- Entity 可独立
- Model 可与 Entity 并行
- Repository 依赖 Entity
- Service 依赖 Repository 和 Model
- Controller 依赖 Service
- Frontend 依赖 Controller
