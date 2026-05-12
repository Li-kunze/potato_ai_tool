# XGrid 列类型详解

XGrid 是 Escort 的核心表格组件,支持多种列类型用于数据展示和编辑。

## 基础配置

```html
<escort-xgrid
  id="vueXgrid_main"
  ref="vueXgrid_main"
  :data="gridData"
  height="400"
  border
  stripe
  highlight-current-row>

  <!-- 列定义 -->
  <escort-xgrid-column prop="xxx" text="xxx" width="100px"></escort-xgrid-column>
</escort-xgrid>
```

## 固定列类型

### 复选框列 (type="checkbox")

用于多选行的复选框列。

```html
<escort-xgrid-column type="checkbox" width="50px" align="center"></escort-xgrid-column>
```

**常用属性:**
- `type="checkbox"`: 必需,标识为复选框列
- `width="50px"`: 固定宽度 50px
- `align="center"`: 居中对齐

**获取选中行:**
```javascript
// 获取所有选中的行
var selectedRows = this.$refs.vueXgrid_main.getSelectRecords();

// 获取选中行的 ID
var selectedIds = selectedRows.map(function(item) {
  return item.id;
});
```

### 序号列 (type="index")

显示行序号的列。

```html
<escort-xgrid-column type="index" width="50px" align="center" min-width="50px"></escort-xgrid-column>
```

**常用属性:**
- `type="index"`: 必需,标识为序号列
- `width="50px"`: 固定宽度 50px
- `min-width="50px"`: 最小宽度

### 单选列 (type="radio")

用于单选行的单选框列。

```html
<escort-xgrid-column type="radio" width="50px" align="center"></escort-xgrid-column>
```

## 可编辑列类型

### 文本输入列 (render-name="input")

可编辑的文本输入框列。

```html
<escort-xgrid-column
  prop="itemKey"
  text="物料编号"
  width="120px"
  show-overflow="ellipsis"
  render-name="input">
</escort-xgrid-column>
```

**常用属性:**
- `render-name="input"`: 必需,标识为输入框列
- `show-overflow="ellipsis"`: 超长显示省略号

### 文本域列 (render-name="textarea")

可编辑的多行文本域列。

```html
<escort-xgrid-column
  prop="remark"
  text="备注"
  width="200px"
  show-overflow="tooltip"
  render-name="textarea">
</escort-xgrid-column>
```

### 下拉选择列 (render-name="select")

可编辑的下拉选择列。

```html
<escort-xgrid-column
  prop="itemType"
  text="物料类型"
  width="120px"
  render-name="select"
  :options="itemTypeOpts">
</escort-xgrid-column>
```

**选项绑定方式:**
```javascript
// 在 computed 中定义选项
computed: {
  itemTypeOpts: function() {
    return [
      { value: 'RAW', label: '原材料' },
      { value: 'SEMI', label: '半成品' },
      { value: 'FINISHED', label: '成品' }
    ];
  }
}
```

### 日期列 (render-name="date")

可编辑的日期选择列。

```html
<escort-xgrid-column
  prop="planDate"
  text="计划日期"
  width="120px"
  render-name="date"
  edit-render-value-format="yyyy-MM-dd"
  format="ymd">
</escort-xgrid-column>
```

**日期格式说明:**
- `edit-render-value-format="yyyy-MM-dd"`: 编辑时绑定值格式
- `format="ymd"`: 显示格式 (ymd=年月日, ymdt=年月日时分秒)

**日期时间列:**
```html
<escort-xgrid-column
  prop="createTime"
  text="创建时间"
  width="180px"
  render-name="date"
  edit-render-value-format="yyyy-MM-dd HH:mm:ss"
  format="ymdt">
</escort-xgrid-column>
```

### 数值列 (render-name="numeric")

可编辑的数值输入列。

```html
<escort-xgrid-column
  prop="planQty"
  text="计划数量"
  width="100px"
  align="right"
  render-name="numeric">
</escort-xgrid-column>
```

**常用属性:**
- `align="right"`: 右对齐
- `precision="2"`: 小数位数(可选)

### 复选框列 (render-name="checkbox")

可编辑的复选框列 (true/false)。

```html
<escort-xgrid-column
  prop="isActive"
  text="启用"
  width="80px"
  align="center"
  render-name="checkbox">
</escort-xgrid-column>
```

### 单选列 (render-name="radio")

可编辑的单选框列。

```html
<escort-xgrid-column
  prop="type"
  text="类型"
  width="100px"
  render-name="radio"
  :options="typeOpts">
</escort-xgrid-column>
```

### 开关列 (render-name="switch")

可编辑的开关列。

```html
<escort-xgrid-column
  prop="enabled"
  text="启用"
  width="80px"
  align="center"
  render-name="switch">
</escort-xgrid-column>
```

## 只读列类型

### 文本列 (无 render-name)

纯文本显示列,不可编辑。

