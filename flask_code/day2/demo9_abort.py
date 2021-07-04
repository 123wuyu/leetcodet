from flask import Flask,abort
# Flask中的异常处理
app = Flask(__name__)

@app.route('/')
def index():
    # abort本质类似于python中的raise语句，只能抛出符合http协议的异常状态码；
    # try:
    #     ***
    # except Exception:
    #     abort()
    abort(500)
    return 'hello world'

# 捕获abort函数抛出的异常信息，自定义异常页面
@app.errorhandler(500)
def err_handler(e):
    return '服务器发生异常，请重新涮新页面或访问某某页面'


if __name__ == '__main__':
    app.run(debug=True)