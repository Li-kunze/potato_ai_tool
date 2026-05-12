---
name: flexplanner-frontend
description: 创建 FlexPlanner 项目的 Escort 前台页面。使用 Escort UI 组件库编写 Vue2 前台代码。适用于: (1) 查询+Grid 展示页面, (2) 表单编辑页面, (3) 弹窗/侧边栏子页面。使用 Escort 组件(escort-button, escort-xgrid, escort-form 等), 遵循项目标准三段式结构(style/template/script), 代码注释使用中文。
---

# FlexPlanner 前台画面开发 Skill

本 Skill 用于生成符合 FlexPlanner 项目规范的 Escort 前台页面。

## 技能触发条件

当用户请求创建或修改 FlexPlanner 前台页面时触发此技能,例如:
- "创建一个物料查询页面"
- "制作一个表单编辑页面"
- "写一个包含 Grid 和弹窗的前台页面"

## 项目结构

```
flexplanner-web/src/main/webapp/
├── views/              # 页面文件目录
│   ├── MODULE/         # 功能模块目录(如 PP, DDMRP, APS 等)
│   │   └── MODULE_XX/  # 功能子模块
│   │       └── MODULE_XX_01.html  # 页面文件
├── resources/          # 资源文件目录
│   ├── css/            # 样式文件
│   ├── js/             # JavaScript 文件
│   └── images/         # 图片资源
```

## 页面标准结构

FlexPlanner 页面采用标准的三段式结构:

```html
<style type="text/css" scoped>
  <!-- 自定义样式 -->
</style>

<template>
  <div v-cloak class="page" v-loading="pageLoading" :vue-loading-text="messageutil.get('page.loading.text')">
    <escort-form ref="form" id="form" :model="form">
      <!-- 页面内容 -->
    </escort-form>
  </div>
</template>

<script type="text/javascript">
  var pageMixins;
  (function() {
    var pageMixinMap = {};
    pageMixinMap.event = {
      methods: { /* 事件处理 */ }
    };
    pageMixinMap.manualCommon = [{
      props: { /* 父组件传参 */ }
    }];
    pageMixinMap.manualSeperate = {
      methods: { /* 业务逻辑 */ },
      computed: { /* 计算属性 */ }
    };
    pageMixinMap.auto = {
      data: function() {
        return {
          pageLoading: false,
          form: { /* 表单数据 */ },
          vueDataSet_xxx: this.getDataSource({ /* 数据源 */ })
        };
      },
      mounted: function() { /* 初始化 */ }
    };
    pageMixins = getPageMixins(pageMixinMap);
  })();
  module.exports = {
    mixins: pageMixins,
    name: "pageNumber"
  };
</script>
```

## 核心工作流程

### 1. 确定页面功能类型

根据需求确定页面类型:
- **查询+Grid 展示页**: 包含查询条件、按钮、XGrid 表格
- **表单编辑页**: 包含表单输入、验证、保存按钮
- **弹窗/侧边栏子页**: 用于详情查看、编辑子页面

### 2. 选择合适的 Escort 组件

常用 Escort 组件:
- 表单容器: `escort-form`
- 布局组件: `escort-row`, `escort-col`
- 输入组件: `escort-input`, `escort-select`, `escort-datetime-picker`, `escort-textarea`
- 按钮组件: `escort-button`
- 表格组件: `escort-xgrid`
- 弹窗组件: `escort-window` (居中弹窗), `escort-aside` (侧边栏)

### 3. 配置 DataSource 数据源

DataSource 是前后端数据交互的核心:

```javascript
vueDataSet_xxx: this.getDataSource({
  url: "/api/endpoint.json",    // 后端接口
  type: "POST",                  // 请求方式
  parameter: {                   // 请求参数
    param1: value1
  },
  success: this.vueDataSetXxxSuccess  // 成功回调
})
```

详细配置说明见 [datasource-config.md](references/datasource-config.md)

