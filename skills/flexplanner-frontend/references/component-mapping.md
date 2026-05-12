# ViyUI ↔ Escort 组件映射表

本文档说明 ViyUI (Vue2) 组件与 Escort 组件的属性映射关系。

## 映射原则

**核心规则**: ViyUI (vue-) 组件的属性在 Escort (escort-) 组件上基本相同,可以直接使用。

例如:
```html
<!-- Vue2 组件 -->
<vue-button type="primary" size="small" icon="vue-icon-search">查询</vue-button>

<!-- Escort 组件(属性完全一致) -->
<escort-button type="primary" size="small" icon="vue-icon-search">查询</escort-button>
```

## 基础组件映射

### 按钮组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-button | escort-button | - |
| type | ✓ | ✓ | primary/success/warning/danger/info/text |
| size | ✓ | ✓ | large/small/mini 默认medium |
| icon | ✓ | ✓ | 图标类名,如 vue-icon-search |
| disabled | ✓ | ✓ | 是否禁用 |
| loading | ✓ | ✓ | 是否加载中状态 |
| plain | ✓ | ✓ | 朴素按钮 |
| circle | ✓ | ✓ | 圆形按钮 |
| hotkey | - | ✓ | 快捷键支持,如 "ctrl+s" |
| hidden | - | ✓ | 是否隐藏 |

**示例:**
```html
<escort-button type="primary" size="small" @click="searchClick">查询</escort-button>
<escort-button type="success" hotkey="ctrl+s" @click="saveClick">保存</escort-button>
<escort-button :hidden="true" type="danger" @click="deleteClick">删除</escort-button>
```

### 输入框组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-input | escort-input | - |
| v-model | ✓ | ✓ | 双向绑定 |
| placeholder | ✓ | ✓ | 占位文本 |
| disabled | ✓ | ✓ | 是否禁用 |
| clearable | ✓ | ✓ | 是否可清空 |
| type | ✓ | ✓ | text/password/textarea |
| label-value | - | ✓ | 标签文本 |
| label-width | - | ✓ | 标签宽度,如 "100px" |
| :label-display | - | ✓ | 是否显示标签 |
| :style_ | - | ✓ | 自定义样式对象或字符串 |

**示例:**
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

### 下拉选择组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-select | escort-select | - |
| v-model | ✓ | ✓ | 双向绑定 |
| :options | ✓ | ✓ | 选项数组(静态数据时使用) |
| :datasource | - | ✓ | DataSource 数据源(动态数据) |
| value-member | - | ✓ | 选项值字段名,如 "key1" |
| display-member | - | ✓ | 显示字段名,如 "codeData1" |
| clearable | ✓ | ✓ | 是否可清空 |
| filterable | ✓ | ✓ | 是否可搜索 |
| multiple | ✓ | ✓ | 是否多选 |
| disabled | ✓ | ✓ | 是否禁用 |
| placeholder | ✓ | ✓ | 占位文本 |

**示例:**
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
```

### 日期时间选择器

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-datetime-picker | escort-datetime-picker | - |
| v-model | ✓ | ✓ | 双向绑定 |
| type | ✓ | ✓ | date/datetime/datetimeange/dateange |
| value-format | ✓ | ✓ | 绑定值格式,如 "yyyy-MM-dd" |
| format | ✓ | ✓ | 显示格式,如 "ymd" / "ymdt" |
| placeholder | ✓ | ✓ | 占位文本 |
| disabled | ✓ | ✓ | 是否禁用 |
| clearable | ✓ | ✓ | 是否可清空 |

**常用格式:**
- `value-format="yyyy-MM-dd"` + `format="ymd"` → 日期选择
- `value-format="yyyy-MM-dd HH:mm:ss"` + `format="ymdt"` → 日期时间选择

**示例:**
```html
<escort-datetime-picker
  v-model="form.planDate"
  prop="planDate"
  value-format="yyyy-MM-dd"
  type="date"
  :label-value="messageutil.get('计划日期')"
  label-width="100px"
  format="ymd">
</escort-datetime-picker>

<escort-datetime-picker
  v-model="form.createTime"
  value-format="yyyy-MM-dd HH:mm:ss"
  type="datetime"
  :label-value="messageutil.get('创建时间')"
  label-width="100px"
  format="ymdt">
</escort-datetime-picker>
```

### 复选框组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-checkbox | escort-checkbox | - |
| v-model | ✓ | ✓ | 双向绑定,绑定为数组 |
| :options | ✓ | ✓ | 选项数组 |
| checkbox-style | - | ✓ | 渲染样式: "checkBox"(方框) / "button"(按钮) |
| disabled | ✓ | ✓ | 是否禁用 |
| :label-display | - | ✓ | 是否显示标签 |

**示例:**
```html
<!-- 方框样式复选框 -->
<escort-checkbox
  v-model="form.selectedItems"
  :options="checkboxOpts"
  checkbox-style="checkBox">
</escort-checkbox>

<!-- 按钮样式复选框 -->
<escort-checkbox
  v-model="form.selectedTypes"
  :options="typeOpts"
  checkbox-style="button">
</escort-checkbox>
```

### 单选按钮组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-radio-button | escort-radio-button | - |
| v-model | ✓ | ✓ | 双向绑定 |
| :options | ✓ | ✓ | 选项数组 |
| radio-style | - | ✓ | 渲染样式: "radio"(圆圈) / "button"(按钮) |
| disabled | ✓ | ✓ | 是否禁用 |

**示例:**
```html
<!-- 圆圈样式单选 -->
<escort-radio-button
  v-model="form.queryType"
  :options="queryTypeOpts"
  radio-style="radio">
</escort-radio-button>

