from flask import Flask
from flask_restful import Api,Resource
app = Flask(__name__)
api = Api(app)
# 添加装饰器：
# 装饰器1
def decorator1(fun):
    def wrapper(*args,**kwargs):
        print('decorator1 run')
        return fun(*args,**kwargs)
    return wrapper

# 装饰器2
def decorator2(fun):
    def wrapper(*args,**kwargs):
        print('decorator2 run')
        return fun(*args,**kwargs)
    return wrapper

class IndexResource(Resource):
    # 装饰器添加容器默认是列表，
    # method_decorators = [decorator1,decorator2]
    # 需求：get请求触发decorator1，post请求触发decorator2
    method_decorators = {
        'get':[decorator1],
        'post':[decorator2,decorator1]
    }
    def get(self):
        return {'get': 'hello world'}

    def post(self):
        return {'post': 'hello world'}

api.add_resource(IndexResource,'/')

if __name__ == '__main__':
    print(app.url_map)
    app.run()