### 4. 编写 XGrid 表格

XGrid 是 Escort 的核心表格组件,支持多种列类型:

```html
<escort-xgrid :data="gridData" height="400">
  <escort-xgrid-column type="checkbox" width="50px"></escort-xgrid-column>
  <escort-xgrid-column type="index" width="50px"></escort-xgrid-column>
  <escort-xgrid-column prop="itemKey" text="物料编号" render-name="input"></escort-xgrid-column>
  <escort-xgrid-column prop="planDate" text="计划日期" render-name="date"></escort-xgrid-column>
  <escort-xgrid-column fixed="right" :buttons="vueXgridButtons" render-name="button"></escort-xgrid-column>
</escort-xgrid>
```

详细列类型说明见 [grid-column-types.md](references/grid-column-types.md)

### 5. 绑定事件和方法

按钮点击事件:
```javascript
methods: {
  searchBtnClick: function(event) {
    this.vueDataSet_search.retrieve();
  }
}
```

XGrid 列按钮:
```javascript
methods: {
  vueXgridButtons: function(scope) {
    return [{
      value: "编辑",
      size: 'small',
      type: 'text',
      click: this.editClick,
      hidden: scope.row.status === 'locked'
    }];
  }
}
```

## 组件属性映射

ViyUI (Vue2) 组件与 Escort 组件的属性基本相同:

| ViyUI | Escort | 说明 |
|-------|--------|------|
| vue-button | escort-button | 按钮组件,type/size/icon 属性一致 |
| vue-input | escort-input | 输入框组件,v-model/placeholder 属性一致 |
| vue-select | escort-select | 下拉组件,options/v-model 属性一致 |
| vue-datetime-picker | escort-datetime-picker | 日期组件,value-format/type 属性一致 |

更多映射关系见 [component-mapping.md](references/component-mapping.md)

## 代码规范

1. **中文注释**: 所有代码注释必须使用中文
2. **命名规范**:
   - 页面命名: `MODULE_XX_YY.html` (MODULE: 模块名, XX: 功能编号, YY: 页面序号)
   - 方法命名: `vueComponentNameClick` (按钮点击), `vueDataSetXxxSuccess` (数据回调)
   - ID/Ref: `vueComponentName` (vue 前缀)
3. **国际化文本**: 使用 `messageutil.get('key')` 获取国际化文本
4. **消息提示**:
   - 成功: `componentutils.showSuccessMessage({ message: "xxx" })`
   - 错误: `componentutils.showErrorMessage({ message: "xxx" })`
   - 确认: `this.$confirm({ title: "提示", message: "xxx", type: "warning" })`

## 常用代码片段

详见 [common-components.md](references/common-components.md)

## API 集成

后端 Controller 使用 Spring Boot 注解:

```java
@Controller
@RequestMapping("/flexplannerApi/xxx")
public class XxxController {
    @PostMapping(value = "/saveXxx")
    @ResponseBody
    public RestBaseModel saveXxx(@RequestBody XxxModel model) {
        return new RestBaseModel<>(200, "保存成功");
    }
}
```

前段 DataSource 对应配置见 [api-integration.md](references/api-integration.md)

## 参考模板

- 空页面模板: [assets/templates/empty-template.html](assets/templates/empty-template.html)
- 完整示例页面: [assets/templates/sample-page.html](assets/templates/sample-page.html)

---

## 常见页面模式(实战总结)

基于项目实际页面分析,以下为6种常见页面模式的完整模板:

### 1. 查询+Grid内联编辑页 (参考: CRP0001_01.html)

**适用场景**: 需要查询条件、分页Grid、支持行内编辑、侧边栏详情的页面

**核心特征**:
- 条件区 + 查询/导出/更新按钮
- Grid分页、合计行显示
- 条件编辑逻辑
- 双击行打开侧边栏

**完整代码结构**:

