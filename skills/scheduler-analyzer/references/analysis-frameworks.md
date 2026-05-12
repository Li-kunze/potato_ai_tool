# 支持的调度框架类型

## 目录

1. [Quartz 框架](#quartz-框架)
2. [Spring Scheduler](#spring-scheduler)
3. [Spring Batch](#spring-batch)
4. [自研框架](#自研框架)
5. [框架识别速查表](#框架识别速查表)

---

## Quartz 框架

### 核心组件

| 组件 | 类名模式 | 作用 |
|------|---------|------|
| Job | `implements Job` | 任务定义 |
| JobDetail | `JobDetailBuilder` | 任务配置 |
| Trigger | `TriggerBuilder`, `CronTrigger` | 触发器 |
| Scheduler | `Scheduler`, `StdSchedulerFactory` | 调度器 |

### 识别特征

**导入语句**:
```java
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
```

**任务定义**:
```java
public class SampleJob implements Job {
    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        // 任务逻辑
    }
}
```

**配置方式**:
```java
// 编程式配置
JobDetail job = JobBuilder.newJob(SampleJob.class)
    .withIdentity("job1", "group1")
    .build();

Trigger trigger = TriggerBuilder.newTrigger()
    .withIdentity("trigger1", "group1")
    .withSchedule(CronScheduleBuilder.cronSchedule("0/20 * * * * ?"))
    .build();

scheduler.scheduleJob(job, trigger);
```

### 分析要点

1. **查找任务类**: 搜索 `implements Job`
2. **查找触发器**: 搜索 `TriggerBuilder`, `CronScheduleBuilder`
3. **查找调度器配置**: 搜索 `SchedulerFactory`, `StdSchedulerFactory`
4. **提取cron表达式**: 从触发器配置中提取

---

## Spring Scheduler

### 核心注解

| 注解 | 作用 |
|------|------|
| `@EnableScheduling` | 启用调度功能 |
| `@Scheduled` | 标记调度方法 |

### 识别特征

**启用调度**:
```java
@SpringBootApplication
@EnableScheduling
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

**任务定义**:
```java
@Component
public class ScheduledTasks {
    
    @Scheduled(cron = "0 0 1 * * ?")
    public void dailyTask() {
        // 每日凌晨1点执行
    }
    
    @Scheduled(fixedRate = 3600000)
    public void hourlyTask() {
        // 每3600秒执行一次
    }
    
    @Scheduled(fixedDelay = 60000)
    public void minuteTask() {
        // 上次执行结束后60秒执行
    }
    
    @Scheduled(initialDelay = 10000, fixedRate = 60000)
    public void delayedTask() {
        // 启动后延迟10秒，然后每60秒执行
    }
}
```

### 分析要点

1. **查找调度方法**: 搜索 `@Scheduled`
2. **提取触发条件**:
   - `cron`: cron表达式
   - `fixedRate`: 固定间隔（毫秒）
   - `fixedDelay`: 固定延迟（毫秒）
   - `initialDelay`: 初始延迟（毫秒）
3. **查找配置类**: 搜索 `@EnableScheduling`

---

## Spring Batch

### 核心组件

| 组件 | 接口/类 | 作用 |
|------|---------|------|
| Job | `org.springframework.batch.core.Job` | 批处理作业 |
| Step | `org.springframework.batch.core.Step` | 处理步骤 |
| ItemReader | `ItemReader<T>` | 数据读取 |
| ItemProcessor | `ItemProcessor<I, O>` | 数据处理 |
| ItemWriter | `ItemWriter<T>` | 数据写入 |
| JobLauncher | `JobLauncher` | 作业启动器 |

### 识别特征

**导入语句**:
```java
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.item.ItemReader;
import org.springframework.batch.item.ItemProcessor;
import org.springframework.batch.item.ItemWriter;
```

**配置示例**:
```java
@Configuration
@EnableBatchProcessing
public class BatchConfig {
    
    @Bean
    public Job sampleJob(JobBuilderFactory jobs, StepBuilderFactory steps) {
        return jobs.get("sampleJob")
            .start(sampleStep(steps))
            .build();
    }
    
    @Bean
    public Step sampleStep(StepBuilderFactory steps) {
        return steps.get("sampleStep")
            .<InputType, OutputType>chunk(100)
            .reader(reader())
            .processor(processor())
            .writer(writer())
            .build();
    }
}
```

### 分析要点

1. **查找Job配置**: 搜索 `@EnableBatchProcessing`, `JobBuilderFactory`
2. **查找Step定义**: 搜索 `StepBuilderFactory`, `.chunk(`
3. **识别数据流**: 查找 `ItemReader`, `ItemProcessor`, `ItemWriter`
4. **提取批次大小**: 从 `.chunk(n)` 提取

---

## 自研框架

### 常见设计模式

#### 模式1: 接口驱动

```java
// 框架定义
public interface TaskExecutor {
    ExecutionResult execute(TaskContext context);
}

// 业务实现
@Component
public class BusinessTask implements TaskExecutor {
    @Override
    public ExecutionResult execute(TaskContext context) {
        // 业务逻辑
    }
}
```

**识别特征**:
- 自定义接口（如 `*Executor`, `*Task`, `*Job`）
- 统一上下文对象（如 `*Context`, `*Param`）
- 统一结果对象（如 `*Result`, `*Response`）

#### 模式2: 抽象类模板

```java
// 框架抽象类
public abstract class AbstractTask {
    
    public final String run(Object param) {
        // 前置处理
        beforeExecute(param);
        
        // 业务逻辑（子类实现）
        String result = doExecute(param);
        
        // 后置处理
        afterExecute(result);
        
        return result;
    }
    
    protected abstract String doExecute(Object param);
}

// 业务实现
@Component
public class ConcreteTask extends AbstractTask {
    @Override
    protected String doExecute(Object param) {
        // 业务逻辑
    }
}
```

**识别特征**:
- 抽象基类定义流程
- 模板方法模式
- 子类实现具体逻辑

#### 模式3: 注解标记

```java
// 自定义注解
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface ScheduledTask {
    String name();
    String cron();
    String description() default "";
}

// 业务使用
@Component
@ScheduledTask(name = "dataSync", cron = "0 0 2 * * ?")
public class DataSyncTask {
    // 任务逻辑
}
```

**识别特征**:
- 自定义注解（如 `@*Task`, `@*Job`）
- 注解包含调度信息
- 框架通过反射扫描

### 分析要点

1. **查找框架接口/抽象类**: 搜索 `interface`, `abstract class`
2. **查找注解定义**: 搜索 `@interface`
3. **识别上下文类**: 搜索 `Context`, `Param`, `Model` 类
4. **识别结果类**: 搜索 `Result`, `Response`, `Status` 类
5. **查找注册机制**: 搜索工厂类、扫描器、注册表

---

## 框架识别速查表

### 导入包识别

| 导入包 | 框架类型 |
|--------|---------|
| `org.quartz` | Quartz |
| `org.springframework.scheduling` | Spring Scheduler |
| `org.springframework.batch` | Spring Batch |
| `com.xxx.scheduler` / 公司包名 | 自研框架 |

### 关键字识别

| 关键字 | 框架类型 |
|--------|---------|
| `implements Job` | Quartz |
| `@Scheduled` | Spring Scheduler |
| `@EnableBatchProcessing` | Spring Batch |
| `ItemReader/ItemWriter` | Spring Batch |
| `*Executor`, `*Task` 接口 | 自研框架 |
| `@*Task` 自定义注解 | 自研框架 |

### 配置文件识别

| 配置项 | 框架类型 |
|--------|---------|
| `spring.quartz` | Quartz (Spring集成) |
| `spring.batch` | Spring Batch |
| 自定义配置前缀 | 自研框架 |

---

## 混合框架场景

实际项目中可能存在多种框架混用：

```java
// Spring Scheduler 触发 Quartz Job
@Component
public class SchedulerTrigger {
    
    @Autowired
    private Scheduler quartzScheduler;
    
    @Scheduled(cron = "0 0 1 * * ?")
    public void triggerQuartzJobs() throws SchedulerException {
        quartzScheduler.triggerJob(new JobKey("nightlyJob"));
    }
}
```

**分析策略**:
1. 先识别主要框架
2. 查找框架间的集成点
3. 追踪任务调用链
4. 绘制混合架构图
