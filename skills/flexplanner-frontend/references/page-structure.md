# FlexPlanner 页面标准结构

本文档详细说明 FlexPlanner 前台页面的标准三段式结构。

## 完整页面结构

FlexPlanner 页面由三个部分组成:
1. `<style>` 样式区域
2. `<template>` 模板区域
3. `<script>` 脚本区域

## 1. Style 样式区域

```html
<style type="text/css" scoped>
  /* 自定义样式类 */
  .custom-class {
    background-color: #f0f0f0;
  }

  /* 样式示例：表格行背景色 */
  .table-row-color {
    background-color: #FFFF33;
    color: black;
  }

  /* 样式示例：按钮样式 */
  .xgrid-delete-btn {
    color: red;
    margin: 0 24px;
  }

  /* Grid 内按钮样式 */
  .grid-delete .vue-button {
    color: red;
  }

  /* 样式示例：对齐 */
  .select-text {
    margin-top: 8px;
    padding-left: 10px;
    text-align: right;
    font-size: 15px;
    font-weight: bold;
  }
</style>
```

**注意事项:**
- 使用 `scoped` 限定样式作用域
- 避免使用 Vue 关键字作为类名
- 优先使用 `escort-vue` 相关的 class 名

## 2. Template 模板区域

```html
<template>
  <!-- 页面根容器 -->
  <div v-cloak class="page" v-loading="pageLoading" :vue-loading-text="messageutil.get('page.loading.text')">
    <!-- 表单容器 -->
    <escort-form ref="form" id="form" :model="form">
      <!-- ========== 查询条件区 ========== -->
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
        </escort-col>
      </escort-row>

      <!-- ========== 数据展示区 (XGrid) ========== -->
      <escort-row id="vueRow_grid" ref="vueRow_grid">
        <escort-col :md="{span:24}">
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
              show-overflow="ellipsis">
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

            <!-- 数值列 (右对齐) -->
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

            <!-- 按钮列 (固定在右侧) -->
            <escort-xgrid-column
              fixed="right"
              align="center"
              text="操作"
              width="120px"
              render-name="button"
              :buttons="vueXgridButtons">
            </escort-xgrid-column>
          </escort-xgrid>
        </escort-col>
      </escort-row>

      <!-- ========== 弹窗区域 ========== -->
      <!-- 居中弹窗 -->
      <escort-window
        v-model="showEditWindow"
        size="small"
        top="15%"
        title="编辑信息"
        :close-on-click-modal="false"
        id="vueWindow_edit"
        ref="vueWindow_edit">
        <!-- 弹窗内容 -->
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

      <!-- 侧边栏弹窗 -->
      <escort-aside
        :close-on-press-escape="true"
        :close-on-click-modal="true"
        position="right"
        size="small"
        id="vueAside_detail"
        ref="vueAside_detail"
        src="/views/MODULE/SUBPAGE.html">
      </escort-aside>

    </escort-form>
  </div>
</template>
```

**关键说明:**
- `v-cloak`: 防止 Vue 编译前页面闪烁
- `v-loading`: 页面加载中遮罩
- `messageutil.get()`: 获取国际化文本
- `escort-form`: 必须作为根容器
- `escort-row` + `escort-col`: 布局组件
- `escort-xgrid`: 表格组件

## 3. Script 脚本区域

