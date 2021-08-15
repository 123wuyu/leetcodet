### 1.Git工作流

* 项目开发的分支模型，多人协同开发，功能分支、项目发布、测试等的版本和分支控制。
* master：存储项目的发布版本；
* dev：项目的主要分支，最活跃的分支，合并代码。
* feature：功能分支，从dev分支拉取最新代码，在dev分支上新创建功能分支，git checkout -b f_register/f_goods/f_orders
* release：发布测试，测试人员对项目进行测试。
* hotfix：bug修复分支。
* git造成冲突的操作方式：
  * 一直写不提交
  * 写之前不是最新代码
  * 操作同一文件；
* git冲突的解决方式：
  * 拉取代码，手动合并，人工解决
  * 拉取代码，尝试让git自动合并，会提示冲突的信息。

### 2.项目运行方式

* 把代码上传到远程centos系统中，配置mapping路径映射/home/python/toutiao-backend
* 选择远程python解释器，文件映射，/home/python/toutiao-backend
* 选择main文件，右键运行，会有报错信息
* 编辑main的配置信息，选择新版Flask1.*推荐的运行方式，即FLASK_APP
* 配置module name:flask；scirpts：run -h 0.0.0.0
* 配置环境变量:
  * 添加FLASK_APP，toutiao.main
  * 可选，添加FLASK_ENV，development/production
* 文件夹工作路径：删除/toutiao
* 运行代码会提示错误信息，没有logs文件夹
* 在/home/python/路径下，手动创建logs文件夹。
* 运行main文件，成功。
  * 代码中提示的导包错误，可以通过配置pycharm的搜包路径解决，操作方法：在common文件夹右键标记为sources root。

### 3.项目目录说明

* ​	项目启动文件main.py

* 项目核心初始化文件，创建程序实例、各种扩展和功能的初始化

  ~~~python
  # 工厂函数中，实例化redis的主从配置信息
  app.redis_master = _sentinel.master_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
      app.redis_slave = _sentinel.slave_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
  
  # 视图中如何使用
  current_app.redis_master
  current_app.redis_slave
  current_app.redis_cluster
  
  # 请求钩子使用
  @app.before_request
  def before_request():
    print('xxx')
  
  
  ~~~

### 4.项目调试

* 判断是前端还是后端问题？
  * 前后端分离：先判断状态码，如果4开头，只看前端，如果5开头，只看后端；
  * 前后端不分离：先判断状态码，如果4开头，先看前端再看后端，如果5开头，先看后端；
  * 善于利用工具，pycharm断点和chrome浏览器的断点；
  * 如果客户端不是浏览器，使用tail命令，实时查看日志。

### 5.登录代码

* redis的key定义：之前使用sms_code_mobile，推荐使用sms:code:mobile
* 验证码的校验：
  * 短信验证码：先删除、再比较。好处：只能比较一次，本质是只能对redis数据库get一次。**可以先比较，再删除。**
  * 图片验证码：**只能是先删除、再比较。**图片验证码只能比较一次。
  * 图片验证码校验是不是人？
  * 短信验证码校验人是不是你？

### 6.生成token

* 先拉取最新代码
* 在dev分支上，新建功能分支，f_jwt_zhangsan
* 实现功能代码
* 推送到自己的功能分支上



















