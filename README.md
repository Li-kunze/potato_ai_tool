# Agent 与 Skill 完整清单

> 本文档列出了系统中所有可用的 **Agent** 及其使用的 **Skill**。
> 
> **最后更新**: 2026-05-12
> **配置文件**: `opencode.json`

---

## 📋 目录

1. [Agent 类型说明](#agent-类型说明)
2. [Primary Agent (主智能体)](#primary-agent-主智能体)
3. [Subagent (子智能体)](#subagent-子智能体)
4. [Agent 与 Skill 对应关系](#agent-与-skill-对应关系)
5. [Skill 分类详解](#skill-分类详解)

---

## 🎯 Agent 类型说明

在 OpenCode 系统中，Agent 有三种模式 (`mode`)：

| 模式 | 说明 | 调用方式 |
|-----|------|---------|
| **primary** | 主智能体，可以直接与用户交互，接收用户指令 | 用户直接 @ 或系统自动选择 |
| **subagent** | 子智能体，只能被其他 agent 调用，不能直接接收用户指令 | 通过 Task 工具调用 |
| **all** | 既可以作为主智能体也可以作为子智能体 | 两种方式都可以 |

### 调用关系
```
用户
  ↓ (直接交互)
Primary Agent (如: @scheduler-analyze-agent)
  ↓ (通过 Task 工具调用)
Subagent (如: @flexplanner-entity-agent)
  ↓ (通过 Task 工具调用)
Subagent (如: @flexplanner-repository-agent)
```

---

## 🤖 Primary Agent (主智能体)

可以直接与用户交互的 Agent，定义在 `opencode.json` 中：

| Agent 名称 | 模式 | 用途 | 对应 Skill |
|-----------|------|------|-----------|
| **flexplanner-orchestrator-agent** | **primary** | **FlexPlanner 需求协调器** | flexplanner-agent-orchestrator |
| **scheduler-analyze-agent** | **primary** | **系统代码分析专家** | scheduler-analyzer |

### 2. `flexplanner-orchestrator-agent` (FlexPlanner协调器) ⭐
- **模式**: `primary`
- **模型**: `local-qwen/qwen3-coder`
- **用途**: 解析 Markdown 需求文档，拆解任务，调度各专门 agent 生成完整代码链
- **对应 Skill**: `flexplanner-agent-orchestrator`
- **工作流程**:
  1. 解析用户提供的 Markdown 需求文档
  2. 识别代码类型(后台/前台/完整)
  3. 拆解为独立任务单元
  4. 根据依赖关系调度对应的 agent
  5. 汇总所有 agent 的生成结果
- **依赖关系顺序**: 
  ```
  Entity(独立) → Model(可并行) → Repository(依赖Entity) → Service(依赖Repository+Model) → Controller(依赖Service) → Frontend(依赖Controller)
  ```
- **子 Agent**:
  - @flexplanner-entity-agent
  - @flexplanner-model-agent
  - @flexplanner-repository-agent
  - @flexplanner-service-agent
  - @flexplanner-controller-agent
  - @flexplanner-front-agent
- **工具权限**: read, write, edit, task, grep, glob
- **Max Tokens**: 8000

### 3. `scheduler-analyze-agent` (调度系统分析专家) ⭐
- **模式**: `primary`
- **模型**: `local-qwen/qwen3-coder`
- **用途**: 分析复杂调度系统的代码结构，识别调度任务、提取业务逻辑、梳理依赖关系
- **对应 Skill**: `scheduler-analyzer`
- **工作流程**:
  1. 识别项目中的调度框架类型(Quartz/自研/Spring Scheduler等)
  2. 扫描并提取所有调度任务信息
  3. 分析每个任务的业务逻辑和调用链
  4. 追踪数据流向和依赖关系
  5. 生成结构化的分析报告(markdown格式)
- **分析重点**:
  - 业务域分类(MRP/APS/数据同步/计算处理等)
  - 数据表操作(读/写/更新)
  - 服务依赖关系
  - 任务触发条件和执行顺序
- **工具权限**: read, write, edit, task, grep, glob
- **Max Tokens**: 8000

---

## 🔧 Subagent (子智能体)

只能被 Primary Agent 调用的 Agent：

### FlexPlanner 代码生成类

| Agent 名称 | 模式 | 用途 | 对应 Skill |
|-----------|------|------|-----------|
| `flexplanner-entity-agent` | subagent | 生成 JPA Entity 实体类 | flexplanner-agent-entity |
| `flexplanner-model-agent` | subagent | 生成 Model/DTO 数据传输对象 | flexplanner-agent-model |
| `flexplanner-repository-agent` | subagent | 生成 Repository 三层数据访问层 | flexplanner-agent-repository |
| `flexplanner-service-agent` | subagent | 生成 Service 业务层代码 | flexplanner-agent-service |
| `flexplanner-controller-agent` | subagent | 生成 Controller 控制层代码 | flexplanner-agent-controller |
| `flexplanner-front-agent` | subagent | 生成前台页面 | flexplanner-frontend |

#### 5. `flexplanner-entity-agent` (Entity生成)
- **模式**: `subagent`
- **用途**: 生成 FlexPlanner JPA Entity 实体类
- **对应 Skill**: `flexplanner-agent-entity`
- **支持类型**: 继承 AbstractEntity / 独立实体
- **输出目录**: `flexplanner-domain/entity/`
- **工具权限**: write, edit, read, grep, glob

#### 6. `flexplanner-model-agent` (Model生成)
- **模式**: `subagent`
- **用途**: 生成 FlexPlanner Model/DTO 数据传输对象
- **对应 Skill**: `flexplanner-agent-model`
- **支持类型**: 查询表单、数据传输对象、业务聚合模型
- **输出目录**: `flexplanner-domain/model/`
- **工具权限**: write, edit, read, grep, glob

#### 7. `flexplanner-repository-agent` (Repository生成)
- **模式**: `subagent`
- **用途**: 生成 FlexPlanner Repository 三层数据访问层
- **对应 Skill**: `flexplanner-agent-repository`
- **三层结构**: Repository接口 + RepositoryCustom接口 + RepositoryImpl实现类
- **输出目录**: `repository/` 和 `repository/impl/`
- **工具权限**: write, edit, read, grep, glob, bash

#### 8. `flexplanner-service-agent` (Service生成)
- **模式**: `subagent`
- **用途**: 生成 FlexPlanner Service 业务层代码
- **对应 Skill**: `flexplanner-agent-service`
- **支持类型**: 标准业务 Service、批处理 Service
- **输出目录**: `flexplanner-domain/service/`
- **工具权限**: write, edit, read, grep, glob

#### 9. `flexplanner-controller-agent` (Controller生成)
- **模式**: `subagent`
- **用途**: 生成 FlexPlanner Controller 控制层代码
- **对应 Skill**: `flexplanner-agent-controller`
- **输出目录**: `flexplanner-web/web/app/api/`
- **工具权限**: write, edit, read, grep, glob

#### 10. `flexplanner-front-agent` (前台页面生成)
- **模式**: `subagent`
- **用途**: 专门用于生成 FlexPlanner 前台页面
- **对应 Skill**: `flexplanner-frontend`
- **工具权限**: write, edit, read, grep, glob

---

## 🔗 Agent 与 Skill 对应关系

### Primary Agent 与 Skill 对应表

| Primary Agent | 主要 Skill | 辅助 Skill |
|--------------|-----------|-----------|
| @flexplanner-orchestrator-agent | flexplanner-agent-orchestrator | - |
| @scheduler-analyze-agent | scheduler-analyzer | - |

### Subagent 与 Skill 对应表

| Subagent | Skill |
|---------|-------|
| @flexplanner-entity-agent | flexplanner-agent-entity |
| @flexplanner-model-agent | flexplanner-agent-model |
| @flexplanner-repository-agent | flexplanner-agent-repository |
| @flexplanner-service-agent | flexplanner-agent-service |
| @flexplanner-controller-agent | flexplanner-agent-controller |
| @flexplanner-front-agent | flexplanner-frontend |

---

## 🛠️ Skill 分类详解

### FlexPlanner 代码生成类

#### 6. `flexplanner-agent-orchestrator`
- **描述**: FlexPlanner多Agent协调器。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-agent-orchestrator/`

#### 7. `flexplanner-agent-entity`
- **描述**: 生成FlexPlanner项目的Entity实体类。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-agent-entity/`

#### 8. `flexplanner-agent-model`
- **描述**: 生成FlexPlanner项目的Model/DTO类。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-agent-model/`

#### 9. `flexplanner-agent-repository`
- **描述**: 生成FlexPlanner项目的Repository数据访问层。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-agent-repository/`

#### 10. `flexplanner-agent-service`
- **描述**: 生成FlexPlanner项目的Service业务层代码。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-agent-service/`

#### 11. `flexplanner-agent-controller`
- **描述**: 生成FlexPlanner项目的Controller层代码。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-agent-controller/`

#### 12. `flexplanner-frontend`
- **描述**: 创建FlexPlanner项目的Escort前台页面。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/flexplanner-frontend/`

---

### 调度系统分析类

#### 13. `scheduler-analyzer`
- **描述**: 分析复杂调度系统的代码结构。
- **存储位置**: `C:/Users/mid2422/.config/opencode/skills/scheduler-analyzer/`
- **项目级位置**: `D:/potato_project/flexplanner_seat8/scheduler-analyzer/`
- **支持的框架**: Quartz, Spring Scheduler, Spring Batch, 自研框架

---

### 其他 Skill (简要列表)

| Skill | 描述 | 存储位置 |
|-------|------|---------|
| docx | Word文档处理 | `.config/opencode/skills/docx/` |
| pptx | PPT演示文稿处理 | `.config/opencode/skills/pptx/` |
| pdf | PDF操作工具包 | `.config/opencode/skills/pdf/` |
| xlsx | 电子表格处理 | `.config/opencode/skills/xlsx/` |
| browser-use | 浏览器自动化 | `.agents/skills/browser-use/` |
| agent-browser | 浏览器自动化CLI | `.agents/skills/agent-browser/` |
| baoyu-url-to-markdown | URL转Markdown | `.agents/skills/baoyu-url-to-markdown/` |
| webapp-testing | Web应用测试 | `.config/opencode/skills/webapp-testing/` |
| frontend-design | 前端界面设计 | `.config/opencode/skills/frontend-design/` |
| theme-factory | 主题样式工具包 | `.config/opencode/skills/theme-factory/` |
| canvas-design | 视觉艺术创作 | `.config/opencode/skills/canvas-design/` |
| algorithmic-art | 算法艺术生成 | `.config/opencode/skills/algorithmic-art/` |
| slack-gif-creator | Slack GIF创建 | `.config/opencode/skills/slack-gif-creator/` |
| brand-guidelines | Anthropic品牌指南 | `.config/opencode/skills/brand-guidelines/` |
| meeting-minutes | 会议纪要生成 | `.config/opencode/skills/meeting-minutes/` |
| internal-comms | 内部沟通编写 | `.config/opencode/skills/internal-comms/` |
| log-report-analyzer | 日志报告分析 | `.config/opencode/skills/log-report-analyzer/` |
| mcp-builder | MCP服务器开发 | `.config/opencode/skills/mcp-builder/` |
| web-artifacts-builder | Web Artifacts构建 | `.config/opencode/skills/web-artifacts-builder/` |
| skill-creator | Skill创建指南 | `.config/opencode/skills/skill-creator/` |
| find-skills | Skill发现安装 | `.agents/skills/find-skills/` |
| doc-coauthoring | 文档协作编写 | `.agents/skills/doc-coauthoring/` |

---

## 📊 统计汇总

### Agent 统计 (来自 opencode.json)

| 类型 | 数量 | Agent列表 |
|-----|------|----------|
| **Primary Agent** | **3** | personal-knowledge-advisor, flexplanner-orchestrator-agent, scheduler-analyze-agent |
| **Subagent** | **10** | knowledge-retrieval-agent, knowledge-base-manager-agent, conversation-agent, content-synthesizer-agent, flexplanner-entity-agent, flexplanner-model-agent, flexplanner-repository-agent, flexplanner-service-agent, flexplanner-controller-agent, flexplanner-front-agent |
| **总计** | **13** | - |

### Skill 统计

| 分类 | Skill数量 |
|-----|----------|
| 知识库与检索类 | 5 |
| FlexPlanner代码生成类 | 7 |
| 调度系统分析类 | 1 |
| 文档处理类 | 3 |
| 浏览器与网页交互类 | 4 |
| 设计与创意类 | 6 |
| 办公自动化类 | 3 |
| 开发工具类 | 5 |
| 个人助理类 | 1 |
| **总计** | **35** |

---

## 📝 重要说明

### Agent 调用示例

**Primary Agent 调用 Subagent**:
```typescript
task({
  description: "生成Entity代码",
  subagent_type: "flexplanner-entity-agent",
  prompt: "根据以下表结构生成Entity类..."
});
```

**用户调用 Primary Agent**:
```
@scheduler-analyze-agent 分析我项目的调度系统
```

### Agent vs Skill 的区别

- **Agent (智能体)**: 执行任务的实体，定义在 `opencode.json` 中
  - **Primary Agent**: 可以直接与用户交互（3个）
  - **Subagent**: 只能被其他 Agent 调用（10个）
  
- **Skill (技能)**: Agent使用的工具/指南，存储在 `skills/` 目录下

---

*本文档基于 `opencode.json` 配置文件生成。*
