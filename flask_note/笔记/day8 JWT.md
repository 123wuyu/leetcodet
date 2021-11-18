### 1.每天代码的实现流程：

* 确认当前在dev分支，本地的dev
* 拉取最新代码：git pull
* 新建并切换到新的功能分支，git checkout -b f_jwt
* 当前就在f_jwt分支实现功能代码
* 代码实现完成，git add/commit/push

### 2.登录验证

* 需求：项目中很多接口，都需要用户身份user_id，用户登录后才能访问。
* 实现方式：登录验证装饰器。

### 3.token刷新

* 代码实现：
  * utils/decoraters.py 实现了登录验证装饰器
  * utils/middlewares.py 实现中间件，在每次请求前校验用户权限，提取用户id
  * toutiao/resourses/user/passport.py 在登录代码中，补充生成token和涮新token的代码。

### 4.JWT禁用

* 用户修改密码，需要颁发新的token，禁用还在有效期内的老token
* 后台封禁用户

### 5.对象存储

* 在头条项目中，如用户头像、文章图片等数据需要使用文件存储系统来保存

  * 自己搭建文件系统服务
  * 选用第三方对象存储服务

  * 对于项目来说，一般网站，流量的80%左右都集中在图片上，对于项目的优化，必须要考虑图片文件存储，数据去重问题，CDN内容分发网络；

* 七牛云使用：
  * 安装使用：pip install qiniu
  * 单脚本文件测试：上下文问题，token过期问题。

* 需求：实现用户头像上传。

  * 接口设计

  ~~~python
  接口名称：上传头像。
  接口地址：/v1_0/user/photo
  请求方法：get/post/put/delete
  post表示create/insert
  put表示update,put要求修改一个资源，要传所有参数；
  {
    'user_id':xx,
    'user_name':xx,
    'mobile':xx,
    'photo':xx,
    ...
  }
  patch表示update，patch修改一个资源，只传相关参数；
  {
    'photo':xx,
    ...
  }
  
  请求参数：
  参数名			参数类型			是否必须			参数说明
  photo				files				 是				用户上传的头像图片文件
  
  返回结果：
  正常情况下：
  {'message':'ok','data':{'photo_url':'七牛云的空间域名+图片名称'}}
  异常情况下：
  {'message':'token error'},400
  
  ~~~

  

* 异常处理：IO操作、网络io、磁盘io。
  * 1.类型转换
  * 2.查询数据库，内存型；
  * 3.调用第三方接口。





