```html
<escort-xgrid-column
  prop="itemName"
  text="物料名称"
  width="150px"
  show-overflow="ellipsis">
</escort-xgrid-column>
```

**常用属性:**
- `prop="xxx"`: 数据字段名
- `text="xxx"`: 表头文本
- `width="100px"`: 列宽度
- `show-overflow="ellipsis"`: 超长显示省略号
- `show-overflow="tooltip"`: 超长显示提示框

## 自定义渲染列

### 模板列 (template="true")

使用 Vue 插槽自定义渲染。

```html
<escort-xgrid-column
  prop="status"
  text="状态"
  width="100px"
  :template="true"
  render-name="template">
  <template slot="default" slot-scope="scope">
    <span :class="getStatusCss(scope.row)">
      {{scope.row.status}}
    </span>
  </template>
</escort-xgrid-column>
```

**样式方法:**
```javascript
methods: {
  getStatusCss: function(row) {
    var status = row.status;
    if (status === '已完成') {
      return ['status-blue'];
    } else if (status === '待处理') {
      return ['status-red'];
    }
    return [];
  }
}
```

**CSS:**
```html
<style type="text/css" scoped>
  .status-blue {
    color: #409eff;
    font-weight: bold;
  }
  .status-red {
    color: #f56c6c;
    font-weight: bold;
  }
</style>
```

### 链接列 (render-name="input-link")

可点击的链接列。

```html
<escort-xgrid-column
  prop="itemKey"
  text="物料编号"
  width="120px"
  render-name="input-link"
  :click="itemKeyClick">
</escort-xgrid-column>
```

**点击方法:**
```javascript
methods: {
  itemKeyClick: function(row) {
    // 打开详情页
    this.$refs.vueAside_detail.open({
      id: row.id,
      parent: this
    });
  }
}
```

### 图片列 (render-name="img")

显示图片的列。

```html
<escort-xgrid-column
  prop="imageUrl"
  text="图片"
  width="100px"
  align="center"
  render-name="img">
</escort-xgrid-column>
```

## 操作列

### 按钮列 (render-name="button")

操作按钮列,通常固定在右侧。

```html
<escort-xgrid-column
  fixed="right"
  align="center"
  text="操作"
  width="150px"
  render-name="button"
  :buttons="vueXgridButtons">
</escort-xgrid-column>
```

**按钮配置方法:**
```javascript
methods: {
  vueXgridButtons: function(scope) {
    var self = this;
    return [{
      value: "编辑",
      size: 'small',
      type: 'text',
      click: self.editClick,
      hidden: scope.row.status === 'locked'  // 根据条件隐藏
    }, {
      value: "删除",
      size: 'small',
      type: 'text',
      click: self.deleteClick
    }, {
      value: "查看",
      size: 'small',
      type: 'text',
      click: self.viewClick
    }];
  }
}
```

**按钮点击方法:**
```javascript
methods: {
  editClick: function(row) {
    var self = this;
    // 设置编辑数据
    self.form.editRow = row;
    // 打开编辑弹窗
    self.showEditWindow = true;
  },

  deleteClick: function(row) {
    var self = this;
    self.$confirm({
      title: "提示",
      message: "确定要删除这条数据吗?",
      type: "warning"
    }).then(function(action) {
      // 调用删除接口
      self.vueDataSet_delete.setParameter({ id: row.id });
      self.vueDataSet_delete.retrieve(function(resp) {
        if (resp.code === 200) {
          componentutils.showSuccessMessage({ message: "删除成功" });
          self.searchBtnClick();
        }
      });
    });
  },

  viewClick: function(row) {
    // 打开详情侧边栏
    this.$refs.vueAside_detail.open({
      id: row.id,
      parent: this
    });
  }
}
```

## 常用列属性

### 基础属性
| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| prop | String | 数据字段名 | `prop="itemKey"` |
| text | String | 表头文本 | `text="物料编号"` |
| width | String | 固定宽度 | `width="120px"` |
| min-width | String | 最小宽度 | `min-width="100px"` |
| align | String | 对齐方式 left/center/right | `align="right"` |

### 溢出处理
| 属性 | 值 | 说明 |
|------|-----|------|
| show-overflow | ellipsis | 超长显示省略号 |
| show-overflow | tooltip | 超长显示提示框 |
| show-overflow | title | 超长显示 title |

### 固定列
| 属性 | 值 | 说明 |
|------|-----|------|
| fixed | left | 固定在左侧 |
| fixed | right | 固定在右侧 |

### 可编辑列属性
| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| render-name | String | 列类型 | `render-name="input"` |
| resizable | Boolean | 是否可调整列宽 | `:resizable="true"` |

### 日期列专用
| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| edit-render-value-format | String | 编辑时值格式 | `edit-render-value-format="yyyy-MM-dd"` |
| format | String | 显示格式 | `format="ymd"` 或 `format="ymdt"` |

### 模板列专用
| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| :template | Boolean | 是否为模板列 | `:template="true"` |