```javascript
// pageMixinMap.manualCommon methods
methods: {
  // 条件编辑方法 determining whether cell is editable
  gridActiveMethod: function(obj) {
    // obj = {row, rowIndex, column, columnIndex}
    // 返回 true: 可编辑, false: 不可编辑
    if (obj.column.property == 'fieldAlwaysEditable') {
      return true;
    }
    if (obj.row.conditionField == 'value' && 
        (obj.column.property == 'fieldConditionalEditable1' || 
         obj.column.property == 'fieldConditionalEditable2')) {
      return true;
    }
    return false;
  },

  // 下拉列change事件
  gridFieldXxxChange: function(obj, newValue, newOption, oldValue) {
    var row = obj.row;
    if (newValue == '0') {
      row.fieldY = 0;
      row.fieldZ = 0;
    }
  },

  // 查询按钮
  searchBtnClick: function(event) {
    this.$refs.grid.paginationReturnToFirst();
    this.vueDataSet_grid.retrieve();
  },

  // 导出按钮
  exportBtnClick: function(event) {
    var self = this;
    var url = contextPath + "/ddmrp/exportTempleteGrid/PAGE_CODE";
    var body = {
      grid: 'grid',
      condition: self.getSearchParams()
    };
    self.exportGrid(url, body);
  },

  // 更新按钮
  updateBtnClick: function(event) {
    var self = this;
    var updateRows = self.$refs.grid.getUpdateRows();
    self.$refs.grid.validate(function(valid) {
      if (valid) {
        var body = { dataList: updateRows };
        var url = contextPath + "/api/updateData.json";
        var issueSuccess = function(response) {
          successMessage('label.operationSuccess');
          self.vueDataSet_grid.retrieve();
        };
        createFormPost(url, body, issueSuccess);
      }
    });
  },

  // 双击Grid行
  gridCellDblclick: function(obj, event) {
    var self = this;
    if (obj.column.property != 'fieldEditable') {
      self.$refs.pageAside.open({
        form: obj.row
      }, null);
    }
  },

  // 获取查询参数(包含分页)
  getSearchParams: function() {
    var self = this;
    var paginationObj = {
      currentPageSize: self.$refs.grid.getPageParams().pageSize,
      currentPage: self.$refs.grid.getPageParams().currentPage
    };
    return VueUtil.merge(VueUtil.cloneDeep(self.conditionForm), paginationObj);
  },

  // 列formatter(如百分比显示)
  gridFieldXxxFormatter: function(row, columnConfig, cellValue) {
    return cellValue + '%';
  }
}

// pageMixinMap.watch
watch: {
  conditionForm: {
    handler: function(newVal, oldVal) {
      this.vueDataSet_grid.data = {};
      this.$refs.grid.$refs.grid.clearFilter();
      this.$refs.grid.$refs.grid.clearSort();
    },
    deep: true
  }
}

// pageMixinMap.auto data
data: function() {
  return {
    conditionForm: { /* 查询条件字段 */ },
    gridRules: { /* Grid行验证规则 */ },
    gridFieldXxxEvents: { "change": this.gridFieldXxxChange },
    vueDataSet_grid: this.getDataSource({
      url: "/api/getGridData.json",
      type: "POST",
      parameter: this.getSearchParams,
      success: this.vueDataSetGridSuccess
    }),
    codeDs: this.getDataSource({
      url: "/common/getCodeList.json",
      type: "POST",
      parameter: { 'codeId': 'CODE_ID' },
      emulateJSON: true
    })
  };
}

// Grid列配置示例
/* 
<escort-xgrid :edit-config="{trigger: 'click', mode: 'row', activeMethod: gridActiveMethod}">
  <escort-xgrid-column 
    prop="fieldSelect" 
    render-name="select"
    :template="true"
    :edit-render-events="gridFieldXxxEvents"
    :edit-render-attrs-options="codeDs.data"
    :edit-render-attrs-datasource="codeDs"
    edit-render-attrs-display-member="codeData1"
    edit-render-attrs-value-member="key1"
    :editable="true">
    <template slot="default" slot-scope="scope">
      <escort-xgrid-column-display 
        :row="scope.row" 
        field="fieldSelect" 
        widget-type="select" 
        display-member="codeData1" 
        value-member="key1"
        display-type="tag"
        :options="codeDs.data">
      </escort-xgrid-column-display>
    </template>
  </escort-xgrid-column>
  
  <escort-xgrid-column 
    prop="fieldNumeric" 
    render-name="numeric"
    :edit-render-attrs-decimal-scale="0"
    :formatter="gridFieldXxxFormatter"
    :editable="true">
  </escort-xgrid-column>
</escort-xgrid>
*/
```

