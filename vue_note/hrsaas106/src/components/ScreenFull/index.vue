<template>
  <!-- 因为要布局 所以变成块元素 -->
  <div>
    <svg-icon
      icon-class="fullscreen"
      style="color:#fff; width: 20px; height: 20px"
      @click="changeScreen"
    />
  </div>
</template>

<script>
import ScreenFull from 'screenfull'
export default {
  methods: {
    changeScreen() {
    //   document.documentElement.requestFullscreen() 原生方式
      if (!ScreenFull.isEnabled) {
        this.$message.warning('当前全屏功能不可用')
        return
      }
      //   直接全屏
      ScreenFull.toggle() // 全屏方法  既可以全屏 也可以退出全屏
    }
  }
}
</script>

<style>

</style>
