# 后端 API 集成指南

本文档说明 FlexPlanner 前端与后端 API 的集成方式。

## 后端 Controller 模式

FlexPlanner 后端使用 Spring Boot 框架,Controller 统一使用以下模式:

### 基础 Controller 模板

```java
package com.ymsl.flexplanner.web.app.api;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.ymsl.flexplanner.security.auth.PJUserAccessor;
import com.ymsl.flexplanner.model.RestBaseModel;
import com.ymsl.flexplanner.service.XxxService;

@Controller
@RequestMapping("/flexplannerApi/xxx")
public class XxxController {

    @Autowired
    private XxxService xxxService;

    /**
     * 查询接口
     */
    @PostMapping(value = "/search")
    @ResponseBody
    public RestBaseModel search(@RequestBody SearchModel model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        model.setSiteId(siteId);
        model.setFactoryId(factoryId);
        return xxxService.search(model);
    }

    /**
     * 保存接口
     */
    @PostMapping(value = "/save")
    @ResponseBody
    public RestBaseModel save(@RequestBody SaveModel model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        model.setSiteId(siteId);
        model.setFactoryId(factoryId);
        return xxxService.save(model);
    }

    /**
     * 删除接口
     */
    @PostMapping(value = "/delete")
    @ResponseBody
    public RestBaseModel delete(@RequestBody DeleteModel model) {
        String siteId = PJUserAccessor.getUserDetail().getSiteId();
        String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
        return xxxService.delete(model);
    }
}
```

## 常用注解说明

### @Controller
标识为控制器类,返回 JSON 数据。

### @RequestMapping
定义控制器的基础路径。

```java
@RequestMapping("/flexplannerApi/itemInfo")
```

### @PostMapping
定义 POST 请求映射。

```java
@PostMapping(value = "/save")
```

### @RequestBody
接收请求体中的 JSON 数据。

```java
public RestBaseModel save(@RequestBody ItemInfoModel model)
```

### @ResponseBody
将返回对象转换为 JSON 格式。

```java
@ResponseBody
public RestBaseModel save(...)
```

## 常见响应格式

### RestBaseModel 标准响应

```java
// 控制器
return new RestBaseModel<>(200, "操作成功");

// 或带数据
return new RestBaseModel<>(200, "操作成功", dataList);
```

**响应结构:**
```json
{
  "code": 200,
  "message": "操作成功",
  "data": [...]
}
```

### 自定义 Model 响应

```java
// Model 类
public class SearchModel extends BaseModel {
    private List<ItemInfo> data;
    private Long total;
    // ...
}

// 控制器
return new SearchModel(200, "查询成功", dataList, dataList.size());
```

## 前端 DataSource 对应配置

### 基础配置

```javascript
// DataSource 定义
vueDataSet_save: this.getDataSource({
  url: "/flexplannerApi/itemInfo/save",
  type: "POST",
  parameter: {
    itemKey: '',
    itemName: '',
    itemType: ''
  },
  success: this.vueDataSetSaveSuccess
})
```

### 对应后端 Controller

```java
@PostMapping(value = "/save")
@ResponseBody
public RestBaseModel save(@RequestBody ItemInfoModel model) {
    // model 自动接收前端 JSON 数据
    String itemKey = model.getItemKey();
    String itemName = model.getItemName();
    String itemType = model.getItemType();

    // 处理业务逻辑
    return new RestBaseModel<>(200, "保存成功");
}
```

## 查询接口集成

### 后端实现

```java
/**
 * 查询接口
 */
@PostMapping(value = "/search")
@ResponseBody
public RestBaseModel search(@RequestBody ItemInfoSearchModel model) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    model.setSiteId(siteId);
    model.setFactoryId(factoryId);
    return itemInfoService.search(model);
}
```

### 前端配置

