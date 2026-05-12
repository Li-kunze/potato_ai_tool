# 页面控制器完整模板

## 类结构（OrderController - 业务操作控制器）

```java
package com.ymsl.flexplanner.web.app.controller;

import java.util.List;
import java.util.Map;

import javax.inject.Inject;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.ymsl.flexplanner.model.OrdersModel;
import com.ymsl.flexplanner.model.RestBaseModel;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.service.OrderService;

@Controller
@RequestMapping("/order")
public class OrderController {

    @Inject
    OrderService orderService;

    @SuppressWarnings("rawtypes")
    @PostMapping(value = "/api/getOrders")
    @ResponseBody
    public RestBaseModel<List<OrdersModel>> getOrders(@RequestBody Map<String, Object> model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        String item = (String) model.get("item");
        String planFinishDate = (String) model.get("planFinishDate");
        String orderNo = (String) model.get("orderNo");
        return orderService.getOrders(siteId, factoryId, item, planFinishDate, orderNo);
    }

    @SuppressWarnings("rawtypes")
    @PostMapping(value = "/api/calculationOrderResult")
    @ResponseBody
    public RestBaseModel<Map<String, Object>> calculationOrderResult(@RequestBody Map<String, Object> model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        List<String> itemKeys = (List<String>) model.get("itemKeys");
        return orderService.calculationOrderResult(siteId, factoryId, itemKeys);
    }
}
```

## 类结构（MstCategoryInfoController - CRUD控制器）

```java
package com.ymsl.flexplanner.web.app.controller;

import java.util.List;

import javax.inject.Inject;

import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import com.ymsl.flexplanner.model.CategoryInfoModel;
import com.ymsl.flexplanner.model.MrpItemRelationModel;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.service.MstCategoryInfoService;

/**
 * 类别管理控制器
 */
@Controller
@RequestMapping("/categoryInfoMa")
public class MstCategoryInfoController {
    
    @Inject
    MstCategoryInfoService mstCategoryInfoService;

    /**
     * 分页查询
     */
    @RequestMapping(value = "/getDataByPage.json", method = RequestMethod.POST)
    @ResponseBody
    public Page<CategoryInfoModel> getDataByPage(@RequestBody CategoryInfoModel categoryInfoModel) {
        categoryInfoModel.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
        categoryInfoModel.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
        return mstCategoryInfoService.getDataByPage(categoryInfoModel);
    }

    /**
     * 新增或修改
     */
    @RequestMapping(value = "/updateOrNewData.json", method = RequestMethod.POST)
    @ResponseBody
    public void updateOrNewData(@RequestBody CategoryInfoModel categoryInfoModel) {
        categoryInfoModel.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
        categoryInfoModel.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
        mstCategoryInfoService.updateOrNewData(categoryInfoModel);
    }

    /**
     * 检查数据是否存在
     */
    @RequestMapping(value = "/checkDataIsExist.json", method = RequestMethod.POST)
    @ResponseBody
    public Boolean checkDataIsExist(@RequestBody CategoryInfoModel categoryInfoModel) {
        categoryInfoModel.setSiteId(PJUserAccessor.getUserDetail().getSiteId());
        categoryInfoModel.setFactoryId(PJUserAccessor.getUserDetail().getFactoryId());
        return mstCategoryInfoService.checkDataExist(categoryInfoModel);
    }
}
```

## 类结构（DemandmanageController - 扩展控制器）

```java
package com.ymsl.flexplanner.web.app.controller;

import java.util.List;

import javax.inject.Inject;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.ymsl.flexplanner.engine.DdmrpSearchEngine;
import com.ymsl.flexplanner.entity.DdmrpParaDefInfo;
import com.ymsl.flexplanner.model.JsonBinaryMap;
import com.ymsl.flexplanner.repository.DdmrpSysUserdefInfoRepository;
import com.ymsl.flexplanner.repository.IDdmrpParaDefInfoJpaRepository;
import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.service.batchService.CommonService;

/**
 * 需求管理模块控制器
 */
@Controller
@RequestMapping("/dm")
public class DemandmanageController {

    @Inject
    private DdmrpSysUserdefInfoRepository ddmrpSysUserdefInfoRepository;
    @Inject
    IDdmrpParaDefInfoJpaRepository ddmrpParaDefInfoJpaRepository;

    /**
     * 获取需求类型说明图片
     */
    @RequestMapping(value = "/getDemandTypeImgUrl.json", method = RequestMethod.POST)
    @ResponseBody
    public JsonBinaryMap getDemandTypeImgUrl(@RequestParam String codeTy) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        JsonBinaryMap imgUrl = null;
        List<DdmrpSysUserdefInfo> list = ddmrpSysUserdefInfoRepository
                .findAllBySiteIdAndFactoryIdAndCodeTy(siteId, factoryId, codeTy);
        if (!list.isEmpty()) {
            imgUrl = list.get(0).getExtendList();
        }
        return imgUrl;
    }

    /**
     * 需求类型下拉框
     */
    @PostMapping(value = "/getDemandTypeList.json")
    @ResponseBody
    public List<DdmrpParaDefInfo> getDropDownData(@RequestParam String codeTy) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        return ddmrpParaDefInfoJpaRepository.findBySiteIdAndFactoryIdAndCodeTyOrderBySeq(siteId, factoryId, codeTy);
    }
}
```

## URL规范

| Controller类名 | @RequestMapping | 接口方法URL |
|---------------|-----------------|------------|
| `OrderController` | `/order` | `/api/getOrders` |
| `MstCategoryInfoController` | `/categoryInfoMa` | `/getDataByPage.json` |
| `DemandmanageController` | `/dm` | `/getDemandTypeList.json` |
| `ProductPlanController` | `/productPlan` | `/api/getProductPlanInfo` |

## 常见方法命名

| 功能 | 方法命名规律 | 示例 |
|------|------------|------|
| 查询列表 | `getXXX` | `getOrders`, `getInfo` |
| 保存数据 | `saveXXX` | `save`, `saveCustomColumnSetInfo` |
| 删除数据 | `delXXX` | `delCustomColumnSetInfo` |
| 检查存在 | `checkXXX` | `checkDataIsExist` |
| 更新/新增 | `updateOrNewXXX` | `updateOrNewData` |
| 计算结果 | `calculationXXX` | `calculationOrderResult` |
