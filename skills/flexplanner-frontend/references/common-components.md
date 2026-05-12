# FlexPlanner 常用组件代码片段

本文档收录 FlexPlanner 项目常用的 Escort 组件代码片段,便于快速参考。

## 表单组件

### 输入框

```html
<escort-input
  v-model="form.itemKey"
  prop="itemKey"
  :label-value="messageutil.get('物料编号')"
  label-width="100px"
  placeholder="请输入物料编号"
  :style_="{ width: '200px' }">
</escort-input>
```

**只读输入框:**
```html
<escort-input
  v-model="form.itemKey"
  :disabled="true"
  :label-value="messageutil.get('物料编号')"
  label-width="100px">
</escort-input>
```

**密码输入框:**
```html
<escort-input
  v-model="form.password"
  type="password"
  prop="password"
  :label-value="messageutil.get('密码')"
  label-width="100px">
</escort-input>
```

### 下拉选择

```html
<!-- 静态选项 -->
<escort-select
  v-model="form.itemType"
  :options="itemTypeOpts"
  :label-value="messageutil.get('物料类型')"
  label-width="100px">
</escort-select>

<!-- 动态选项(DataSource) -->
<escort-select
  v-model="form.itemType"
  :datasource="vueDataSet_itemType"
  value-member="key1"
  display-member="codeData1"
  :label-value="messageutil.get('物料类型')"
  label-width="100px"
  :filterable="true"
  :clearable="true">
</escort-select>

<!-- 多选下拉 -->
<escort-select
  v-model="form.itemTypes"
  :datasource="vueDataSet_itemType"
  value-member="key1"
  display-member="codeData1"
  :label-value="messageutil.get('物料类型')"
  label-width="100px"
  :multiple="true">
</escort-select>
```

**选项定义:**
```javascript
// 静态选项
itemTypeOpts: function() {
  return [
    { value: 'RAW', label: '原材料' },
    { value: 'SEMI', label: '半成品' },
    { value: 'FINISHED', label: '成品' }
  ];
}
```

### 日期时间选择

```html
<!-- 日期选择 -->
<escort-datetime-picker
  v-model="form.planDate"
  prop="planDate"
  value-format="yyyy-MM-dd"
  type="date"
  :label-value="messageutil.get('计划日期')"
  label-width="100px"
  format="ymd">
</escort-datetime-picker>

<!-- 日期时间选择 -->
<escort-datetime-picker
  v-model="form.createTime"
  value-format="yyyy-MM-dd HH:mm:ss"
  type="datetime"
  :label-value="messageutil.get('创建时间')"
  label-width="100px"
  format="ymdt">
</escort-datetime-picker>

<!-- 日期范围选择 -->
<escort-datetime-picker
  v-model="form.dateRange"
  type="daterange"
  value-format="yyyy-MM-dd"
  :label-value="messageutil.get('日期范围')"
  label-width="100px"
  format="ymd">
</escort-datetime-picker>
```

### 复选框

```html
<!-- 方框样式复选框 -->
<escort-checkbox
  v-model="form.selectedItems"
  :options="checkboxOpts"
  checkbox-style="checkBox"
  :label-value="messageutil.get('选择项目')"
  label-width="100px">
</escort-checkbox>

<!-- 按钮样式复选框 -->
<escort-checkbox
  v-model="form.selectedTypes"
  :options="typeOpts"
  checkbox-style="button">
</escort-checkbox>

<!-- 单个复选框 -->
<vue-checkbox v-model="form.acceptFlag">接受条款</vue-checkbox>
```

### 单选按钮

```html
<!-- 圆圈样式单选 -->
<escort-radio-button
  v-model="form.queryType"
  :options="queryTypeOpts"
  radio-style="radio"
  :label-value="messageutil.get('查询类型')"
  label-width="100px">
</escort-radio-button>

<!-- 按钮样式单选 -->
<escort-radio-button
  v-model="form.displayMode"
  :options="displayModeOpts"
  radio-style="button">
</escort-radio-button>
```

### 文本域