### 2. 纯查询Grid页 (参考: CRP0002_01.html)

**适用场景**: 只需查询、无编辑、支持导出的列表页

**核心特征**:
- 条件区 + 查询/导出按钮
- Grid分页
- 无编辑功能
- 导出带下拉数据映射

**关键代码**:

```javascript
// 导出带mapData转换
doExport: function() {
  var self = this;
  var url = contextPath + "/ddmrp/exportTempleteGrid/PAGE_CODE";
  var body = {
    grid: 'grid',
    condition: self.getSearchParams(),
    mapData: {
      // code转desc的映射
      fieldName1: self.resolveDropdownMstCode(self.codeDs1),
      fieldName2: self.resolveDropdownMstCode(self.codeDs2)
    }
  };
  self.exportGrid(url, body);
},

// 下拉映射方法
resolveDropdownMstCode: function(_ds) {
  var dropdownData = _ds.data;
  var colDropdown = {};
  for (var key in dropdownData) {
    colDropdown[dropdownData[key].key1] = dropdownData[key].codeData1;
  }
  return colDropdown;
}
```

### 3. 侧边栏详情页 (参考: CRP0001_02.html)

**适用场景**: 从父页面双击打开的侧边栏,用于显示/编辑详细信息

**核心特征**:
- `vue-aside-header` 标题栏
- 分区域 `escort-collapse` 折叠面板
- 从父组件接收数据(`this.$attrs.params`)
- 嵌套Grid(如资源列表)

**关键代码**:

```html
<template>
  <div v-loading="pageLoading">
    <vue-aside-header 
      :headtitle="$t('title.xxx')" 
      @back="$emit('close')">
    </vue-aside-header>
    <div class="contentPadding scroll">
      <escort-form ref="form" id="form" :model="form">
        <escort-area cls="conditionPart">
          <escort-form id="conditionForm" ref="conditionForm" :model="conditionForm">
            <!-- 表单字段 -->
          </escort-form>
        </escort-area>
        <escort-area cls="detailPart">
          <!-- 嵌套Grid -->
        </escort-area>
      </escort-form>
    </div>
  </div>
</template>

<script>
pageMixinMap.manualCommon = [{
  created: function() {
    // 从父页面加载数据
    var form = VueUtil.merge(this.conditionForm, this.$attrs.params.form);
  },
  mounted: function() {
    var self = this;
    setTimeout(function() {
      Vue.autoSetAsideGridHeight(self, 60);
    }, 0);
    VueUtil.addResizeListener(document.body, self.resizeEvent);
  }
}];
</script>
```

### 4. 复杂条件+动态组件页 (参考: PP0001_01.html)

**适用场景**: 多布局条件区、动态切换显示组件(图表/表格)、侧边栏+弹窗组合

**核心特征**:
- 多行条件布局(escort-row)
- `escort-collapse` 包裹动态组件
- 动态组件加载 `<component :is="form.chartDiv">`
- 侧边栏和弹窗组合使用

**关键代码**:

