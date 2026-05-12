# 调度系统常见模式

## 目录

1. [任务执行模式](#任务执行模式)
2. [参数传递模式](#参数传递模式)
3. [结果处理模式](#结果处理模式)
4. [依赖管理模式](#依赖管理模式)
5. [异常处理模式](#异常处理模式)
6. [数据流模式](#数据流模式)
7. [业务分类模式](#业务分类模式)

---

## 任务执行模式

### 1.1 接口实现模式

调度任务通常通过实现统一接口来定义：

```java
// 通用调度接口模式
public interface JobExecutor {
    String execute(Object param);
}

// 任务实现
@Component
public class SampleTask implements JobExecutor {
    @Override
    public String execute(Object param) {
        // 业务逻辑
        return result;
    }
}
```

**识别特征**:
- 类实现特定接口
- 使用 `@Component` 或类似注解注册
- 包含 `execute` 或 `run` 方法

### 1.2 注解驱动模式

使用注解定义调度任务：

```java
@Component
public class ScheduledTasks {
    
    @Scheduled(cron = "0 0 1 * * ?")
    public void dailyTask() {
        // 每日执行
    }
    
    @Scheduled(fixedRate = 3600000)
    public void hourlyTask() {
        // 每小时执行
    }
}
```

**识别特征**:
- `@Scheduled` 注解
- cron表达式或固定间隔
- 无参数或简单参数

### 1.3 配置驱动模式

通过配置文件定义任务：

```yaml
scheduler:
  jobs:
    - name: dataSync
      cron: "0 0/30 * * * ?"
      class: com.example.DataSyncJob
    - name: reportGen
      cron: "0 0 2 * * ?"
      class: com.example.ReportGenJob
```

**识别特征**:
- YAML/XML 配置文件
- 任务名与类名映射
- 触发条件配置

---

## 参数传递模式

### 2.1 上下文对象模式

通过封装对象传递参数：

```java
public class JobContext {
    private String jobId;
    private Map<String, Object> parameters;
    private Map<String, Object> results;
    // getters/setters
}

// 使用
public String execute(Object param) {
    JobContext context = (JobContext) param;
    String siteId = (String) context.getParameters().get("siteId");
}
```

**识别特征**:
- 统一的上下文类
- Map 结构存储参数
- 支持动态参数

### 2.2 配置注入模式

通过配置属性注入参数：

```java
@Value("${scheduler.defaultSiteId}")
private String defaultSiteId;

@Value("${scheduler.defaultFactoryId}")
private String defaultFactoryId;
```

**识别特征**:
- `@Value` 注解
- 配置文件中的默认值
- 环境相关配置

### 2.3 混合模式

上下文参数 + 配置默认值：

```java
public String execute(Object param) {
    String siteId = extractFromContext(param, "siteId");
    if (StringUtils.isEmpty(siteId)) {
        siteId = defaultSiteId; // 使用配置默认值
    }
}
```

**识别特征**:
- 优先使用传入参数
- 缺失时使用默认值
- 参数校验逻辑

---

## 结果处理模式

### 3.1 结构化结果模式

返回标准化的结果对象：

```java
public class JobResult {
    private boolean success;
    private String message;
    private Map<String, Object> data;
    private LocalDateTime executeTime;
}

// 转换为JSON返回
return JsonUtils.toString(result);
```

**识别特征**:
- 统一的结果类
- 状态码/布尔状态
- JSON序列化

### 3.2 异常驱动模式

通过异常表示失败：

```java
public String execute(Object param) {
    try {
        // 业务逻辑
        return createSuccessResult("执行成功");
    } catch (BusinessException e) {
        return createErrorResult(e.getMessage());
    } catch (Exception e) {
        return createErrorResult("系统错误: " + e.getMessage());
    }
}
```

**识别特征**:
- try-catch 块
- 业务异常 vs 系统异常
- 错误信息封装

### 3.3 状态码模式

使用常量定义结果状态：

```java
public class JobStatus {
    public static final String SUCCESS = "0";
    public static final String SQL_ERROR = "-1";
    public static final String PROGRAM_ERROR = "-2";
    public static final String VALIDATION_ERROR = "-3";
}
```

**识别特征**:
- 常量类定义状态
- 数字或字符串编码
- 分类错误类型

---

## 依赖管理模式

### 4.1 服务注入模式

通过依赖注入使用业务服务：

```java
@Component
public class SampleTask implements JobExecutor {
    
    @Autowired
    private BusinessService businessService;
    
    @Autowired
    private DataRepository dataRepository;
    
    @Override
    public String execute(Object param) {
        // 使用注入的服务
        businessService.process();
    }
}
```

**识别特征**:
- `@Autowired` 或 `@Inject`
- Service/Repository 注入
- 解耦业务逻辑

### 4.2 工厂模式

通过工厂获取执行器：

```java
public class JobFactory {
    public static JobExecutor getExecutor(String jobType) {
        switch (jobType) {
            case "SYNC": return new SyncJobExecutor();
            case "ASYNC": return new AsyncJobExecutor();
            default: throw new IllegalArgumentException();
        }
    }
}
```

**识别特征**:
- 工厂类
- 类型到实现的映射
- 动态创建实例

---

## 异常处理模式

### 5.1 捕获记录模式

捕获异常并记录，不中断流程：

```java
try {
    // 业务逻辑
} catch (Exception e) {
    log.error("任务执行失败", e);
    // 返回错误结果，但不抛出
    return createErrorResult(e.getMessage());
}
```

**识别特征**:
- 打印堆栈跟踪
- 返回错误状态
- 任务继续执行

### 5.2 中断抛出模式

异常时中断并抛出：

```java
try {
    // 业务逻辑
} catch (Exception e) {
    throw new JobExecutionException("任务执行失败", e);
}
```

**识别特征**:
- 抛出运行时异常
- 触发框架重试或告警
- 事务回滚

### 5.3 分级处理模式

根据异常类型不同处理：

```java
try {
    // 业务逻辑
} catch (ValidationException e) {
    // 验证错误，记录并继续
    log.warn("验证失败: {}", e.getMessage());
    return createWarningResult(e.getMessage());
} catch (BusinessException e) {
    // 业务错误，记录并返回
    log.error("业务错误: {}", e.getMessage());
    return createErrorResult(e.getMessage());
} catch (Exception e) {
    // 系统错误，抛出
    log.error("系统错误", e);
    throw new SystemException(e);
}
```

**识别特征**:
- 多 catch 块
- 不同异常不同处理
- 日志级别区分

---

## 数据流模式

### 6.1 ETL 模式

Extract-Transform-Load 流程：

```
[源数据] → [提取] → [转换] → [加载] → [目标表]
```

**典型场景**:
- 数据同步任务
- 数据清洗任务
- 报表生成任务

### 6.2 计算模式

读取数据 → 计算 → 更新结果：

```
[输入表] → [计算逻辑] → [输出表/字段]
```

**典型场景**:
- 统计计算
- 指标更新
- 价格计算

### 6.3 工作流模式

多步骤顺序执行：

```
[步骤1] → [步骤2] → [步骤3] → [完成]
   ↓
[补偿逻辑] (失败时)
```

**典型场景**:
- 订单处理
- 审批流程
- 复杂业务逻辑

### 6.4 事件驱动模式

监听事件并触发处理：

```
[事件源] → [事件监听] → [事件处理] → [状态更新]
```

**典型场景**:
- 消息队列消费
- 文件监听
- 数据库变更监听

---

## 业务分类模式

### 7.1 数据同步类

**特征**:
- 从外部系统获取数据
- 数据格式转换
- 写入本地数据库

**命名模式**:
- `*Sync`, `*Import`, `*Api*Batch`
- `Get*From*`, `Insert*Data`

### 7.2 计算处理类

**特征**:
- 读取业务数据
- 执行计算逻辑
- 更新计算结果

**命名模式**:
- `*Cal`, `*Calc`, `*Compute`
- `*Process`, `*Handler`

### 7.3 数据维护类

**特征**:
- 清理过期数据
- 更新状态字段
- 归档历史数据

**命名模式**:
- `*Clean`, `*Clear`, `*Delete`
- `*Update*Status`, `*Archive`

### 7.4 通知告警类

**特征**:
- 检查业务条件
- 生成通知内容
- 发送消息/邮件

**命名模式**:
- `*Notice`, `*Alert`, `*Mail`
- `*Notification`, `*Reminder`

### 7.5 控制协调类

**特征**:
- 管理其他任务
- 控制执行流程
- 状态监控

**命名模式**:
- `*Control`, `*Manager`, `*Coordinator`
- `*Start`, `*End`, `*Monitor`

---

## 分析检查清单

分析调度任务时，检查以下要点：

- [ ] 任务实现方式（接口/注解/配置）
- [ ] 参数来源（上下文/配置/混合）
- [ ] 结果返回格式（JSON/对象/状态码）
- [ ] 依赖服务（Service/Repository/外部接口）
- [ ] 异常处理策略（捕获/抛出/分级）
- [ ] 数据流向（输入源 → 处理 → 输出目标）
- [ ] 业务分类（同步/计算/维护/通知/控制）
- [ ] 触发条件（cron/固定间隔/事件驱动）
