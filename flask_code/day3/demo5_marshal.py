from flask import Flask
from flask_restful import Api,Resource,marshal_with,fields,marshal
# 序列化数据:marshal工具；


app = Flask(__name__)

api = Api(app)

# 让后端返回的数据可以进行序列化
class User(object):

    def __init__(self,user_id,mobile,name):
        self.user_id = user_id
        self.mobile = mobile
        self.name = name

# 序列化容器
resource_data = {
    'user_id':fields.Integer,
    'mobile':fields.String,
    'name':fields.String
}

class HelloWorldResource(Resource):

    # envelope表示信封；
    # @marshal_with(resource_data,envelope='data')
    def get(self):
        # 对象无法直接返回
        # user = User.objects.get()
        user = User(2019,'13066668888','python42')
        # user = {
        #     'user_id':user.user_id,
        #     'mobile':user.mobile,
        #     'name':user.name
        # }
        return marshal(user,resource_data,envelope='content')

api.add_resource(HelloWorldResource,'/')

if __name__ == '__main__':
    app.run()