```html
<template>
  <escort-form>
    <!-- 条件区1: 单选按钮 -->
    <escort-row>
      <escort-radio-button 
        :options="vueDataSet_type.data"
        v-model="form.chartDiv">
      </escort-radio-button>
    </escort-row>
    
    <!-- 条件区2: 日期+下拉框+按钮 -->
    <escort-row>
      <escort-datetime-picker v-model="form.calDateFrom"></escort-datetime-picker>
      <escort-datetime-picker v-model="form.calDateTo"></escort-datetime-picker>
      <escort-select v-model="form.workCenterList" :multiple="true"></escort-select>
      <escort-button @click="searchBtnClick">查询</escort-button>
      <escort-button @click="openColorSetting">颜色设置</escort-button>
    </escort-row>
    
    <!-- 动态组件区域 -->
    <escort-collapse :show-arrow="false">
      <component ref="showPage" :is="form.chartDiv" :form="form"></component>
    </escort-collapse>
    
    <!-- 侧边栏 -->
    <escort-aside ref="colorSettingAside" src="/xxx/xxx_04.html"></escort-aside>
    
    <!-- 弹窗 -->
    <escort-window v-model="saveVersionFlag" title="保存版本">
      <!-- 弹窗内容 -->
    </escort-window>
  </escort-form>
</template>

<script>
// 动态加载子组件
created: function() {
  this.$options.components['componentCode1'] = VueLoader('../../../views/PP/PP0001/PP0001_02.html');
  this.$options.components['componentCode2'] = VueLoader('../../../views/PP/PP0001/PP0001_03.html');
}

// 调用子组件方法
doSearch: function() {
  // 调用动态子组件的DataSource
  this.$refs.showPage.vueDataSet_grid.retrieve();
}
</script>
```

### 5. Grid嵌套ECharts页 (参考: PP0001_02.html)

**适用场景**: Grid列中嵌套ECharts图表(如产能负荷可视化)

**核心特征**:
- Grid列使用 `v-for` 动态生成
- 列中嵌套 `escort-echarts`
- ECharts option配置复杂
- 点击单元格弹出快捷菜单

**关键代码**:

```html
<escort-xgrid>
  <escort-xgrid-column 
    v-for="(column,column_index) in vueDataSet_title.data"
    :key="column_index"
    :template="true"
    :template-header="true"
    :prop="'listData.['+column_index+']'"
    align="center"
    width="180px">
    
    <template slot="header" slot-scope="scope">
      <vue-row>
        <vue-col :span="24">
          <span>{{column.calUnit}}</span>
        </vue-col>
      </vue-row>
    </template>
    
    <template slot="default" slot-scope="scope">
      <escort-echarts 
        :id="'echarts_' + scope.row._XID + '_' + column_index"
        :option="getOption(scope.row, column_index)"
        :style_="{width:'170px', height:'195px'}">
      </escort-echarts>
    </template>
  </escort-xgrid-column>
</escort-xgrid>

<script>
methods: {
  getOption: function(row, index) {
    var number = row.listData[index].actualValue;
    var maxValue = row.listData[index].maxValue;
    
    var option = {
      grid: { x: -1, y: 0, x2: 0, y2: 0 },
      xAxis: [{
        type: 'category',
        axisLabel: { show: false }
      }],
      yAxis: [{
        type: 'value',
        axisLabel: { show: false },
        min: 0,
        max: maxValue
      }],
      series: [
        { type: 'line', data: Array(10).fill(maxValue * 0.7) },
        { type: 'line', showSymbol: false, itemStyle: { color: this.getBgColor(number, maxValue) } }
      ]
    };
    return option;
  }
}
</script>
```

### 6. 模板侧边栏页 (参考: PP0001_04.html)

**适用场景**: 简单项管理(如标签、颜色设置)

**核心特征**:
- 简单的输入+选择组合
- `escort-color-picker` 颜色选择器
- 标签添加/删除操作

**关键代码**:

