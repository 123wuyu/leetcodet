from flask import Flask,render_template
# 返回模板
app = Flask(__name__)

@app.route('/')
def index():
    # 直接返回响应字符串，返回给浏览器。
    # return 'hello world'
    return render_template('index.html')


if __name__ == '__main__':
    app.run()