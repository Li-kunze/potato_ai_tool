# Agent 选择逻辑

## Agent 清单

| Agent | 职责 | Skill 文件 |
|-------|------|----------|
| orchestrator | 需求解析、任务分配 | flexplanner-agent-orchestrator/SKILL.md |
| entity | Entity 实体类生成 | flexplanner-agent-entity/SKILL.md |
| model | Model/DTO 生成 | flexplanner-agent-model/SKILL.md |
| repository | Repository 三层生成 | flexplanner-agent-repository/SKILL.md |
| service | Service 业务层生成 | flexplanner-agent-service/SKILL.md |
| controller | Controller 控制层生成 | (现有) flexplanner-controller-skill/SKILL.md |
| frontend | 前台 Vue2 页面生成 | flexplanner-agent-frontend/SKILL.md |

## 选择规则

### 代码类型 = 后台

触发 Agents: entity, model, repository, service, (controller)

```
需求: 表结构 + API 定义
    │
    ├─→ entity (表结构)
    ├─→ model (表结构)
    ├─→ repository (entity)
    ├─→ service (repository, model)
    └─→ (controller) (service, model, API定义)
```

### 代码类型 = 前台

触发 Agents: frontend

```
需求: 前台页面需求 + 已有 API
    │
    └─→ frontend (页面类型, Grid列, API路径)
```

### 代码类型 = 完整

触发所有 Agents: entity, model, repository, service, (controller), frontend

## Agent 描述

- flexplanner-agent-entity: "生成FlexPlanner项目的Entity实体类。支持继承AbstractEntity和独立实体。根据数据库表结构生成完整JPA实体。"
- flexplanner-agent-model: "生成FlexPlanner项目的Model/DTO类。支持查询表单、数据传输对象、业务聚合模型。"
- flexplanner-agent-repository: "生成FlexPlanner项目的Repository数据访问层。生成JpaRepository接口、自定义接口、实现类。"
- flexplanner-agent-service: "生成FlexPlanner项目的Service业务层。支持标准业务Service，包含查询、保存、更新、删除等方法。"
- flexplanner-agent-frontend: "生成FlexPlanner的Vue2+Ecsort前台页面。支持查询+Grid、表单编辑、侧边栏、弹窗等页面类型。"