```html
<template>
  <escort-form>
    <!-- 标签列表 -->
    <escort-row>
      <escort-col v-for="(tag, index) in form.colorSettingTags">
        <vue-tag 
          :closable="tag.closable" 
          @close="tagCloseHandle(tag)"
          :style="'background-color:'+tag.backgroundColor">
          &nbsp;
        </vue-tag>
        <escort-input v-model="tag.showText" :disabled="true"></escort-input>
      </escort-col>
    </escort-row>
    
    <!-- 添加新标签 -->
    <escort-row>
      <escort-color-picker v-model="form.setColorValue"></escort-color-picker>
      <escort-input v-model="form.setColorNumberValue"></escort-input>
      <escort-button @click="addTag">添加</escort-button>
    </escort-row>
  </escort-form>
</template>

<script>
methods: {
  addTag: function() {
    this.form.colorSettingTags.push({
      name: this.form.setColorNumberValue,
      backgroundColor: this.form.setColorValue,
      closable: true
    });
  },
  tagCloseHandle: function(tag) {
    this.form.colorSettingTags.splice(this.form.colorSettingTags.indexOf(tag), 1);
  }
}
</script>
```

---

## DataSource 常见配置模板

### 1. 列表查询DataSource (最常用)

```javascript
vueDataSet_grid: this.getDataSource({
  url: "/api/getDataByPage.json",
  type: "POST",
  parameter: this.gridDsParameter,  // 必须是函数
  emulateJSON: true
}),

// 参数构建方法
gridDsParameter: function() {
  var self = this;
  var paginationObj = {
    currentPageSize: self.$refs.grid.getPageParams().pageSize,
    currentPage: self.$refs.grid.getPageParams().currentPage
  };
  return VueUtil.merge(VueUtil.cloneDeep(self.conditionForm), paginationObj);
}
```

### 2. 字典数据DataSource (下拉选项)

```javascript
// 标准字典
workCenterTypeDs: this.getDataSource({
  url: "/common/getCodeList.json",
  type: "POST",
  parameter: { codeId: 'CRP_WC_CLA' },
  emulateJSON: true
}),

// 自定义接口下拉
workCenterDs: this.getDataSource({
  url: "/crp/getWorkCenterDropDownListInfo.json",
  type: "POST",
  parameter: { paramType: 'xxx' }
})
```

### 3. 带成功回调DataSource

```javascript
vueDataSet_grid: this.getDataSource({
  url: "/api/getData.json",
  type: "POST",
  parameter: this.gridDsParameter,
  success: this.gridDsSuccess,
  error: this.gridDsError
}),

methods: {
  gridDsSuccess: function(response) {
    if (response && response.code === 200) {
      // 处理成功响应
      this.gridDs.data = response.content || [];
    }
  },
  gridDsError: function(response) {
    // 处理错误
    componentutils.showErrorMessage({ message: (response && response.message) || '加载失败' });
  }
}
```

### 4. 初始化后自动加载DataSource

```javascript
mounted: function() {
  this.vueDataSet_grid.retrieve();
  this.codeDs1.retrieve();
  this.codeDs2.retrieve();
}
```

---

## Grid 高级配置

### 1. 条件编辑逻辑 (gridActiveMethod)

```javascript
// 列级别控制
edit-config: {
  trigger: 'click',
  mode: 'row',
  activeMethod: function(obj) {
    if (obj.column.property == 'fieldA') return true;  // fieldA始终可编辑
    if (obj.row.fieldB == '1' && obj.column.property == 'fieldC') return true;  // 条件可编辑
    return false;
  }
}

// 单列条件控制(通过属性)
<escort-xgrid-column 
  :gridActiveMethod="function(obj) {
    return obj.row.status == '1';
  }">
</escort-xgrid-column>
```

### 2. 下拉列change事件处理

**步骤**:
1. 在data中定义事件对象
2. 列配置绑定事件
3. 实现change方法