```javascript
<script type="text/javascript">
  var pageMixins;
  (function() {
    var pageMixinMap = {};

    // ========== 1. 事件处理方法 ==========
    pageMixinMap.event = {
      methods: {
        // 按钮点击事件
        searchBtnClick: function(event) {
          var self = this;
          // 设置查询参数
          self.vueDataSet_search.setParameter({
            itemKey: self.form.itemKey,
            itemType: self.form.itemType,
            planDate: self.form.planDate
          });
          // 调用数据源
          self.vueDataSet_search.retrieve();
        },

        // 保存按钮点击
        saveBtnClick: function(event) {
          var self = this;
          // 表单验证
          self.$refs.form.validate(function(valid) {
            if (valid) {
              // 调用保存接口
              self.vueDataSet_save.setParameter({
                items: self.$refs.vueXgrid_main.getPendingRows()
              });
              self.vueDataSet_save.retrieve(function(resp) {
                if (resp.code === 200) {
                  componentutils.showSuccessMessage({
                    message: resp.message
                  });
                  // 刷新数据
                  self.searchBtnClick();
                }
              });
            } else {
              componentutils.showErrorMessage({
                message: "请填写完整信息"
              });
            }
          });
        },

        // XGrid 按钮列配置方法
        vueXgridButtons: function(scope) {
          var self = this;
          return [{
            value: "编辑",
            size: 'small',
            type: 'text',
            click: self.editClick,
            hidden: scope.row.status === 'locked'
          }, {
            value: "删除",
            size: 'small',
            type: 'text',
            click: self.deleteClick
          }];
        },

        // 编辑按钮点击
        editClick: function(row) {
          var self = this;
          // 设置编辑数据
          self.form.editRow = row;
          self.showEditWindow = true;
        },

        // 删除按钮点击
        deleteClick: function(row) {
          var self = this;
          // 确认删除
          self.$confirm({
            title: "提示",
            message: "确定要删除这条数据吗?",
            type: "warning"
          }).then(function(action) {
            // 调用删除接口
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
        },

        // 确认编辑弹窗
        confirmEditClick: function(event) {
          var self = this;
          self.showEditWindow = false;
          componentutils.showSuccessMessage({
            message: "保存成功"
          });
        }
      }
    };

    // ========== 2. 手动混入 (父组件传参、依赖注入) ==========
    pageMixinMap.manualCommon = [{
      props: {
        // 父组件传参示例
        prodLine: String,
        itemId: String
      },
      // 依赖注入
      inject: ['parent']
    }];

    // ========== 3. 业务逻辑方法、计算属性 ==========
    pageMixinMap.manualSeperate = {
      methods: {
        // 获取状态样式
        getStatusCss: function(row) {
          var status = row.status;
          if (status === '已完成') {
            return ['buffer-rate-blue'];
          } else if (status === '待处理') {
            return ['buffer-rate-red'];
          }
          return [];
        },

        // XGrid 单元格样式回调
        vueXgridCellClassName: function(obj) {
          var row = obj.row;
          var column = obj.column;
          var field = column.field;

          // 根据状态设置行背景色
          if (field === 'status' && row.status === '待处理') {
            return 'table-row-color';
          }
          return '';
        },

        // 打开侧边栏
        openAsideDetail: function(row) {
          this.$refs.vueAside_detail.open({
            id: row.id,
            parent: this
          });
        }
      },
      computed: {
        // 计算属性示例：XGrid 数据
        gridData: function() {
          var self = this;
          var data = self.vueDataSet_search.data || [];

          // 数据转换
          return data.map(function(item) {
            return {
              id: item.id,
              itemKey: item.itemKey,
              itemName: item.itemName,
              itemType: item.itemType,
              planDate: VueUtil.formatDate(item.planDate, 'yyyy-MM-dd'),
              planQty: item.planQty,
              status: item.status
            };
          });
        },

        // 计算属性示例：选择数据的数量
        selectedCount: function() {
          return this.$refs.vueXgrid_main ? this.$refs.vueXgrid_main.getSelectRecords().length : 0;
        }
      }
    };

    // ========== 4. 数据初始化 ==========
    pageMixinMap.auto = {
      data: function() {
        return {
          // 页面加载状态
          pageLoading: false,

          // 表单数据
          form: {
            itemKey: '',
            itemType: '',
            planDate: '',
            remark: ''
          },

          // 弹窗显示状态
          showEditWindow: false,

          // 数据源定义
          vueDataSet_search: this.getDataSource({
            url: "/flexplannerApi/itemInfo/search.json",
            type: "POST",
            success: this.vueDataSetSearchSuccess
          }),

          vueDataSet_save: this.getDataSource({
            url: "/flexplannerApi/itemInfo/save.json",
            type: "POST",
            success: this.vueDataSetSaveSuccess
          }),

          vueDataSet_delete: this.getDataSource({
            url: "/flexplannerApi/itemInfo/delete.json",
            type: "POST",
            success: this.vueDataSetDeleteSuccess
          }),

          // 下拉选项数据源
          vueDataSet_itemType: this.getDataSource({
            url: "/common/getCodeList.json?codeId=ITEM_TYPE",
            type: "POST",
            success: this.vueDataSetItemTypeSuccess
          })
        };
      },

      methods: {
        // 查询数据源成功回调
        vueDataSetSearchSuccess: function(res, ds) {
          if (res && res.code === 200) {
            this.vueDataSet_search.data = res.data || [];
          } else {
            componentutils.showErrorMessage({
              message: "查询失败: " + (res.message || "未知错误")
            });
          }
        },

        // 保存成功回调
        vueDataSetSaveSuccess: function(res, ds) {
          if (res && res.code === 200) {
            componentutils.showSuccessMessage({
              message: res.message || "保存成功"
            });
            // 清空表格
            this.$refs.vueXgrid_main.clearData();
          }
        },

        // 删除成功回调
        vueDataSetDeleteSuccess: function(res, ds) {
          if (res && res.code === 200) {
            componentutils.showSuccessMessage({
              message: "删除成功"
            });
            // 刷新数据
            this.searchBtnClick();
          }
        },

        // 物料类型数据源成功回调
        vueDataSetItemTypeSuccess: function(res, ds) {
          if (res && res.data) {
            this.vueDataSet_itemType.data = res.data;
          }
        }
      },

      // 生命周期钩子
      beforeMount: function() {
        // 页面挂载前初始化
        this.dataInit();
      },

      mounted: function() {
        // 页面挂载后初始化
        // 加载下拉选项
        this.vueDataSet_itemType.retrieve();

        // 如果页面是子页面,接收父组件传参
        if (this.parent && this.parent.params) {
          this.form.itemId = this.parent.params.itemId;
          this.searchBtnClick();
        } else {
          // 默认查询
          this.searchBtnClick();
        }
      },

      methods: {
        // 数据初始化方法
        dataInit: function() {
          // 设置默认日期为今天
          this.form.planDate = VueUtil.formatDate(new Date(), 'yyyy-MM-dd');
        }
      }
    };

    // 生成混入对象
    pageMixins = getPageMixins(pageMixinMap);
  })();

  // 导出模块
  module.exports = {
    mixins: pageMixins,
    name: "MODULE_XX_YY"  // 模块功能编号
  };
</script>
```