```javascript
// DataSource 定义
vueDataSet_search: this.getDataSource({
  url: "/flexplannerApi/itemInfo/search",
  type: "POST",
  parameter: function() {
    return {
      siteId: store.state.userSiteId,
      factoryId: store.state.userFactoryId,
      itemKey: this.form.itemKey,
      itemType: this.form.itemType
    };
  },
  success: this.vueDataSetSearchSuccess
})

// 成功回调
vueDataSetSearchSuccess: function(res, ds) {
  if (res && res.code === 200) {
    this.vueDataSet_search.data = res.data || [];
  }
}

// 查询按钮点击
searchBtnClick: function() {
  this.vueDataSet_search.retrieve();
}
```

## 保存接口集成

### 后端实现

```java
/**
 * 保存接口(单条或多条)
 */
@PostMapping(value = "/save")
@ResponseBody
public RestBaseModel save(@RequestBody List<ItemInfoModel> items) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();

    for (ItemInfoModel item : items) {
        item.setSiteId(siteId);
        item.setFactoryId(factoryId);
    }

    return itemInfoService.save(items);
}
```

### 前端配置

```javascript
// DataSource 定义
vueDataSet_save: this.getDataSource({
  url: "/flexplannerApi/itemInfo/save",
  type: "POST",
  success: this.vueDataSetSaveSuccess
})

// 保存按钮点击
saveBtnClick: function() {
  var self = this;

  // 获取表格待保存的数据
  var pendingData = self.$refs.vueXgrid_main.getPendingRows();

  if (pendingData.length === 0) {
    componentutils.showWarningMessage({
      message: "没有需要保存的数据"
    });
    return;
  }

  self.vueDataSet_save.setParameter({
    siteId: store.state.userSiteId,
    factoryId: store.state.userFactoryId,
    items: pendingData
  });

  self.vueDataSet_save.retrieve(function(resp) {
    if (resp.code === 200) {
      componentutils.showSuccessMessage({
        message: resp.message || "保存成功"
      });
      self.searchBtnClick();
    }
  });
}

// 成功回调
vueDataSetSaveSuccess: function(res, ds) {
  if (res && res.code === 200) {
    componentutils.showSuccessMessage({
      message: "操作成功"
    });
  }
}
```

## 删除接口集成

### 后端实现

```java
/**
 * 删除接口
 */
@PostMapping(value = "/delete")
@ResponseBody
public RestBaseModel delete(@RequestBody DeleteModel model) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    return itemInfoService.delete(siteId, factoryId, model.getId());
}
```

### 前端配置

```javascript
// DataSource 定义
vueDataSet_delete: this.getDataSource({
  url: "/flexplannerApi/itemInfo/delete",
  type: "POST",
  success: this.vueDataSetDeleteSuccess
})

// 删除按钮点击
deleteClick: function(row) {
  var self = this;
  self.$confirm({
    title: "提示",
    message: "确定要删除这条数据吗?",
    type: "warning"
  }).then(function() {
    self.vueDataSet_delete.setParameter({
      id: row.id
    });
    self.vueDataSet_delete.retrieve(function(resp) {
      if (resp.code === 200) {
        componentutils.showSuccessMessage({
          message: "删除成功"
        });
        self.searchBtnClick();
      }
    });
  });
}
```

## 导出接口集成

### 后端实现

```java
/**
 * 导出接口
 */
@PostMapping(value = "/export")
@ResponseBody
public RestBaseModel export(@RequestBody ExportModel model) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    model.setSiteId(siteId);
    model.setFactoryId(factoryId);

    String filePath = itemInfoService.export(model);
    return new RestBaseModel<>(200, "导出成功", filePath);
}
```

### 前端配置

```javascript
// DataSource 定义
vueDataSet_export: this.getDataSource({
  url: "/flexplannerApi/itemInfo/export",
  type: "POST",
  success: this.vueDataSetExportSuccess
})

// 导出按钮点击
exportBtnClick: function() {
  var self = this;

  var selectedRows = self.$refs.vueXgrid_main.getSelectRecords();

  if (selectedRows.length === 0) {
    componentutils.showWarningMessage({
      message: "请先选择要导出的数据"
    });
    return;
  }

  var ids = selectedRows.map(function(item) {
    return item.id;
  });

  self.vueDataSet_export.setParameter({
    siteId: store.state.userSiteId,
    factoryId: store.state.userFactoryId,
    ids: ids
  });

  self.vueDataSet_export.retrieve(function(resp) {
    if (resp && resp.data) {
      // 下载文件
      window.location.href = resp.data;
      componentutils.showSuccessMessage({
        message: "导出成功"
      });
    }
  });
}
```

