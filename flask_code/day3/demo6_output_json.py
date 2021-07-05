# 导入Flask类
from flask import Flask
from flask_restful import Api,Resource
# 需求：统一数据交互的格式；
# 默认情况下：{"get": "hell world"}
# 异常情况下：{
#     "message": {
#         "a": "missing a"
#     }
# }
# 目标情况下：{"message":"ok","data":{"get": "hell world"}}

app = Flask(__name__)

api = Api(app)

from flask import make_response, current_app
from flask_restful.utils import PY3
from json import dumps

# 使用装饰器的形式，实现了json数据格式的统一
# @api.representation('application/json')--->api.representation('application/json')(output_json)
# 装饰器：本质是函数嵌套，@只是python中的语法糖,表示函数调用
def output_json(data, code, headers=None):

    settings = current_app.config.get('RESTFUL_JSON', {})
    # 在返回数据之前，对data进行定制json的格式
    # {"message":"ok","data":{"get": "hell world"}}
    # 因为异常情况下，data中有message字段，所以，需要判断响应是否为异常
    if 'message' not in data:
        data = {
            'message':'666',
            'data':data
        }

    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp

# 手动调用装饰器
api.representation('application/json')(output_json)

class HelloWorldResource(Resource):

    def get(self):
        return {'get': 'hell world'}

api.add_resource(HelloWorldResource,'/')

if __name__ == '__main__':
    app.run()