## 页面混入说明

FlexPlanner 使用混入(Mixins)模式组织页面代码,分为四个部分:

### 1. event (事件处理)
- 按钮点击事件
- XGrid 列按钮配置方法
- 弹窗操作事件

### 2. manualCommon (手动混入 - 共通)
- `props`: 父组件传递的参数
- `inject`: 依赖注入,如 `inject: ['parent']` 获取父组件实例

### 3. manualSeperate (手动混入 - 独立)
- `methods`: 业务逻辑方法
- `computed`: 计算属性

### 4. auto (自动混入 - 数据初始化)
- `data`: 响应式数据
- `methods`: DataSource 成功回调方法
- 生命周期钩子 (`beforeMount`, `mounted`, `created` 等)

## 常见页面模式

### 查询+Grid 模式
```html
<escort-row id="vueRow_condition">
  <!-- 查询条件 -->
</escort-row>
<escort-row id="vueRow_grid">
  <!-- XGrid 表格 -->
</escort-row>
```

### 表单编辑模式
```html
<escort-row id="vueRow_form">
  <escort-col>
    <!-- 表单输入组件 -->
  </escort-col>
</escort-row>
<escort-row id="vueRow_buttons">
  <escort-col align="center">
    <!-- 操作按钮 -->
  </escort-col>
</escort-row>
```

### 弹窗子页模式
```html
<escort-window v-model="showWindow" title="xxx">
  <!-- 子页面内容 -->
</escort-window>
```

或

```html
<escort-aside src="/views/XXX/YYY.html">
</escort-aside>
```

## 注意事项

1. **必须使用 getPageMixins()** 混入对象
2. **module.exports** 必须导出 `mixins` 和 `name`
3. **DataSource 方法必须定义在 auto.methods 中**
4. **页面命名规范**: MODULE_XX_YY.html (MODULE: 模块名, XX: 功能编号, YY: 页面序号)
5. **组件 id 和 ref 必须一致**