## 共通代码表接口

### 后端实现

```java
/**
 * 获取共通代码表
 */
@PostMapping(value = "/getCodeList")
@ResponseBody
public RestBaseModel getCodeList(@RequestParam String codeId) {
    return commonService.getCodeList(codeId);
}
```

### 前端配置

```javascript
// DataSource 定义
vueDataSet_itemType: this.getDataSource({
  url: "/common/getCodeList.json?codeId=ITEM_TYPE",
  type: "POST",
  success: this.vueDataSetItemTypeSuccess
})

// mounted 中调用
mounted: function() {
  this.vueDataSet_itemType.retrieve();
}

// 成功回调
vueDataSetItemTypeSuccess: function(res, ds) {
  if (res && res.data) {
    this.vueDataSet_itemType.data = res.data;
  }
}
```

## 用户信息获取

### 获取当前用户信息

```javascript
// 获取站点ID
var siteId = store.state.userSiteId;

// 获取工厂ID
var factoryId = store.state.userFactoryId;

// 获取用户ID
var userId = PJUserAccessor.getUserDetail().getUserId();

// 获取用户名
var userName = PJUserAccessor.getUserDetail().getUserName();
```

### 在 Controller 中获取

```java
String siteId = PJUserAccessor.getUserDetail().getSiteId();
String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
String userId = PJUserAccessor.getUserDetail().getUserId();
```

## 错误处理

### 后端异常处理

```java
try {
    // 业务逻辑
    return new RestBaseModel<>(200, "操作成功");
} catch (BusinessCodedException e) {
    return new RestBaseModel<>(500, e.getMessage());
} catch (Exception e) {
    e.printStackTrace();
    return new RestBaseModel<>(500, "系统错误");
}
```

### 前端错误处理

```javascript
vueDataSetSearchSuccess: function(res, ds) {
  if (res && res.code === 200) {
    this.vueDataSet_search.data = res.data || [];
  } else {
    componentutils.showErrorMessage({
      message: "查询失败: " + (res.message || "未知错误")
    });
  }
}

vueDataSetSearchError: function(err, ds) {
  componentutils.showErrorMessage({
    message: "网络错误,请稍后重试"
  });
  console.error('DataSource error:', err);
}
```

## 分页接口集成

### 后端实现

```java
@PostMapping(value = "/searchPage")
@ResponseBody
public RestBaseModel searchPage(@RequestBody SearchModel model) {
    String siteId = PJUserAccessor.getUserDetail().getSiteId();
    String factoryId = PJUserAccessor.getUserDetail().getFactoryId();
    model.setSiteId(siteId);
    model.setFactoryId(factoryId);

    Page<ItemInfo> page = itemInfoService.searchPage(model);

    return new RestBaseModel<>(200, "查询成功", page.getContent(), page.getTotalElements());
}
```

### 前端配置

```javascript
// DataSource 定义
vueDataSet_search: this.getDataSource({
  url: "/flexplannerApi/itemInfo/searchPage",
  type: "POST",
  parameter: function() {
    return {
      siteId: store.state.userSiteId,
      factoryId: store.state.userFactoryId,
      itemKey: this.form.itemKey,
      page: 0,
      size: 10
    };
  },
  success: this.vueDataSetSearchSuccess
})

// 成功回调
vueDataSetSearchSuccess: function(res, ds) {
  if (res && res.code === 200) {
    this.vueDataSet_search.data = res.data || [];
    this.total = res.total || 0;
  }
}
```

## 注意事项

1. **所有 POST 接口都需要 @RequestBody 注解**
2. **Controller 统一返回 RestBaseModel**
3. **前端使用 DataSource 封装 HTTP 请求**
4. **成功响应code为200**
5. **用户信息(siteId, factoryId)统一在Controller中获取**
6. **异常处理返回错误信息,不要抛出异常到前端**
