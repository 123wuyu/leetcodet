<template>
  <!-- 工作日历 -->
  <div>
    <!-- 年和月 -->
    <el-row type="flex" justify="end">
      <!-- 年 用组件给定一个日期，日期获取年，年取前五年 + 后五年 -->
      <el-select v-model="currentYear" size="small" style="width: 120px" @change="dataChange">
        <el-option v-for="item in yearList" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="currentMonth" size="small" style="width: 120px;margin-left: 10px" @change="dataChange">
        <!-- 循环 -->
        <el-option v-for="item in 12" :key="item" :label="item" :value="item" />
      </el-select>
    </el-row>
    <!-- 放置一个日历组件 -->
    <el-calendar v-model="currentDate">
      <template slot="dateCell" slot-scope="{ date, data }">
        <!-- date是当前单元格的日期 data是对象 对象里有要显示的day -->
        <!-- <template v-slot:dateCell="{ date, data }"> -->
        <div class="date-content">
          <span class="text"> {{ data.day | getDay }}</span>
          <span v-if="isWeek(date)" class="rest">休</span>
        </div>
      </template>
    </el-calendar>
  </div>
</template>

<script>
export default {
  filters: {
    getDay(value) {
      const day = value.split('-')[2]
      return day.startsWith('0') ? day.substr(1) : day
    }
  },
  props: {
    startDate: {
      type: Date,
      // 回调函数式的返回值
      default: () => new Date() // 如果没有传递startDate 就取当前时间
    }
  },
  data() {
    return {
      yearList: [], // 要遍历的年的数组
      currentYear: null, // 当前年份
      currentMonth: null, // 当前月份
      currentDate: null // 当前时间
    }
  },
  created() {
    // 获取当前的年份
    this.currentYear = this.startDate.getFullYear() // 得到当前的年份
    this.currentMonth = this.startDate.getMonth() + 1 // 当前月份
    // 快速生成数组的方法
    this.yearList = Array.from(Array(11), (v, i) => this.currentYear + i - 5)
    // 钩子函数执行完成之后
    this.dataChange() // 主动调用一下方法
  },
  methods: {
    dataChange() {
    // 生成新的日期
      this.currentDate = new Date(`${this.currentYear}-${this.currentMonth}-1`) // 以1号为开始
    },
    // 判断当前是否是周末
    isWeek(date) {
      return date.getDay() === 6 || date.getDay() === 0
    }
  }
}
</script>
<style  scoped>
 /deep/ .el-calendar-day {
  height:  auto;
 }
 /deep/ .el-calendar-table__row td,/deep/ .el-calendar-table tr td:first-child,  /deep/ .el-calendar-table__row td.prev{
  border:none;
 }
.date-content {
  height: 40px;
  text-align: center;
  line-height: 40px;
  font-size: 14px;
}
.date-content .rest {
  color: #fff;
  border-radius: 50%;
  background: rgb(250, 124, 77);
  width: 20px;
  height: 20px;
  line-height: 20px;
  display: inline-block;
  font-size: 12px;
  margin-left: 10px;
}
.date-content .text{
  width: 20px;
  height: 20px;
  line-height: 20px;
 display: inline-block;

}
 /deep/ .el-calendar-table td.is-selected .text{
   background: #409eff;
   color: #fff;
   border-radius: 50%;
 }
 /deep/ .el-calendar__header {
   display: none
 }
</style>