```javascript
// data中定义
gridFieldEvents: { "change": this.gridFieldChange },

// 列配置
<escort-xgrid-column 
  :edit-render-events="gridFieldEvents"
  render-name="select"
  :datasource="codeDs">
</escort-xgrid-column>

// change方法
gridFieldChange: function(obj, newValue, newOption, oldValue) {
  var row = obj.row;
  if (newValue == '0') {
    row.field1 = 0;
    row.field2 = '';
  } else if (newValue == '1') {
    row.field1 = 100;
  }
}
```

### 3. 列formatter格式化

```javascript
// 百分比格式化
<escort-xgrid-column 
  :formatter="gridPercentFormatter">
</escort-xgrid-column>

methods: {
  gridPercentFormatter: function(row, columnConfig, cellValue) {
    return (Number(cellValue)).toFixed(0) + '%';
  }
}

// 日期格式化
<escort-xgrid-column 
  :formatter="gridDateFormatter">
</escort-xgrid-column>

methods: {
  gridDateFormatter: function(row, columnConfig, cellValue) {
    return cellValue ? VueUtil.formatDate(cellValue, 'yyyy-MM-dd') : '';
  }
}

// 条件格式化
<escort-xgrid-column 
  :formatter="gridConditionFormatter">
</escort-xgrid-column>

methods: {
  gridConditionFormatter: function(row, columnConfig, cellValue) {
    if (row.workCenterType === 'EQUIP') {
      return '';
    }
    return cellValue;
  }
}
```

### 4. 动态列生成 (v-for)

**适用于**: 时间序列表、多维度数据显示

```html
<escort-xgrid :data="vueDataSet_grid.data">
  <escort-xgrid-column prop="fixedCol" text="固定列" fixed="left"></escort-xgrid-column>
  
  <!-- 动态列 -->
  <escort-xgrid-column 
    v-for="(column,column_index) in vueDataSet_title.data" 
    :key="column_index"
    :template="true"
    :template-header="true"
    :prop="'dynamicData.['+column_index+']'"
    :text="column.headerName"
    width="150px">
    
    <template slot="header" slot-scope="scope">
      <vue-row>
        <vue-col :span="24">
          <span>{{column.headerName}}</span>
        </vue-col>
      </vue-row>
    </template>
    
    <template slot="default" slot-scope="scope">
      <vue-row>
        <vue-col :span="12">
          显示内容1
        </vue-col>
        <vue-col :span="12">
          显示内容2
        </vue-col>
      </vue-row>
    </template>
  </escort-xgrid-column>
</escort-xgrid>
```

### 5. 自定义汇总 (aggregate)

```javascript
// 页面全局方法
loopColumnAggregate: function(escortColumn, columnIndex, data) {
  var sumValue = VueUtil.sumBy(data, function(row, index) {
    return row.dynamicData[columnIndex - 2].value;
  });
  return '合计: ' + sumValue;
}

// 列配置
<escort-xgrid-column 
  :aggregate="loopColumnAggregate"
  show-footer="true">
</escort-xgrid-column>
```

### 6. 列级样式条件

```javascript
// 方法定义样式
<escort-xgrid-column 
  :class-name="function(rowIndex, cellIndex, row) {
    if (row.status != '1') {
      return 'unedit-cell';
    }
    return '';
  }">
</escort-xgrid-column>

// CSS样式
<style scoped>
  .unedit-cell {
    background-color: #eef1f6;
  }
  .row--current .unedit-cell {
    background-color: #e6f7ff;
  }
</style>
```

---

## ViyUI 组件库文档

ViyUI 组件库完整文档位于项目 `ViyUI/VIY2/docs/docs/` 目录下,包含所有 Escort 组件的详细说明。

## 注意事项

1. 页面必须使用 `escort-form` 作为根容器
2. 所有 Escort 组件都需要 `id` 和 `ref` 属性
3. 表单字段需要 `v-model` 绑定和 `prop` 属性用于验证
4. 数据源调用使用 `.retrieve()` 方法
5. 使用 `this.$refs.ref` 访问组件实例