<!-- 按钮样式单选 -->
<escort-radio-button
  v-model="form.displayMode"
  :options="displayModeOpts"
  radio-style="button">
</escort-radio-button>
```

### 文本域组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-textarea | escort-textarea | - |
| v-model | ✓ | ✓ | 双向绑定 |
| :rows | ✓ | ✓ | 行数 |
| placeholder | ✓ | ✓ | 占位文本 |
| disabled | ✓ | ✓ | 是否禁用 |
| :style_ | - | ✓ | 自定义样式 |

**示例:**
```html
<escort-textarea
  v-model="form.remark"
  prop="remark"
  :rows="4"
  placeholder="请输入备注信息"
  :style_="{ width: '400px' }">
</escort-textarea>
```

### 文本组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-text | escort-text | - |
| text | - | ✓ | 显示的文本内容 |
| :style_ | - | ✓ | 自定义样式对象或字符串 |

**示例:**
```html
<escort-text text="快速选择:" :style_="{ fontSize: '15px', fontWeight: 'bold' }"></escort-text>
```

## 布局组件

### 行组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-row | escort-row | - |
| :inline | - | ✓ | 是否为行内模式 |
| :md/:sm/:xs | ✓ | ✓ | 响应式断点,{span: 12} |

**示例:**
```html
<escort-row :inline="true">
  <escort-col :md="{span:8}">
    <!-- 内容 -->
  </escort-col>
  <escort-col :md="{span:8}">
    <!-- 内容 -->
  </escort-col>
  <escort-col :md="{span:8}">
    <!-- 内容 -->
  </escort-col>
</escort-row>
```

### 列组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-col | escort-col | - |
| :inline | - | ✓ | 是否为行内模式 |
| :md/:sm/:xs | ✓ | ✓ | 响应式断点,{span: 12} |
| align | - | ✓ | 对齐方式: left/center/right |

**示例:**
```html
<escort-col :inline="true" :md="{span:6}" align="left">
  <escort-input v-model="form.itemKey"></escort-input>
</escort-col>
<escort-col :inline="true" :md="{span:4}" align="center">
  <escort-button @click="searchClick">查询</escort-button>
</escort-col>
```

## 表单组件

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-form | escort-form | - |
| :model | ✓ | ✓ | 表单数据对象 |
| ref | ✓ | ✓ | 引用标识 |
| :rules | ✓ | ✓ | 验证规则 |

**示例:**
```html
<escort-form ref="form" id="form" :model="form" :rules="rules">
  <!-- 表单内容 -->
</escort-form>
```

## 弹窗组件

### 居中弹窗

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-dialog | escort-window | - |
| v-model | ✓ | ✓ | 是否显示 |
| title | ✓ | ✓ | 弹窗标题 |
| size | ✓ | ✓ | tiny/small/medium/large/full |
| top | ✓ | ✓ | 距离顶部位置,如 "15%" |
| :close-on-click-modal | ✓ | ✓ | 点击遮罩关闭 |
| show-close | ✓ | ✓ | 是否显示关闭按钮 |

**示例:**
```html
<escort-window
  v-model="showWindow"
  size="small"
  top="15%"
  title="编辑信息"
  :close-on-click-modal="false">
  <!-- 弹窗内容 -->
</escort-window>
```

### 侧边栏弹窗

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | - | escort-aside | - |
| v-model | ✓ | - | 是否显示 |
| src | - | ✓ | 子页面路径 |
| position | - | ✓ | 位置: left/right |
| size | - | ✓ | 尺寸: tiny/small/medium/large |
| :close-on-press-escape | - | ✓ | 按 ESC 关闭 |
| :close-on-click-modal | - | ✓ | 点击遮罩关闭 |

**示例:**
```html
<escort-aside
  ref="aside"
  position="right"
  size="small"
  :close-on-press-escape="true"
  src="/views/MODULE/SUBPAGE.html">
</escort-aside>

<!-- 调用方式 -->
<script>
  this.$refs.aside.open({
    id: 'xxx',
    parent: this
  });
</script>
```

## 表格组件

XGrid 是 Escort 专用的表格组件,ViyUI 中没有对应的 vue-grid 组件。

详见 [grid-column-types.md](grid-column-types.md)

## 特殊组件

### 折叠面板

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-collapse | escort-collapse | - |
| v-model | ✓ | ✓ | 展开的值数组 |
| :show-arrow | ✓ | ✓ | 是否显示箭头 |
| :show-title | ✓ | ✓ | 是否显示标题 |

**示例:**
```html
<escort-collapse :show-arrow="false" :show-title="false">
  <template slot="title">
    <!-- 自定义标题内容 -->
  </template>
  <escort-collapse-item title="折叠项1">
    <!-- 内容 -->
  </escort-collapse-item>
</escort-collapse>
```

### 标签页

| 属性 | ViyUI | Escort | 说明 |
|------|-------|--------|------|
| 组件名 | vue-tabs | escort-tabs | - |
| v-model | ✓ | ✓ | 当前激活的标签 |

**示例:**
```html
<escort-tabs v-model="activeTab">
  <escort-tab-pane label="标签1" name="tab1">
    <!-- 内容 -->
  </escort-tab-pane>
  <escort-tab-pane label="标签2" name="tab2">
    <!-- 内容 -->
  </escort-tab-pane>
</escort-tabs>
```

## 注意事项

1. **id 和 ref**: 所有 Escort 组件都需要 `id` 和 `ref` 属性,用于组件引用
2. **prop 属性**: 表单字段需要 `prop` 属性用于验证
3. **DataSource**: 动态数据优先使用 `:datasource` 绑定 DataSource 对象
4. **样式属性**: Escort 组件使用 `:style_` 传递样式对象或字符串
