from flask import Flask,g,abort
# 用户认证的案例：利用g对象存储用户信息，校验用户身份


app = Flask(__name__)

# 在每次请求前，校验用户是否登录
@app.before_request
def authentication():
    # 查询数据库，确认用户是否注册，如果已注册，返回用户id，否则该用户不存在
    g.user_id = 2019
    # g.user_id = None

# 手动实现登录验证装饰器
def login_required(func):
    def wrapper(*args,**kwargs):
        if g.user_id is not None:
            return func(*args,**kwargs)
        else:
            abort(401)
    return wrapper

# 首页，不登录可以访问
@app.route('/')
def index():
    return 'index page {}'.format(g.user_id)

# 个人信息页，不登录无法访问
@app.route('/profile')
@login_required
def user_profile():
    return 'profile page {}'.format(g.user_id)

if __name__ == '__main__':
    app.run()