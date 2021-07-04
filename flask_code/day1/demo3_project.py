from flask import Flask
from set import DefaultConfig,ProductionConfig
# 需求：在项目中，配置信息的使用方式；
# 工厂模式：
# 1.定义工厂函数，封装创建程序实例的代码
# 2.定义函数的参数，可以根据参数的不同，生成不同的app

def create_flask_app():
    app = Flask(__name__)
    app.config.from_envvar('SET',silent=True)
    return app


def create_app(config_name):
    app = create_flask_app()
    app.config.from_object(config_name)
    return app

app = create_app(ProductionConfig)

@app.route('/')
def index():
    print(app.config.get("MYSQL_URL"))
    print(app.config.get("REDIS_URL"))
    return 'hello world'

if __name__ == '__main__':
    app.run()