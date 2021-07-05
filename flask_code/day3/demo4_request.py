from flask import Flask
# 1---导入reqparser
from flask_restful import Api,Resource,reqparse,inputs
# 处理请求：
app = Flask(__name__)

api = Api(app)

# 需求：校验手机号格式；
def parse_mobile(mobile):
    if mobile is not None:
        import re
        if re.match(r'1[3-9]\d{9}$',mobile):
            return mobile
    else:
        return ValueError('{} is not valid'.format(mobile))
    pass

class HelloWorldResource(Resource):

    def get(self):
        # 2----在对应的请求方法中实例化reqparse中的工具类
        req = reqparse.RequestParser()
        # 3----添加需要检查和校验参数信息
        # required:表示参数是否必须要传，默认为False，如果True，不传会报错
        # action:表示多个同名参数保存哪一个，store为默认保存第一个
        # req.add_argument('a',required=True,help='missing a',action='store')
        # 如果append,保存多个[]
        # req.add_argument('a',required=True,help='missing a',action='append')
        # type:
        # 可以指定参数的类型
        # req.add_argument('a',type=str,required=True,help='missing a')
        # 使用inputs模块中的函数对参数进行校验
        # req.add_argument('a',type=inputs.int_range(1,100),required=True,help='missing a')
        # req.add_argument('a',type=inputs.regex(r'正则表达式'),required=True,help='missing a')
        # req.add_argument('a',type=parse_mobile,required=True,help='missing a')
        req.add_argument('a',required=True,help='missing a')
        # 4----parse_args解析参数
        args = req.parse_args()
        print(args)
        return {'get': 'get hell world'}

    def post(self):
        req = reqparse.RequestParser()
        # req.add_argument('a', required=True, help='missing a')
        req.add_argument('a', required=True, help='missing a',location='form')
        args = req.parse_args()
        print(args)
        return {'post': 'post hell world'}

api.add_resource(HelloWorldResource,'/')

if __name__ == '__main__':
    app.run()
