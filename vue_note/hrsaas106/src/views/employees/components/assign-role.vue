<template>
  <el-dialog title="分配角色" :visible="showRoleDialog" @close="btnCancel">
    <!-- 多选框组  v-model双向绑定-->
    <el-checkbox-group v-model="roleIds">
      <!-- 要循环的选项 -->
      <!-- 要显示 角色名称 存储 角色id  label表示要存储的值-->
      <el-checkbox v-for="item in list" :key="item.id" :label="item.id">
        {{ item.name }}
      </el-checkbox>
    </el-checkbox-group>
    <!-- 定义footer的插槽 -->
    <el-row slot="footer" type="flex" justify="center">
      <el-col :span="6">
        <el-button type="primary" size="small" @click="btnOK">确定</el-button>
        <el-button size="small" @click="btnCancel">取消</el-button>
      </el-col>
    </el-row>
  </el-dialog>
</template>

<script>
import { getRoleList } from '@/api/setting'
import { getUserDetailById } from '@/api/user'
import { assignRoles } from '@/api/employees'
export default {
  props: {
    showRoleDialog: {
      type: Boolean,
      default: false
    },
    userId: {
      // 用户的id  当前要处理的哪个用户
      type: String,
      default: null
    //   required: true // 要求必须传该id
    }
  },
  data() {
    return {
      list: [], // 负责存储当前所有的角色id
      roleIds: [] // 这个数组负责存储 当前用户所拥有的角色id
    }
  },
  created() {
    // 获取所有的角色
    this.getRoleList()
  },
  methods: {
    async getRoleList() {
      const { rows } = await getRoleList({ page: 1, pagesize: 20 }) // 默认只取10条数据  角色数量 不会太多
      // rows是要循环的记录
      this.list = rows
    },
    // 这个方法是什么时候调用？props传值是异步的 所以这里不能用this.userId
    // 这个方法是给父组件调用的
    async getUserDetailById(id) {
      const { roleIds } = await getUserDetailById(id) // 将用户所拥有的角色赋值给当前用户的对象
      this.roleIds = roleIds
    },
    async btnOK() {
      await assignRoles({ id: this.userId, roleIds: this.roleIds }) // 保存用户的角色
      // 关闭弹层
      this.$emit('update:showRoleDialog', false)
    //   this.$parent.showRoleDialog = false
    },
    btnCancel() {
      // 取消
      this.roleIds = [] // 重置数组 将它还原成一个空
      this.$emit('update:showRoleDialog', false)
    }
  }
}
</script>

<style>

</style>
