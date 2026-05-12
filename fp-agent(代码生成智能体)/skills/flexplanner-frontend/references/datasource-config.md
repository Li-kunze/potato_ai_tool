# DataSource 数据源配置指南

DataSource 是 FlexPlanner 前后端数据交互的核心组件,封装了 HTTP 请求、参数处理、响应解析等功能。

## DataSource 基础配置

### 标准配置模板

```javascript
vueDataSet_xxx: this.getDataSource({
  url: "/api/endpoint.json",      // 后端接口 URL
  type: "POST",                    // 请求方式: GET / POST
  parameter: {                     // 请求参数
    param1: value1,
    param2: value2
  },
  emulateJSON: true,               // 模拟 JSON 格式(可选)
  success: this.vueDataSetXxxSuccess,  // 成功回调
  error: this.vueDataSetXxxError       // 失败回调(可选)
})
```

### 完整配置示例

```javascript
data: function() {
  return {
    // 查询数据源
    vueDataSet_search: this.getDataSource({
      url: "/flexplannerApi/itemInfo/search.json",
      type: "POST",
      parameter: this.vueDataSetSearchParameter,
      emulateJSON: true,
      success: this.vueDataSetSearchSuccess,
      error: this.vueDataSetSearchError
    }),

    // 保存数据源
    vueDataSet_save: this.getDataSource({
      url: "/flexplannerApi/itemInfo/save.json",
      type: "POST",
      success: this.vueDataSetSaveSuccess
    }),

    // 删除数据源
    vueDataSet_delete: this.getDataSource({
      url: "/flexplannerApi/itemInfo/delete.json",
      type: "POST",
      parameter: {
        id: ''
      },
      success: this.vueDataSetDeleteSuccess
    })
  };
}
```

## DataSource 配置项详解

### url (必需)
后端接口 URL 地址,以 `.json` 结尾。

**示例:**
```javascript
url: "/flexplannerApi/itemInfo/search.json"
```

### type (必需)
HTTP 请求方式,值为 `"GET"` 或 `"POST"`。

FlexPlanner 项目主要使用 `POST` 方式。

**示例:**
```javascript
type: "POST"
```

### parameter (可选)
请求参数,可以是:
- **对象**: 静态参数对象
- **函数**: 动态返回参数对象

**静态参数示例:**
```javascript
parameter: {
  codeTy: 'ITEM_TYPE',
  defalut: '0'
}
```

**动态参数示例:**
```javascript
parameter: function() {
  return {
    siteId: store.state.userSiteId,        // 从全局状态获取
    factoryId: store.state.userFactoryId,
    itemKey: this.form.itemKey,           // 从表单绑定获取
    currentDate: VueUtil.formatDate(new Date(), 'yyyy-MM-dd')  // 动态计算
  };
}
```

### headers (可选)
HTTP 请求头配置对象。

**示例:**
```javascript
headers: {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + store.state.userToken
}
```

### emulateJSON (可选)
是否模拟 JSON 格式,通常设置为 `true`。

**示例:**
```javascript
emulateJSON: true
```

### success (必需)
请求成功时的回调函数,接收两个参数:
- `res`: 后端返回的响应对象

**示例:**
```javascript
methods: {
  vueDataSetSearchSuccess: function(res) {
    if (res && res.status === 200) {
      // 设置数据源的数据
      this.vueDataSet_search.data = res.data || [];
      // 记录总条数
      this.total = res.total || 0;
    } else {
      componentutils.showErrorMessage({
        message: "查询失败: " + (res.message || "未知错误")
      });
    }
  }
}
```

### error (可选)
请求失败时的回调函数。

**示例:**
```javascript
methods: {
  vueDataSetSearchError: function(err, ds) {
    componentutils.showErrorMessage({
      message: "网络错误，请稍后重试"
    });
    console.error('DataSource error:', err);
  }
}
```

### before (可选)
请求发送前的回调钩子,返回 `false` 可以中断请求。

**示例:**
```javascript
before: function(ds, tempBefore) {
  // 执行验证
  if (!this.form.itemKey) {
    componentutils.showWarningMessage({
      message: "请输入物料编号"
    });
    return false;  // 中断请求
  }
  // 执行临时回调
  if (VueUtil.isFunction(tempBefore)) {
    return tempBefore();
  }
  return true;
}
```

### localData (可选)
本地静态数据,用于不需要后端请求的场景。

**示例:**
```javascript
vueDataSet_status: this.getDataSource({
  localData: [
    { key: '0', label: '待处理' },
    { key: '1', label: '进行中' },
    { key: '2', label: '已完成' }
  ]
})
```

## DataSource 常用方法

### retrieve(回调函数)
触发 DataSource 请求。

**示例:**
```javascript
// 触发查询
this.vueDataSet_search.retrieve();

// 带回调函数
this.vueDataSet_search.retrieve(function(resp) {
  console.log('请求完成', resp);
});
```

### setParameter(参数对象)
动态设置 DataSource 的请求参数。

**示例:**
```javascript
// 设置参数后触发请求
this.vueDataSet_search.setParameter({
  itemKey: 'ITEM001',
  itemType: 'RAW'
}).retrieve();
```

### setData(数据数组)
直接设置 DataSource 的数据(不触发请求)。

**示例:**
```javascript
this.vueDataSet_search.setData([
  {id: 1, name: '物料1'},
  {id: 2, name: '物料2'}
]);
```

## DataSource 绑定到组件

