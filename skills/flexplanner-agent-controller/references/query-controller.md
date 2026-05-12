# 查询控制器完整模板

## 类结构（LCrpWorkCenterController - 标准查询控制器）

```java
package com.ymsl.flexplanner.web.app.api;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.ymsl.flexplanner.model.LCrpWorkCenterInfoModel;
import com.ymsl.flexplanner.model.RestBaseModel;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.service.LCrpWorkCenterService;

/**
 * xxx信息查询控制器
 */
@Controller
@RequestMapping("/Lxxx")
public class LXxxController {

    @Autowired
    private XxxService xxxService;

    /**
     * 查询xxx信息
     *
     * @param model 查询条件
     * @return 查询结果
     */
    @PostMapping(value = "/getInfo.json")
    @ResponseBody
    public RestBaseModel<Page<XxxInfoModel>> getInfo(@RequestBody XxxInfoModel model) {
        try {
            model.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
            model.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
            Page<XxxInfoModel> page = xxxService.getInfo(model);
            return new RestBaseModel<>(200, "查询成功", page);
        } catch (Exception e) {
            e.printStackTrace();
            return new RestBaseModel<>(500, "查询失败: " + e.getMessage(), null);
        }
    }
}
```

## 类结构（StockOutController - 页面查询控制器）

```java
package com.ymsl.flexplanner.web.app.controller;

import javax.inject.Inject;

import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.ymsl.flexplanner.model.BaseInfoModel;
import com.ymsl.flexplanner.model.RestBaseModel;
import com.ymsl.flexplanner.model.StockOutModel;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.service.StockOutService;

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

## URL规范

| Controller类名 | @RequestMapping | 接口方法URL |
|---------------|-----------------|------------|
| `LCrpWorkCenterController` | `/Lcrp` | `/getWorkCenterInfo.json` |
| `StockOutController` | `/stockout` | `/api/getAllStockOut.json` |
| `OrderController` | `/order` | `/api/getOrders` |
| `MstCategoryInfoController` | `/categoryInfoMa` | `/getDataByPage.json` |

## 响应说明

- 成功: `new RestBaseModel<>(200, "查询成功", page)`
- 失败: `new RestBaseModel<>(500, "查询失败: " + e.getMessage(), null)`