```html
<escort-textarea
  v-model="form.remark"
  prop="remark"
  :rows="4"
  :label-value="messageutil.get('备注')"
  label-width="100px"
  placeholder="请输入备注信息"
  :style_="{ width: '400px' }">
</escort-textarea>
```

### 文本组件

```html
<escort-text
  text="快速选择:"
  :style_="{ fontSize: '15px', fontWeight: 'bold' }">
</escort-text>
```

## 按钮组件

### 基础按钮

```html
<!-- 主按钮 -->
<escort-button type="primary" size="small" @click="searchClick">
  {{messageutil.get('查询')}}
</escort-button>

<!-- 成功按钮 -->
<escort-button type="success" size="small" @click="saveClick">
  {{messageutil.get('保存')}}
</escort-button>

<!-- 警告按钮 -->
<escort-button type="warning" size="small" @click="resetClick">
  {{messageutil.get('重置')}}
</escort-button>

<!-- 危险按钮 -->
<escort-button type="danger" size="small" @click="deleteClick">
  {{messageutil.get('删除')}}
</escort-button>

<!-- 信息按钮 -->
<escort-button type="info" size="small" @click="exportClick">
  {{messageutil.get('导出')}}
</escort-button>

<!-- 文本按钮 -->
<escort-button type="text" @click="detailClick">
  {{messageutil.get('查看详情')}}
</escort-button>
```

### 带图标按钮

```html
<escort-button type="primary" size="small" icon="vue-icon-search" @click="searchClick">
  {{messageutil.get('查询')}}
</escort-button>

<escort-button type="success" size="small" icon="vue-icon-check" @click="saveClick">
  {{messageutil.get('保存')}}
</escort-button>
```

### 带快捷键按钮

```html
<escort-button type="primary" hotkey="ctrl+s" @click="saveClick">
  {{messageutil.get('保存')}}
</escort-button>

<escort-button type="success" hotkey="enter" @click="submitClick">
  {{messageutil.get('提交')}}
</escort-button>
```

### 加载中按钮

```html
<escort-button type="primary" :loading="saving" @click="saveClick">
  {{messageutil.get('保存')}}
</escort-button>
```

### 禁用/隐藏按钮

```html
<!-- 禁用按钮 -->
<escort-button type="primary" :disabled="true" @click="click">
  {{messageutil.get('点击')}}
</escort-button>

<!-- 条件禁用 -->
<escort-button type="primary" :disabled="!hasModify" @click="saveClick">
  {{messageutil.get('保存')}}
</escort-button>

<!-- 隐藏按钮 -->
<escort-button type="danger" :hidden="true" @click="deleteClick">
  {{messageutil.get('删除')}}
</escort-button>
```

## 布局组件

### 行布局

```html
<!-- 单行布局 -->
<escort-row id="vueRow_condition" ref="vueRow_condition">
  <escort-col :inline="true" :md="{span:8}">
    <!-- 内容 -->
  </escort-col>
  <escort-col :inline="true" :md="{span:8}">
    <!-- 内容 -->
  </escort-col>
  <escort-col :inline="true" :md="{span:8}">
    <!-- 内容 -->
  </escort-col>
</escort-row>

<!-- 右对齐按钮行 -->
<escort-row id="vueRow_buttons" ref="vueRow_buttons">
  <escort-col align="right" :inline="true" :md="{span:24}">
    <escort-button type="primary" @click="saveClick">保存</escort-button>
    <escort-button @click="cancelClick">取消</escort-button>
  </escort-col>
</escort-row>

<!-- 居中按钮行 -->
<escort-row id="vueRow_center" ref="vueRow_center">
  <escort-col align="center" :md="{span:24}">
    <escort-button type="primary" @click="confirmClick">确定</escort-button>
  </escort-col>
</escort-row>
```

## 表格组件

### 基础表格

```html
<escort-xgrid
  id="vueXgrid_main"
  ref="vueXgrid_main"
  :data="gridData"
  height="400"
  border
  stripe
  highlight-current-row">

  <escort-xgrid-column type="checkbox" width="50px" align="center"></escort-xgrid-column>
  <escort-xgrid-column type="index" width="50px" align="center"></escort-xgrid-column>
  <escort-xgrid-column prop="itemKey" text="物料编号" width="120px"></escort-xgrid-column>
  <escort-xgrid-column prop="itemName" text="物料名称" width="150px"></escort-xgrid-column>
</escort-xgrid>
```