### 下拉选择组件绑定

```html
<escort-select
  v-model="form.itemType"
  :datasource="vueDataSet_itemType"
  value-member="key"
  display-member="label">
</escort-select>
```

**数据源配置:**
```javascript
vueDataSet_itemType: this.getDataSource({
  url: "/common/getCodeList.json?codeId=ITEM_TYPE",
  type: "POST",
  success: this.vueDataSetItemTypeSuccess
})
```

**成功回调:**
```javascript
vueDataSetItemTypeSuccess: function(res, ds) {
  if (res && res.data) {
    this.vueDataSet_itemType.data = res.data;
  }
}
```

### XGrid 绑定

XGrid 通常绑定到计算属性:

```html
<escort-xgrid :data="gridData">
  <!-- 列定义 -->
</escort-xgrid>
```

**计算属性:**
```javascript
computed: {
  gridData: function() {
    var self = this;
    var data = self.vueDataSet_search.data || [];

    // 数据转换
    return data.map(function(item) {
      return {
        id: item.id,
        itemKey: item.itemKey,
        itemName: item.itemName,
        planDate: VueUtil.formatDate(item.planDate, 'yyyy-MM-dd'),
        planQty: item.planQty
      };
    });
  }
}
```

## 常见 DataSource 模式

### 1. 查询模式

```javascript
// 数据源定义
vueDataSet_search: this.getDataSource({
  url: "/flexplannerApi/itemInfo/search.json",
  type: "POST",
  parameter: this.vueDataSetSearchParameter,
  success: this.vueDataSetSearchSuccess
})

// 查询按钮点击
searchBtnClick: function() {
  var self = this;
  self.vueDataSet_search.retrieve();
}

// 查询参数
vueDataSetSearchParameter: function() {
  var self = this;
  var paginationObj = {
    currentPageSize: self.$refs.grid.getPageParams().pageSize,
    currentPage: self.$refs.grid.getPageParams().currentPage
  };
  var parms = VueUtil.merge(VueUtil.cloneDeep(self.conditionForm), paginationObj);
  return parms;
}

// 成功回调
vueDataSetSearchSuccess: function(res) {
  if (res && res.code === 200) {
    this.vueDataSet_search.data = res.data || [];
  }
}
```

### 2. 保存模式

```javascript
// 数据源定义
vueDataSet_save: this.getDataSource({
  url: "/flexplannerApi/itemInfo/save.json",
  type: "POST",
  success: this.vueDataSetSaveSuccess
})

// 保存按钮点击
saveBtnClick: function() {
  var self = this;

  // 获取表格待保存的数据
  var pendingData = self.$refs.vueXgrid_main.getPendingRows();

  self.vueDataSet_save.setParameter({
    siteId: store.state.userSiteId,
    items: pendingData
  });
  self.vueDataSet_save.retrieve(function(resp) {
    if (resp.code === 200) {
      componentutils.showSuccessMessage({
        message: resp.message || "保存成功"
      });
      // 刷新列表
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

### 3. 删除模式

```javascript
// 数据源定义
vueDataSet_delete: this.getDataSource({
  url: "/flexplannerApi/itemInfo/delete.json",
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
  }).then(function(action) {
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

// 成功回调
vueDataSetDeleteSuccess: function(res, ds) {
  // 删除成功后的处理
}
```

### 4. 下拉选项模式

```javascript
// 数据源定义
vueDataSet_codeList: this.getDataSource({
  url: "/common/getCodeList.json?codeId=ITEM_TYPE",
  type: "POST",
  success: this.vueDataSetCodeListSuccess
})

// mounted 中调用
mounted: function() {
  this.vueDataSet_codeList.retrieve();
}

// 成功回调
vueDataSetCodeListSuccess: function(res, ds) {
  if (res && res.data) {
    this.vueDataSet_codeList.data = res.data;
  }
}
```

### 5. 导出模式

```javascript
// 数据源定义
vueDataSet_export: this.getDataSource({
  url: "/flexplannerApi/itemInfo/export.json",
  type: "POST",
  parameter: function() {
    return {
      itemKey: this.form.itemKey,
      itemType: this.form.itemType
    };
  }
})

// 导出按钮点击
exportBtnClick: function() {
  var self = this;

  // 获取选中的行
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
    ids: ids
  });

  // 获取响应并下载文件
  self.vueDataSet_export.retrieve(function(res) {
    if (res && res.file) {
      // 下载文件
      window.location.href = res.file;
      componentutils.showSuccessMessage({
        message: "导出成功"
      });
    }
  });
}
```

## 常见响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": [
    { "id": 1, "itemKey": "ITEM001", "itemName": "物料1" },
    { "id": 2, "itemKey": "ITEM002", "itemName": "物料2" }
  ],
  "total": 100
}
```

### 错误响应
```json
{
  "code": 500,
  "message": "操作失败: 物料编号已存在"
}
```

### 分页响应
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    { "id": 1, "itemKey": "ITEM001" }
  ],
  "totalElements": 100,
  "totalPages": 10,
  "number": 0,
  "size": 10
}
```

## 注意事项

1. **DataSource 必须定义在 data() 中**
2. **成功回调方法必须定义在 auto.methods 中**
3. **使用 retrieve() 方法触发请求**
4. **参数设置后需要再次调用 retrieve()**
5. **本地数据使用 localData,不需要 success 回调**
6. **推荐使用动态 parameter 函数获取最新数据**
