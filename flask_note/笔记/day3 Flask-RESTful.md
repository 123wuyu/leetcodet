### 1.Flask-RESTful

**Flask-RESTful是用于快速构建REST API的Flask扩展**

* 基本使用：
  * 1.安装扩展包flask-restful
  * 2.导入使用，Api用来在Flask中创建接口，以类视图的形式实现
  * 3.自定义视图类，必须继承自Resource
  * 4.定义请求方法
  * 5.添加路由



* 蓝图使用：

  ~~~python
  from flask import Flask,Blueprint
  from flask_restful import Api,Resource
  # 蓝图和restful的使用
  # 蓝图的使用步骤：1.创建蓝图对象；2.定义蓝图路由；3.注册蓝图对象
  app = Flask(__name__)
  index_bp = Blueprint('index_hello',__name__)
  
  # 把蓝图对象添加的api接口中
  api = Api(index_bp)
  
  class IndexResource(Resource):
  
      def get(self):
          return {'get': 'hello world'}
  
      def post(self):
          return {'post': 'hello world'}
  
  # 添加蓝图路由
  api.add_resource(IndexResource,'/')
  # 注册蓝图对象
  app.register_blueprint(index_bp)
  # <Rule '/' (HEAD, POST, OPTIONS, GET) -> index_bp.indexresource>
  # index_bp.indexresource；表示的是蓝图名称.视图类名称
  
  if __name__ == '__main__':
      print(app.url_map)
      app.run()
  
  ~~~

  

* 请求处理：

  * #### 使用步骤：

    1. 创建`RequestParser`对象
    2. 向`RequestParser`对象中添加需要检验或转换的参数声明
    3. 使用`parse_args()`方法启动检验处理
    4. 检验之后从检验结果中获取参数时可按照字典操作或对象属性操作

  * 校验参数的属性：

    * required：是否必须，默认为False
    * help：参数如果错误的提示信息
    * action：同名参数保存的个数，如果store保存第一个，append列表形式保存多个；

    * type：int/str；导入inputs模块，使用正则表达式，还可以使用范围函数int_range(low,high)，还可以自定义校验参数的业务函数；
    * location：表示参数的位置，form/args/headers/files/cookies等，可以不传，默认从args、如果没有从form

  

* 响应处理：
  * 序列化数据marshal工具，定义字典数据，不是重点
    * 装饰器形式marshal_with(fields，envelope='信封')
    * marshal(data,fields,envelop='')
  * 统一数据的json格式
    * 找到flask-restful源码中的output_json函数
    * 重写返回数据的方法data进行嵌套处理
    * 手动调用装饰器