### 可编辑表格

```html
<escort-xgrid :data="gridData">
  <escort-xgrid-column prop="itemKey" text="物料编号" render-name="input"></escort-xgrid-column>
  <escort-xgrid-column prop="planDate" text="计划日期" render-name="date" edit-render-value-format="yyyy-MM-dd" format="ymd"></escort-xgrid-column>
  <escort-xgrid-column prop="planQty" text="计划数量" align="right" render-name="numeric"></escort-xgrid-column>
</escort-xgrid>
```

### 带操作按钮的表格

```html
<escort-xgrid :data="gridData">
  <escort-xgrid-column fixed="right" align="center" text="操作" width="150px" render-name="button" :buttons="vueXgridButtons"></escort-xgrid-column>
</escort-xgrid>
```

```javascript
methods: {
  vueXgridButtons: function(scope) {
    return [{
      value: "编辑",
      size: 'small',
      type: 'text',
      click: this.editClick
    }, {
      value: "删除",
      size: 'small',
      type: 'text',
      click: this.deleteClick
    }];
  }
}
```

## 弹窗组件

### 居中弹窗

```html
<escort-window
  v-model="showEditWindow"
  size="small"
  top="15%"
  title="编辑信息"
  :close-on-click-modal="false"
  id="vueWindow_edit"
  ref="vueWindow_edit">
  <escort-row>
    <escort-col>
      <escort-textarea v-model="form.remark" :rows="4"></escort-textarea>
    </escort-col>
  </escort-row>
  <escort-row>
    <escort-col align="center">
      <escort-button type="primary" @click="confirmEditClick">确定</escort-button>
      <escort-button @click="showEditWindow = false">取消</escort-button>
    </escort-col>
  </escort-row>
</escort-window>
```

### 侧边栏弹窗

```html
<escort-aside
  ref="asideDetail"
  position="right"
  size="small"
  :close-on-press-escape="true"
  :close-on-click-modal="true"
  id="vueAside_detail"
  src="/views/MODULE/SUBPAGE.html">
</escort-aside>
```

**打开侧边栏:**
```javascript
this.$refs.asideDetail.open({
  id: 'xxx',
  parent: this
});
```

## 消息提示

### 成功消息

```javascript
componentutils.showSuccessMessage({
  message: "操作成功",
  duration: 2000
});
```

### 错误消息

```javascript
componentutils.showErrorMessage({
  message: "操作失败: " + errMsg,
  duration: 3000
});
```

### 警告消息

```javascript
componentutils.showWarningMessage({
  message: "请填写完整信息",
  duration: 2000
});
```

### 一般消息

```javascript
componentutils.showMessage({
  message: "这是提示信息",
  duration: 2000
});
```

## 对话框

### 确认对话框

```javascript
this.$confirm({
  title: "提示",
  message: "确定要删除这条数据吗?",
  type: "warning"  // warning / info / success / error
}).then(function(action) {
  // 点击确认按钮
  console.log('确认', action);
}).catch(function(action) {
  // 点击取消按钮
  console.log('取消', action);
});
```

### 警告对话框

```javascript
this.$alert({
  title: "提示",
  message: "操作已完成",
  type: "info",
  confirmButtonText: "确定"
}).then(function() {
  // 点击确定按钮
});
```

## 表单验证

### 验证规则定义

```javascript
data: function() {
  return {
    rules: {
      itemKey: [
        { required: true, message: "请输入物料编号", trigger: "blur" }
      ],
      itemType: [
        { required: true, message: "请选择物料类型", trigger: "change" }
      ],
      planQty: [
        { required: true, message: "请输入计划数量", trigger: "blur" },
        { type: "number", message: "请输入有效数字", trigger: "blur" }
      ]
    }
  };
}
```

### 表单验证

```javascript
methods: {
  saveBtnClick: function() {
    var self = this;
    self.$refs.form.validate(function(valid) {
      if (valid) {
        // 验证通过,执行保存
        self.doSave();
      } else {
        // 验证失败
        componentutils.showErrorMessage({
          message: "请填写完整信息"
        });
      }
    });
  }
}
```

