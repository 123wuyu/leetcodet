from flask import Flask,Blueprint
# 蓝图的使用步骤：
# 1、创建蓝图对象
# 2、定义蓝图路由
# 3、注册蓝图对象
from news import news_bp
app = Flask(__name__)
# 3.注册news_bp蓝图对象
app.register_blueprint(news_bp)

# 创建蓝图对象,第一个参数表示蓝图的名称，第二个参数表示蓝图所在的位置
# bp = Blueprint('bp',__name__)
# 定义蓝图路由
# @bp.route("/users")
# def get_users():
#     return 'user info'

@app.route('/')
def index():
    return 'hello world'
# 注册蓝图对象
# app.register_blueprint(bp)
if __name__ == '__main__':
    print(app.url_map)
    app.run()