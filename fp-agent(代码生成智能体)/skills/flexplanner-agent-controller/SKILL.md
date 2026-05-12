---
name: flexplanner-agent-controller
description: 生成FlexPlanner项目的Controller层代码。支持API控制器（数据同步）、查询控制器（分页查询）和页面控制器（业务操作）三种类型。包含REST接口定义、请求参数处理、业务逻辑委派。此skill只包含Controller生成核心逻辑（200行以内），详细模板、注解说明、命名规范、错误处理模式等存于references目录按需加载。适用场景: 用户提供需求需要生成Controller层代码，或flexplanner-agent-orchestrator分配Controller生成任务。Token优化: 主SKILL.md精简，详细模板按需加载references/。
---

# FlexPlanner Controller Agent

生成FlexPlanner项目的Controller层代码。

## Controller类型

根据功能需求选择Controller类型:

| 类型 | 命名规范 | URL前缀 | 用途 | 注解方式 |
|------|----------|---------|------|---------|
| **API控制器** | `ApiXxxController` | `/flexplannerApi/xxx` | 数据同步、保存、批量处理 | `@PostMapping` + `@RequestBody` |
| **查询控制器** | `LXxxController` 或 `XxxController` | `/Lxxx` 或 `/xxx` | 分页查询、信息获取 | `@PostMapping(value = "/getInfo.json")` |
| **页面控制器** | `XxxController` | `/xxx` | 业务操作、页面交互 | 方法多样 |

## 核心代码结构

### API控制器
```java
@Controller
@RequestMapping("/flexplannerApi/itemInfo")
public class ApiItemInfoController {

    @Autowired
    private InsertDataLogic insertDataLogic;

    @Autowired
    private ApiSaveLogic apiSaveLogic;

    @PostMapping(value = "/saveAllItemInfo")
    @ResponseBody
    public ReRunModel saveAllItemInfo(@RequestBody ReRunModel reRunModel) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        boolean checkFlag = reRunModel == null ? false : reRunModel.isCheckFlag();
        try {
            return apiSaveLogic.saveAllItemInfo(siteId, factoryId, checkFlag);
        } catch (BusinessCodedException e) {
            e.printStackTrace();
            return new ReRunModel();
        }
    }
}
```

### 查询控制器
```java
@Controller
@RequestMapping("/stockout")
public class StockOutController {

    @Inject
    StockOutService stockOutService;

    @PostMapping(value = "/api/getAllStockOut.json")
    @ResponseBody
    public RestBaseModel<Page<StockOutModel>> getAllStockOut(@RequestBody BaseInfoModel model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        return stockOutService.getAllStockOut(siteId, factoryId, model);
    }
}
```

### 页面控制器
```java
@Controller
@RequestMapping("/order")
public class OrderController {

    @Inject
    OrderService orderService;

    @PostMapping(value = "/api/getOrders")
    @ResponseBody
    public RestBaseModel<List<OrdersModel>> getOrders(@RequestBody Map<String, Object> model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        return orderService.getOrders(siteId, factoryId, item, planFinishDate, orderNo);
    }
}
```

## 必需注解

| 注解 | 用途 | 常见值 |
|------|------|--------|
| `@Controller` | Spring控制器 | - |
| `@RequestMapping("/path")` | 类级别URL映射 | `/flexplannerApi/xxx`, `/xxx`, `/Lxxx` |
| `@PostMapping(value = "/method")` | POST接口 | `/saveAllXxxInfo`, `/api/getInfo.json` |
| `@ResponseBody` | 返回JSON | - |
| `@RequestBody` | 接收JSON参数 | `@RequestBody XxxModel model` |
| `@Inject` | 依赖注入（推荐） | `@Inject XxxService xxxService` |
| `@Autowired` | 依赖注入 | `@Autowired XxxService xxxService` |

## 响应类型

- `RestBaseModel<T>` - 通用响应包装（查询场景）
- `ReRunModel` - API返回模型（数据同步场景）
- `String` - 简单消息返回
- `Page<T>` - 分页结果
- `List<T>` - 列表结果
- `Map<String, Object>` - 键值对结果

## 错误处理

```java
try {
    return businessLogic.method(params);
} catch (BusinessCodedException e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "错误信息", null);
} catch (Exception e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "系统错误", null);
}
```

## 用户上下文获取

```java
String siteId = PJUserAccessor.getUserDetail().getSiteId();
String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
String userId = PJUserAccessor.getUserDetail().getUserId();
String userCode = PJUserAccessor.getUserDetail().getUserCode();
```

## 导入顺序

1. Java 标准库
2. 第三方库（javax.inject, org.springframework, com.a1.solid, com.alibaba等）
3. A1插件（com.ymsl.a1.plugins）
4. 项目内部

## 常见接口模式

1. **数据同步接口**: 接收List<String> JSON列表，调用insertDataLogic
2. **分页查询接口**: 接收Model查询条件，返回Page<T>包装在RestBaseModel
3. **保存处理接口**: 接收ReRunModel，调用Service层处理业务逻辑
4. **业务操作接口**: 接收业务参数，调用Service层返回结果

## 详细参考

- Controller命名规范: [references/naming.md](references/naming.md)
- API控制器模板: [references/api-controller.md](references/api-controller.md)
- 查询控制器模板: [references/query-controller.md](references/query-controller.md)
- 页面控制器模板: [references/page-controller.md](references/page-controller.md)
- 错误处理模式: [references/error-handling.md](references/error-handling.md)
- 分页查询模板: [references/paging-query.md](references/paging-query.md)
- 数据同步模板: [references/data-sync.md](references/data-sync.md)
