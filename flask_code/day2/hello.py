from flask import Flask

app = Flask(__name__)

# 作业：不使用装饰器实现路由映射
# @app.route('/')
def index():
    return 'hello world'
# 源码：
# self.add_url_rule(rule, endpoint, f, **options)
app.add_url_rule('/','index',index)


if __name__ == '__main__':
    print(app.url_map)
    app.run()