### 重置表单

```javascript
methods: {
  resetBtnClick: function() {
    this.$refs.form.resetFields();
  }
}
```

## 常用工具方法

### 获取当前日期

```javascript
// 今天
var today = VueUtil.formatDate(new Date(), 'yyyy-MM-dd');

// 昨天
var yesterday = VueUtil.formatDate(new Date(Date.now() - 86400000), 'yyyy-MM-dd');

// 明天
var tomorrow = VueUtil.formatDate(new Date(Date.now() + 86400000), 'yyyy-MM-dd');

// 本月初
var monthStart = new Date();
monthStart.setDate(1);
var monthStartStr = VueUtil.formatDate(monthStart, 'yyyy-MM-dd');

// 本月末
var monthEnd = new Date();
monthEnd.setMonth(monthEnd.getMonth() + 1);
monthEnd.setDate(0);
var monthEndStr = VueUtil.formatDate(monthEnd, 'yyyy-MM-dd');
```

### 日期比较

```javascript
// 判断日期是否过期
var planDate = VueUtil.parseDate(row.planDate, 'yyyy-MM-dd');
var now = new Date();
if (planDate < now) {
  // 已经过期
}
```

### 数据转换

```javascript
// 数组转对象
var typeMap = dataList.reduce(function(map, item) {
  map[item.key] = item.label;
  return map;
}, {});

// 对象数组去重
var uniqueData = VueUtil.unique(dataList, 'itemKey');
```

### 获取用户信息

```javascript
// 获取用户ID
var userId = PJUserAccessor.getUserDetail().getUserId();

// 获取站点ID
var siteId = store.state.userSiteId;

// 获取工厂ID
var factoryId = store.state.userFactoryId;
```

## 完整查询条件区示例

```html
<escort-row id="vueRow_condition" ref="vueRow_condition">
  <escort-col :inline="true" :md="{span:6}" align="left">
    <escort-input
      v-model="form.itemKey"
      prop="itemKey"
      :label-value="messageutil.get('物料编号')"
      label-width="100px"
      placeholder="请输入物料编号"
      :style_="{ width: '200px' }">
    </escort-input>
  </escort-col>
  <escort-col :inline="true" :md="{span:6}" align="left">
    <escort-select
      v-model="form.itemType"
      :datasource="vueDataSet_itemType"
      value-member="key1"
      display-member="codeData1"
      :label-value="messageutil.get('物料类型')"
      label-width="100px"
      :filterable="true">
    </escort-select>
  </escort-col>
  <escort-col :inline="true" :md="{span:6}" align="left">
    <escort-datetime-picker
      v-model="form.planDate"
      prop="planDate"
      value-format="yyyy-MM-dd"
      type="date"
      :label-value="messageutil.get('计划日期')"
      label-width="100px"
      format="ymd">
    </escort-datetime-picker>
  </escort-col>
  <escort-col :inline="true" :md="{span:6}" align="right">
    <escort-button type="primary" size="small" @click="searchBtnClick">
      {{messageutil.get('查询')}}
    </escort-button>
    <escort-button type="success" size="small" @click="saveBtnClick">
      {{messageutil.get('保存')}}
    </escort-button>
    <escort-button type="warning" size="small" @click="resetBtnClick">
      {{messageutil.get('重置')}}
    </escort-button>
  </escort-col>
</escort-row>
```

## 完整按钮行示例

```html
<escort-row id="vueRow_buttons" ref="vueRow_buttons">
  <escort-col align="right" :inline="true" :md="{span:24}">
    <escort-button type="primary" size="small" @click="newClick">
      {{messageutil.get('新建')}}
    </escort-button>
    <escort-button type="success" size="small" @click="saveClick">
      {{messageutil.get('保存')}}
    </escort-button>
    <escort-button type="warning" size="small" @click="resetClick">
      {{messageutil.get('重置')}}
    </escort-button>
    <escort-button type="info" size="small" @click="exportClick">
      {{messageutil.get('导出')}}
    </escort-button>
  </escort-col>
</escort-row>
```
