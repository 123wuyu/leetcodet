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
# 注册蓝图
# <Rule '/' (HEAD, POST, OPTIONS, GET) -> index_bp.indexresource>
# index_bp.indexresource；表示的是蓝图名称.视图类名称
app.register_blueprint(index_bp)

if __name__ == '__main__':
    print(app.url_map)
    app.run()