<template>
  <div>
    <!-- 给action一个#号 就不会报错了 -->
    <!-- file-list是上传的文件列表 可以绑定到上传组件上，让上传组件来显示 -->
    <!-- upload组件显示的是file-list -->
    <el-upload
      list-type="picture-card"
      :limit="1"
      action="#"
      :on-preview="preview"
      :on-remove="handleRemove"
      :on-change="changeFile"
      :before-upload="beforeUpload"
      :http-request="upload"
      :file-list="fileList"
      :class="{ disabled : fileComputed }"
    >
      <i class="el-icon-plus" />
    </el-upload>
    <el-progress v-if="showPercent" :percentage="percent" style="width: 180px" />
    <el-dialog :visible.sync="showDialog" title="图片预览">
      <img :src="imgUrl" alt="" style="width:100%">
    </el-dialog>
  </div>

</template>

<script>
import COS from 'cos-js-sdk-v5' // 引入腾讯云cos包
// 实例化COS对象
const cos = new COS({
  // 同学们拷贝自己的秘钥和key 只有用自己的key和自己的秘钥才能上传到自己的存储桶里面
  SecretId: 'AKID0mqfEWqlUzIbeSkGRL6c7ML6c0B93To9', // 身份识别 ID
  SecretKey: 'JFwNZdeRF2iOp03FFsGNDm44vWFitmNF' // 身份密钥
})
export default {
  data() {
    return {
      fileList: [],
      showDialog: false,
      imgUrl: '',
      currentFileUid: null, // 记录当前正在上传的uid
      percent: 0, // 当前的百分比
      showPercent: false
    }
  },
  computed: {
    // 如果它为true 表示就不应该显示 +号上传了
    fileComputed() {
      return this.fileList.length === 1
    }
  },
  methods: {
    //   点击预览事件
    preview(file) {
      console.log(file.url)
      this.imgUrl = file.url
      this.showDialog = true
    },
    // file是要删除的文件
    // fileList是删过之后的文件
    handleRemove(file, fileList) {
    //   console.log(file)
    //   console.log(fileList)
    //   console.log(this.fileList)
      this.fileList = this.fileList.filter(item => item.uid !== file.uid) // 将当前的删除文件排除在外
    //   this.fileList = fileList
    },
    // 不能用push 这个钩子会执行多次
    changeFile(file, fileList) {
      // file是当前的文件 fileList是当前的最新数组 this.fileList
    //   console.log(file)
      // 如果当前fileList中没有该文件的话 就往里进行追加
      this.fileList = fileList.map(item => item)
      // 这里为何暂时不成功呢  ？ 因为现在还没有上传 所有第二次进来的数据 一定是个空的
    // 如果完成上传动作了 第一次进入 和第二次进去的fileList的长度应该都是1 应该都有数据
    // 上传成功 =》 数据才能进来 =》腾讯云cos
    },
    beforeUpload(file) {
      //   先检查文件类型
      const types = ['image/jpeg', 'image/gif', 'image/bmp', 'image/png']
      if (!types.some(item => item === file.type)) {
        //   如果不存在
        this.$message.error('上传图片只能是 JPG、GIF、BMP、PNG 格式!')
        return false // 上传终止
      }
      // 检查文件大小  5M 1M = 1024KB 1KB = 1024B
      const maxSize = 10 * 1024 * 1024
      if (file.size > maxSize) {
        //   超过了限制的文件大小
        this.$message.error('上传的图片大小不能大于5M')
        return false
      }
      //   已经确定当前上传的就是当前的这个file了
      this.currentFileUid = file.uid
      this.showPercent = true
      return true // 最后一定要return  true
    },
    // 进行上传操作
    upload(params) {
    //   console.log(params.file)
      if (params.file) {
        // 执行上传操作
        cos.putObject({
          Bucket: 'shuiruohanyu-106-1302806742', // 存储桶
          Region: 'ap-beijing', // 地域
          Key: params.file.name, // 文件名
          Body: params.file, // 要上传的文件对象
          StorageClass: 'STANDARD', // 上传的模式类型 直接默认 标准模式即可
          onProgress: (params) => {
            // console.log(params)
            this.percent = params.percent * 100
          }
          // 上传到腾讯云 =》 哪个存储桶 哪个地域的存储桶 文件  格式  名称 回调
        }, (err, data) => {
          // data返回数据之后 应该如何处理
        //   console.log(err || data)
          // data中有一个statusCode === 200 的时候说明上传成功
          if (!err && data.statusCode === 200) {
            //   此时说明文件上传成功  要获取成功的返回地址
            // fileList才能显示到上传组件上 此时我们要将fileList中的数据的url地址变成 现在上传成功的地址
            // 目前虽然是一张图片 但是请注意 我们的fileList是一个数组
            // 需要知道当前上传成功的是哪一张图片
            this.fileList = this.fileList.map(item => {
              // 去找谁的uid等于刚刚记录下来的id
              if (item.uid === this.currentFileUid) {
                // 将成功的地址赋值给原来的url属性
                return { url: 'http://' + data.Location, upload: true }
                // upload 为true 表示这张图片已经上传完毕 这个属性要为我们后期应用的时候做标记
                // 保存  => 图片有大有小 => 上传速度有快又慢 =>要根据有没有upload这个标记来决定是否去保存
              }
              return item
            })
            // 关闭进度条
            // 重置百分比
            setTimeout(() => {
              this.showPercent = false
              this.percent = 0
            }, 1000)
            // 将上传成功的地址 回写到了fileList中 fileList变化  =》 upload组件 就会根据fileList的变化而去渲染视图
          }
        })
      }
    }
  }
}
</script>

<style>
 .disabled .el-upload--picture-card {
     display: none
 }
</style>
