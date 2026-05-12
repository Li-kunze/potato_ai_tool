# Controller命名规范

## 命名模式

### API控制器（数据同步类）
- 命名规则: `Api{业务名}Controller`
- URL前缀: `/flexplannerApi/{业务名}`
- 接口URL: `/saveAll{业务名}Info` (旧格式), `/saveAll{业务名}InfoNew` (新格式)
- 文件位置: `flexplanner-web/src/main/java/com/ymsl/flexplanner/web/app/api/`
- 示例:
  - `ApiItemInfoController` → `/flexplannerApi/itemInfo` → `/saveAllItemInfo`
  - `ApiBomInfoController` → `/flexplannerApi/bomInfo` → `/saveAllBomInfo`
  - `ApiCalendarInfoController` → `/flexplannerApi/calendarInfo` → `/saveAllCalendarInfo`
  - `ApiProcessController` → `/flexplannerApi/process` → `/saveAllProcessInfo`
  - `ApiRoutingController` → `/flexplannerApi/routing` → `/saveAllRoutingInfo`
  - `ApiDemandInfoController` → `/flexplannerApi/demandInfo` → `/saveAllDemandInfo`

### 查询控制器（CRP/L类）
- 命名规则: `L{业务名}Controller` 或 `{业务名}Controller`
- URL前缀: `/L{业务名}` 或 `/{业务名小写}`
- 文件位置: `flexplanner-web/src/main/java/com/ymsl/flexplanner/web/app/api/`
- 示例:
  - `LCrpWorkCenterController` → `/Lcrp`
  - `LCrpOrderController` → `/LcrpOrder`

### 页面控制器（业务操作类）
- 命名规则: `{业务名}Controller`
- URL前缀: `/{业务名拼音或英文小写}`
- 文件位置: `flexplanner-web/src/main/java/com/ymsl/flexplanner/web/app/controller/`
- 示例:
  - `OrderController` → `/order`
  - `StockOutController` → `/stockout`
  - `ProductPlanController` → `/productPlan`
  - `DemandmanageController` → `/dm`
  - `MstCategoryInfoController` → `/categoryInfoMa`
  - `MstBufferColorController` → `/bufferColor`
  - `BomDistinctionController` → `/flexplannerApi/bomDistinctionController`

## 特殊命名

| 特殊前缀 | 含义 | 示例 |
|---------|------|------|
| `L` | 查询类（Look/L） | `LCrpWorkCenterController` |
| `Api` | API接口类 | `ApiItemInfoController` |
| `Mst` | 主数据管理类 | `MstCategoryInfoController` |
| `Crp` | CRP相关类 | `CrpWorkCenterController` |

## URL转换规则

| 业务名 | Controller类名 | URL前缀 |
|--------|--------------|---------|
| WorkCenter | `ApiWorkCenterController` | `/workCenter` (小写) |
| WorkOrderInfo | `ApiWorkOrderInfoController` | `/workOrderInfo` (小写) |
| SalesOrderInfo | `ApiSalesOrderInfoController` | `/salesOrderInfo` (小写) |
| SupplierInfo | `ApiSupplierInfoController` | `/supplierInfo` (小写) |
| CategoryInfoMa | `MstCategoryInfoController` | `/categoryInfoMa` (手动指定) |
| Dm | `DemandmanageController` | `/dm` (手动指定) |
