# API控制器完整模板

## 类结构

```java
package com.ymsl.flexplanner.web.app.api;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.a1.solid.base.exception.BusinessCodedException;
import com.ymsl.flexplanner.constants.PjConstants;
import com.ymsl.flexplanner.model.RestBaseModel;
import com.ymsl.flexplanner.model.api.ReRunModel;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.service.api.logic.ApiSaveLogic;
import com.ymsl.flexplanner.service.api.logic.datainto.InsertDataLogic;

@Controller
@RequestMapping("/flexplannerApi/xxx")
public class ApiXxxController {

    @Autowired
    private InsertDataLogic insertDataLogic;

    @Autowired
    private ApiSaveLogic apiSaveLogic;

    @PostMapping(value = "/saveAllXxxInfo")
    @ResponseBody
    public ReRunModel saveAllXxxInfo(@RequestBody ReRunModel reRunModel) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        boolean checkFlag = reRunModel == null ? false : reRunModel.isCheckFlag();
        try {
            return apiSaveLogic.saveAllXxxInfo(siteId, factoryId, checkFlag);
        } catch (BusinessCodedException e) {
            e.printStackTrace();
            return new ReRunModel();
        }
    }

    @PostMapping(value = "/saveAllXxxInfoNew")
    @ResponseBody
    public RestBaseModel saveAllXxxInfoNew(@RequestBody List<String> jsonStrList) {
        try {
            int count = insertDataLogic.insertData(jsonStrList, PjConstants.infType.XXX_INFO);
            return new RestBaseModel<>(200, count + "条数据同步成功！");
        } catch (Exception e) {
            e.printStackTrace();
            return new RestBaseModel<>(500, "数据同步失败！");
        }
    }
}
```

## URL规范

| 业务模块 | Controller类名 | @RequestMapping | 接口方法URL |
|---------|---------------|-----------------|-------------|
| 物料信息 | `ApiItemInfoController` | `/flexplannerApi/itemInfo` | `/saveAllItemInfo` |
| BOM信息 | `ApiBomInfoController` | `/flexplannerApi/bomInfo` | `/saveAllBomInfo` |
| 日历信息 | `ApiCalendarInfoController` | `/flexplannerApi/calendarInfo` | `/saveAllCalendarInfo` |
| 工艺信息 | `ApiProcessController` | `/flexplannerApi/process` | `/saveAllProcessInfo` |
| 路由信息 | `ApiRoutingController` | `/flexplannerApi/routing` | `/saveAllRoutingInfo` |
| 需求信息 | `ApiDemandInfoController` | `/flexplannerApi/demandInfo` | `/saveAllDemandInfo` |
| 工作中心 | `ApiWorkCenterController` | `/flexplannerApi/workCenter` | `/saveAllWorkCenterInfo` |
| 工单信息 | `ApiWorkOrderInfoController` | `/flexplannerApi/workOrderInfo` | `/saveAllWorkOrderInfo` |

## 常量类型

在`PjConstants.infType`中定义:

```java
PjConstants.infType.ITEM_INFO           // 物料信息
PjConstants.infType.BOM_INFO            // BOM信息
PjConstants.infType.CALENDAR_INFO       // 日历信息
PjConstants.infType.PROCESS_INFO        // 工艺信息
PjConstants.infType.ROUTING_INFO        // 路由信息
PjConstants.infType.DEMAND_INFO         // 需求信息
PjConstants.infType.WORK_CENTER_INFO    // 工作中心信息
PjConstants.infType.WORK_ORDER_INFO     // 工单信息
PjConstants.infType.INVENTORY_INFO      // 库存信息
PjConstants.infType.SUPPLIER_INFO       // 供应商信息
PjConstants.infType.SALES_ORDER_INFO    // 销售订单信息
PjConstants.infType.BATCH_SET_MLT_INFO  // 批量设置信息
```
