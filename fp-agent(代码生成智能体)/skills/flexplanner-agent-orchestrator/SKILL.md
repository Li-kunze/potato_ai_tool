---
name: flexplanner-agent-orchestrator
description: FlexPlanner多Agent协调器。解析Markdown需求文档，识别代码类型（后台/前台/完整），拆解为独立任务单元，根据任务类型选择对应的Agent skill执行。此skill只负责任务分配、结果汇总，不包含任何代码模板。Token优化: SKILL.md只包含核心调度逻辑（300行以内），详细任务定义、Agent选择规则存于references目录按需加载。适用场景: 用户@需求文档，自动分配给entity/model/repository/service/frontend等Agent执行完整代码链生成。
---

# FlexPlanner Agent 协调器

## 工作流程

```
需求文档 (Markdown)
    │
    ↓ 解析
识别代码类型 (后台/前台/完整)
    │
    ↓ 任务拆解
将需求分解为独立任务单元
    │
    ↓ Agent 分配
根据任务类型选择对应 Agent
    │
    ↓ 执行 & 调度
协调 Agents 按依赖关系执行
    │
    ↓ 结果汇总
收集所有 Agent 生成结果并整合
```

## 代码类型判断

从需求文档提取"代码类型"字段：

| 代码类型 | 生成内容 | 包含的 Agents |
|---------|---------|-------------|
| 后台 | Entity + Model + Repository + Service + Controller | entity, model, repository, service, (controller-skill) |
| 前台 | 前台页面 | frontend |
| 完整 | 后台 + 前台 | 所有 Agents |

## Agent 映射规则

| 任务类型 | Agent Skill | 触发条件 | 依赖 |
|---------|-----------|---------|------|
| Entity生成 | `flexplanner-agent-entity` | 需求中有表结构定义 | 无 |
| Model生成 | `flexplanner-agent-model` | 需要数据传输对象 | Entity (可选) |
| Repository生成 | `flexplanner-agent-repository` | 需要数据访问层 | Entity |
| Service生成 | `flexplanner-agent-service` | 需要业务逻辑层 | Repository, Model |
| Controller生成 | (现有controller-skill) | 需要 API 接口 | Service, Model |
| Frontend生成 | `flexplanner-agent-frontend` | 需要前台页面 | Controller |
| Logic生成 | (可选，暂不创建) | 需要复杂计算逻辑 | Service, Repository |

## 依赖关系调度

```
Entity (可独立)
    ↓
Model (可并行于 Entity)
    ↓
Repository (依赖 Entity)
    ↓
Service (依赖 Repository + Model)
    ↓
Controller (依赖 Service)
    ↓
Frontend (依赖 Controller 的 API 路径)

Logic: 可独立或依赖 Service/Repository
```

## 调度策略

### 串行调度（有依赖关系）
```
1. entity-generator.execute()
2. model-generator.execute()
3. repository-generator.execute()
4. service-generator.execute()
5. controller-generator.execute()
6. frontend-generator.execute() (如需)
```

### 并行调度（无依赖关系）
```
entity-generator    model-generator
    │                      │
    └─────────┬────────────┘
              ↓
    repository-generator.execute()
```

## 结果汇总格式

```markdown
## 代码生成完成

### 生成文件统计
- 实体类: 1 个
- 模型类: 2 个
- Repository: 3 个 (接口 + 自定义接口 + 实现)
- Service: 1 个
- Controller: 1 个
- 前台页面: 1 个
- 总计: 8 个文件

### 文件路径列表
1. flexplanner-domain/entity/XxxEntity.java
2. flexplanner-domain/model/XxxModel.java
3. flexplanner-domain/model/XxxConditionForm.java
4. flexplanner-domain/repository/XxxRepository.java
5. flexplanner-domain/repository/XxxRepositoryCustom.java
6. flexplanner-domain/repository/impl/XxxRepositoryImpl.java
7. flexplanner-domain/service/XxxService.java
8. flexplanner-web/web/app/controller/XxxController.java
9. flexplanner-web/src/main/webapp/views/XXX/XXX_01.html
```

## 错误处理

- **需求文档格式错误**: 返回具体缺失字段说明
- **Agent 执行失败**: 记录错误信息，继续执行其他 Agent
- **部分完成**: 汇总成功/失败文件列表

## 详细指引

- 任务拆解规则: 见 `references/task-decomposition.md`
- Agent 选择逻辑: 见 `references/agent-selection.md`
- 结果汇总模板: 见 `references/result-summary.md`
