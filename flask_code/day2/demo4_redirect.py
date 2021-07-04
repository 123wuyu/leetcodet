from flask import Flask,redirect

app = Flask(__name__)

@app.route('/')
def index():
    # redirect表示重定向，参数为location
    # 应用场景：当项目的文件或url地址出现变化的时候；
    return redirect('http://www.baidu.com')

if __name__ == '__main__':
    app.run()