
# 使用flask-restful实现基本程序：类视图的形式
from flask import Flask
# 1----导入flask-restful工具类
from flask_restful import Api,Resource

app = Flask(__name__)
# 2----实例化api对象
api = Api(app)

# @app.route('/')
# def index():
#     return 'hello world'

# 3----定义视图类，必须继承自Resource
class IndexResource(Resource):
    # 定义的http请求方法
    def get(self):
        # 返回响应字符串，默认转成json
        # return 'hello world'
        return {'hello': 'world'}

# 4----添加路由，端点indexresource
# api.add_resource(IndexResource,'/')
# 给视图起名字，endpoint表示视图函数名
api.add_resource(IndexResource,'/',endpoint='index')

if __name__ == '__main__':
    print(app.url_map)
    app.run()

