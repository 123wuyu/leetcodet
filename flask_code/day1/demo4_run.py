from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world2018'

# run函数可以传入参数
# debug等于True表示可以自动跟踪代码的变化，定位错误信息；
# host/port
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5001)