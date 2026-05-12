# 数据同步完整模板

## 旧格式同步（ReRunModel模式）

```java
/**
 * 保存所有xxx信息（旧格式）
 */
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
```

## 新格式同步（接收JSON列表）

```java
/**
 * 保存所有xxx信息（新格式）
 */
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
```

## 混合格式示例（ApiBomInfoController）

```java
@PostMapping(value = "/saveAllBomInfo")
@ResponseBody
public ReRunModel saveAllBomInfo(@RequestBody ReRunModel reRunModel) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    boolean checkFlag = reRunModel == null ? false : reRunModel.isCheckFlag();
    String infType = PjConstants.infType.BOM_INFO;
    ReRunModel model = apiSaveLogic.saveAllBomInfo(siteId, factoryId, checkFlag, infType);
    String getBomSeq = commonService.getPara01(siteId, factoryId, "GET_BOM_SEQ", "0");
    if ("1".equals(getBomSeq)) {
        spBatchService.getBomSeq(siteId);
    }
    return model;
}

@PostMapping(value = "/saveAllBomInfoNew")
@ResponseBody
public String saveAllBomInfoNew(@RequestBody List<String> jsonStrList) {
    try {
        int count = insertDataLogic.insertData(jsonStrList, PjConstants.infType.BOM_INFO);
        return count + "条数据同步成功！";
    } catch (Exception e) {
        e.printStackTrace();
        return "数据同步失败！";
    }
}
```

## ApiCalendarInfoController（包含单条保存）

```java
/**
 * 保存单条日历信息
 */
@PostMapping(value = "/saveCalendarInfo")
@ResponseBody
public void saveCalendarInfo(@RequestBody ApiCalendarInfoModel apiCalendarInfoModel) {
    apiCalendarInfo.saveCalendarInfo(apiCalendarInfoModel);
}

/**
 * 保存所有日历信息（旧格式）
 */
@PostMapping(value = "/saveAllCalendarInfo")
@ResponseBody
public ReRunModel saveAllCalendarInfo(@RequestBody ReRunModel reRunModel) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    boolean checkFlag = reRunModel == null ? false : reRunModel.isCheckFlag();
    return apiSaveLogic.saveAllCalendarInfo(siteId, factoryId, checkFlag);
}

/**
 * 保存所有日历信息（新格式）
 */
@PostMapping(value = "/saveAllCalendarInfoNew")
@ResponseBody
public String saveAllCalendarInfoNew(@RequestBody List<String> jsonStrList) {
    try {
        int count = insertDataLogic.insertData(jsonStrList, PjConstants.infType.CALENDAR_INFO);
        return count + "条数据同步成功！";
    } catch (Exception e) {
        e.printStackTrace();
        return "数据同步失败！";
    }
}
```

## ApiItemInfoController（包含停用接口）

```java
/**
 * 停用物料接口
 */
@PostMapping(value = "/saveAllDisabledItemInfoNew")
@ResponseBody
public RestBaseModel saveAllDisabledItemInfo(@RequestBody List<String> jsonStrList) {
    try {
        int count = insertDataLogic.insertData(jsonStrList, PjConstants.infType.DISABLED_ITEM);
        return new RestBaseModel<>(200, count + "条【停用物料】数据同步成功！");
    } catch (Exception e) {
        e.printStackTrace();
        return new RestBaseModel<>(500, "【停用物料】数据同步失败！");
    }
}
```

## 常用依赖注入

```java
@Autowired
private InsertDataLogic insertDataLogic;

@Autowired
private ApiSaveLogic apiSaveLogic;

@Autowired
private SpBatchService spBatchService;

@Autowired
private CommonService commonService;
```
