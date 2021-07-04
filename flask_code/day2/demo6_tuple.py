from flask import Flask
# 返回元组信息
app = Flask(__name__)

@app.route('/')
def index():
    # 可以返回自定义的状态码
    # return 'hello world',666,{'Server':'itcast_python42'}
    return ('hello world',200,{'Server':'itcast_python42'})

if __name__ == '__main__':
    app.run()