### 按钮列专用
| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| :buttons | Function | 按钮配置函数 | `:buttons="vueXgridButtons"` |

## 行样式与单元格样式

### 单元格样式回调

```html
<escort-xgrid :cell-class-name="vueXgridCellClassName">
```

```javascript
methods: {
  vueXgridCellClassName: function(obj) {
    var row = obj.row;
    var column = obj.column;
    var field = column.field;

    // 根据状态设置单元格背景色
    if (field === 'status' && row.status === '待处理') {
      return 'cell-pending';
    }

    // 根据数值设置单元格颜色
    if (field === 'planQty' && row.planQty < 100) {
      return 'cell-warning';
    }

    return '';
  }
}
```

### 行样式回调

```html
<escort-xgrid :row-class-name="vueXgridRowClassName">
```

```javascript
methods: {
  vueXgridRowClassName: function(obj) {
    var row = obj.row;

    // 根据状态设置整行背景色
    if (row.status === 'locked') {
      return 'row-locked';
    }

    // 根据日期设置行背景色
    var planDate = VueUtil.parseDate(row.planDate, 'yyyy-MM-dd');
    var now = new Date();
    if (planDate < now && row.status === '未完成') {
      return 'row-overdue';
    }

    return '';
  }
}
```

**CSS:**
```html
<style type="text/css" scoped>
  .cell-pending {
    background-color: #fef0f0;
    color: #f56c6c;
  }
  .cell-warning {
    background-color: #fdf6ec;
    color: #e6a23c;
  }
  .row-locked {
    background-color: #f4f4f5;
    color: #909399;
  }
  .row-overdue {
    background-color: #fff1f1;
    color: #f56c6c;
  }
</style>
```

## XGrid 常用方法

### 数据操作

```javascript
// 获取选中行
var selectedRows = this.$refs.vueXgrid_main.getSelectRecords();

// 清除选中
this.$refs.vueXgrid_main.clearSelection();

// 插入行
this.$refs.vueXgrid_main.insertRow({ id: 1, itemKey: 'TEST' });

// 删除选中行
this.$refs.vueXgrid_main.removeSelectedRows();

// 获取待保存的行(增删改)
var pendingRows = this.$refs.vueXgrid_main.getPendingRows();
```

### 分页操作

```javascript
// 获取分页参数
var pageParams = this.$refs.vueXgrid_main.getPageParams();

// 返回第一页
this.$refs.vueXgrid_main.paginationReturnToFirst();
```

## 完整示例

```html
<escort-xgrid
  id="vueXgrid_main"
  ref="vueXgrid_main"
  :data="gridData"
  height="400"
  border
  stripe
  highlight-current-row
  :cell-class-name="vueXgridCellClassName">

  <!-- 复选框列 -->
  <escort-xgrid-column type="checkbox" width="50px" align="center"></escort-xgrid-column>

  <!-- 序号列 -->
  <escort-xgrid-column type="index" width="50px" align="center"></escort-xgrid-column>

  <!-- 输入框列 (可编辑) -->
  <escort-xgrid-column
    prop="itemKey"
    text="物料编号"
    width="120px"
    show-overflow="ellipsis"
    render-name="input">
  </escort-xgrid-column>

  <!-- 只读文本列 -->
  <escort-xgrid-column
    prop="itemName"
    text="物料名称"
    width="150px"
    show-overflow="tooltip">
  </escort-xgrid-column>

  <!-- 日期列 (可编辑) -->
  <escort-xgrid-column
    prop="planDate"
    text="计划日期"
    width="120px"
    render-name="date"
    edit-render-value-format="yyyy-MM-dd"
    format="ymd">
  </escort-xgrid-column>

  <!-- 数值列 (可编辑,右对齐) -->
  <escort-xgrid-column
    prop="planQty"
    text="计划数量"
    width="100px"
    align="right"
    render-name="numeric">
  </escort-xgrid-column>

  <!-- 模板列 (自定义渲染) -->
  <escort-xgrid-column
    prop="status"
    text="状态"
    width="100px"
    :template="true"
    render-name="template">
    <template slot="default" slot-scope="scope">
      <span :class="getStatusCss(scope.row)">{{scope.row.status}}</span>
    </template>
  </escort-xgrid-column>

  <!-- 按钮列 (固定右侧) -->
  <escort-xgrid-column
    fixed="right"
    align="center"
    text="操作"
    width="150px"
    render-name="button"
    :buttons="vueXgridButtons">
  </escort-xgrid-column>
</escort-xgrid>
```

## 注意事项

1. **所有列都需要 `prop` 属性**(除了固定列)
2. **可编辑列需要 `render-name` 属性**
3. **按钮列需要 `:buttons` 绑定方法**
4. **模板列需要 `:template="true"`**
5. **数值列建议使用 `align="right"`**
6. **固定列使用 `fixed="left"` 或 `fixed="right"`**
