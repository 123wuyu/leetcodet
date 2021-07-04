from flask import Flask,abort

app = Flask(__name__)

@app.route('/')
def index():
    abort(400)
    return 'hello world'

# 请求钩子

# 请求前执行
@app.before_first_request
def first_request():
    print("before first request run")

@app.before_request
def before_request():
    print("before request run")

# 请求后执行
# 必须接受参数为响应对象，在出现异常情况下，after_request不执行
@app.after_request
def after_req(resp):
    print('after request run')
    return resp

# 必须接收参数为异常对象，即使出现异常，依然执行
@app.teardown_request
def teardown_req(e):
    print('teardown request run')

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)