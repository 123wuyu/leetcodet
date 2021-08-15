### 1.学习目标

- 明确问题/需求及其背景（即工具的应用场景）
- 理解并掌握解决问题的思想和思路
- 理解后熟练运用工具

### 2.框架的学习目标

1. 如何编写视图
2. 如何处理请求
3. 如何构造响应

### 3.Flask基本认识

#### 核心：werkzeug和Jinja2

* werkzeug是python的模块，封装了请求、响应、编码、数据认证等内容；
* Jinja2是模板引擎；
* Flask诞生2010年、简洁、轻量、扩展性强

### 4.框架的特点、异同、应用场景？

* Django：集成度高、web项目需要的基本功能，都封装在框架中，ORM、CSRF、后台管理等；
* Flask：简洁、轻量、扩展性强；
* 需求：
  * 开发周期：如果项目进度要求比较紧，技术要求Django基本自带；
  * 技术要求：如果有的技术功能实现，建议使用扩展性强的框架；
  * 技术主管人员；

* Flask1.0.2，基于python3；最新版Flask1.1.1

### 4.环境配置

* 虚拟环境：拥有独立的python解释器和对应的依赖文件的环境，独立于真实环境之外的虚拟环境；
* 基本命令：mkvirtualenv、rmvirtualenv、workon等命令不是系统自带的，是virtualenv、virwrapper，source ~/.bashrc命令的作用是让安装的虚拟环境被操作系统找到，.bashrc文件中需要添加virtualenv在磁盘中安装的位置。
  * 创建虚拟环境(基于python2)：mkvirtualenv flask_python42 
  * 创建虚拟环境(基于python3)：mkvirtualenv -p python3 flask_python42 
  * 移除虚拟环境：rmvirtualenv flask_python42
  * 进入、退出：workon、deactivate；

* 安装Flask：pip install flask默认安装最新版，pip install flask==1.0.2
  * 生成依赖文件：pip freeze > requirements.txt
  * 安装依赖文件：pip install -r requirements.txt



### 5.加载配置信息

* 三种方式：

  * 加载配置对象：一般存储业务相关的配置信息，比如数据库配置、连接信息、各种初始化的配置信息等；
    * 优点：封装性好，可复用性强
    * 缺点：不安全；
  * 加载配置文件：
    * 复用性相对不好，不是很安全；
  * 加载环境变量：一般存储敏感信息，不适合对外公开的信息，比如密钥、签名等；
    * 使用相对复杂，更安全；

  * 总结：项目中使用第一种和第三种；

  * 作业：不同的配置方式中，如果key是相同的，加载到的配置信息是哪个？

### 6.项目中程序的配置和启动方式

* 工厂：根据需求的不同，生产不同的产品；
* 工厂模式：根据参数的不同，生产不同模式下的程序实例；

~~~python
from flask import Flask
from set import DefaultConfig,ProductionConfig
# 需求：在项目中，配置信息的使用方式；
# 工厂模式：
# 1.定义工厂函数，封装创建程序实例的代码
# 2.定义函数的参数，可以根据参数的不同，生成不同的app

# 从环境变量中加载配置信息，一般是不适合对外公开的信息；
def create_flask_app():
    app = Flask(__name__)
    app.config.from_envvar('SET',silent=True)
    return app

# 从配置对象中加载配置信息，一般是和业务相关的信息，比如数据库的连接信息等；
def create_app(config_name):
    app = create_flask_app()
    app.config.from_object(config_name)
    return app
# 调用工厂函数，传入配置参数，获取程序实例对象
app = create_app(ProductionConfig)

@app.route('/')
def index():
    print(app.config.get("MYSQL_URL"))
    print(app.config.get("REDIS_URL"))
    return 'hello world'

if __name__ == '__main__':
    app.run()

~~~

### 7.路由

~~~python
在终端中：flask routes，会输出如下信息：
Endpoint  Methods  Rule
--------  -------  -----------------------
index     GET      /
static    GET      /static/<path:filename>
  
endpoint:端点，视图函数名的字符串形式；
methods：请求方法；
rule：路径规则；
static是Flask框架帮我们默认创建的静态路由，方便静态文件的访问；
~~~

* 查看路由的方式：app.url_map，存储项目中所有的路由映射；

  ~~~python
  Map(
    	[
    <Rule '/abc' (HEAD, OPTIONS, GET) -> index2019>,
    <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>
  		]
  	)
  
  python中<>存储的信息，一般表示对象；
  map:表示路由映射，容器列表；
  rule:路径规则，存储了url的路径名、http请求方法、端点(视图函数名)
  ~~~

  

### 8.蓝图

* Flask自带的模块，容器，存储了一组将来在应用程序上执行的操作；不能独立运行，可以有自己的静态文件和模板等；
  * 类似于Django中的子应用；

* 蓝图的多文件使用：容易发生循环导入的问题。
  * 除了基本的三步以外，必须把使用蓝图对象的视图文件，导入到创建蓝图对象的文件中；



