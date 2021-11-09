<template>
  <el-card class="page-tools">
    <el-row type="flex" justify="space-between" align="middle">
      <el-col>
        <!-- 前插槽 -->
        <!--有名字的叫具名插槽 没名字的叫匿名插槽 -->
        <div v-if="showBefore" class="before">
          <!-- 图标 随着 showBefore显示而显示 -->
          <i class="el-icon-info" />
          <slot name="before" />
        </div>
      </el-col>
      <el-col>
        <el-row type="flex" justify="end">
          <!-- 后插槽 -->
          <slot name="after" />
        </el-row>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
// 组件可以显示 左侧内容 也可以显示右侧内容  如果左侧内容不传 图标应该不显示
export default {
  props: {
    showBefore: {
      default: false,
      type: Boolean
    }
  }
}
</script>

<style lang='scss'>
 .page-tools {
    margin: 10px 0;
    .before {
      line-height: 34px;
    i {
      margin-right: 5px;
      color: #409eff;
    }
    display: inline-block;
    padding: 0px 10px;
    border-radius: 3px;
    border: 1px solid rgba(145, 213, 255, 1);
    background: rgba(230, 247, 255, 1);
  }
 }
</style>
