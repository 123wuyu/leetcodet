<template>
  <div class="dashboard-container">
    <div class="app-container">
      <!-- 靠右的按钮 -->
      <page-tools>
        <template v-slot:after>
          <el-button type="primary" size="small" @click="addPermission(1, '0')">添加权限</el-button>
        </template>
      </page-tools>
      <!-- 表格 -->
      <!-- 指定id为唯一属性的标识 -->
      <el-table border :data="list" row-key="id">
        <el-table-column label="名称" prop="name" />
        <el-table-column align="center" label="标识" prop="code" />
        <el-table-column align="center" label="描述" prop="description" />
        <el-table-column align="center" label="操作">
          <template v-slot="{ row }">
            <!-- 添加按钮只在 访问权的层级显示 当type==1 时才显示添加按钮 -->
            <el-button v-if="row.type === 1" type="text" @click="addPermission(2, row.id)">添加</el-button>
            <el-button type="text" @click="editPermission(row.id)">编辑</el-button>
            <el-button type="text" @click="delPermission(row.id)">删除</el-button>
          </template>
        </el-table-column>

      </el-table>
    </div>
    <!-- 新增编辑弹层 -->
    <el-dialog :visible="showDialog" :title="showText" @close="btnCancel">
      <!-- 表单 -->
      <el-form ref="permForm" :model="formData" :rules="rules" label-width="120px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="formData.name" style="width:90%" />
        </el-form-item>
        <el-form-item label="标识" prop="code">
          <el-input v-model="formData.code" style="width:90%" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" style="width:90%" />
        </el-form-item>
        <el-form-item label="开启">
          <!-- 当值为1时 激活 当值为0时  不激活 -->
          <el-switch
            v-model="formData.enVisible"
            active-value="1"
            inactive-value="0"
            style="width:90%"
          />
        </el-form-item>
      </el-form>
      <!-- 底部的确定和取消 -->
      <el-row slot="footer" type="flex" justify="center">
        <el-col :span="6">
          <el-button type="primary" size="small" @click="btnOK">确定</el-button>
          <el-button size="small" @click="btnCancel">取消</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import { getPermissionList, delPermission, addPermission, updatePermission, getPermissionDetail } from '@/api/permission'
import { tranListToTreeData } from '@/utils'
export default {
  data() {
    return {
      list: [],
      showDialog: false,
      formData: {
        name: '', // 名称
        code: '', // 标识
        description: '', // 描述
        type: '', // 类型 该类型 不需要显示 因为点击添加的时候已经知道类型了
        pid: '', // 因为做的是树 需要知道添加到哪个节点下了
        enVisible: '0' // 开启
      },
      rules: {
        name: [{ required: true, message: '权限名称不能为空', trigger: 'blur' }],
        code: [{ required: true, message: '权限标识不能为空', trigger: 'blur' }]
      }}
  },
  computed: {
    showText() {
      return this.formData.id ? '编辑权限' : '新增权限'
    }
  },
  created() {
    this.getPermissionList()
  },
  methods: {
    async getPermissionList() {
      // 将数据转化成了 带chilren的树形结构
      this.list = tranListToTreeData(await getPermissionList(), '0')
    },
    delPermission(id) {
      this.$confirm('确认删除该权限点吗').then(() => {
        return delPermission(id)
      }).then(() => {
        this.$message.success('删除成功')
        // 重新拉取数据
        this.getPermissionList()
      })
    },
    addPermission(type, pid) {
      // 访问权的type = 1  按钮操作的权type =2
      // pid表示当前数据的父节点的标识
      // 记录当前添加的类型和父标识
      this.formData.type = type
      this.formData.pid = pid
      this.showDialog = true
    },
    btnOK() {
      // this.$refs.permForm.validate(isOK => {})
      this.$refs.permForm.validate().then(() => {
        // 校验成功
        if (this.formData.id) {
          // 认为是编辑
          return updatePermission(this.formData)
        }
        return addPermission(this.formData) // 新增接口
      }).then(() => {
        // 添加成功
        this.$message.success('操作成功')
        this.getPermissionList()
        this.showDialog = false
      })
    },
    btnCancel() {
      // 重置数据
      this.formData = {
        name: '', // 名称
        code: '', // 标识
        description: '', // 描述
        type: '', // 类型 该类型 不需要显示 因为点击添加的时候已经知道类型了
        pid: '', // 因为做的是树 需要知道添加到哪个节点下了
        enVisible: '0' // 开启
      }
      // 移除校验
      this.$refs.permForm.resetFields() // 移除校验
      this.showDialog = false
    },
    async  editPermission(id) {
      this.formData = await getPermissionDetail(id)
      this.showDialog = true
    }
  }
}
</script>

<style>

</style>
