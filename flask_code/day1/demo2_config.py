from flask import Flask
# 配置文件加载：字典形式存储配置信息
# 三种形式：
# 1、从配置对象中加载
# 2、从配置文件中加载
# 3、从环境变量中加载
# class DefaultConfig(object):
#     MYSQL_URL = 'mysql address'
#     REDIS_URL = 'redis address'

app = Flask(__name__)
# 获取配置对象的配置信息
from set import DefaultConfig,ProductionConfig
app.config.from_object(DefaultConfig)
# 获取配置文件的配置信息,可以加载不是py格式的文件；
# ini初始化文件，里面保存的是配置信息
# app.config.from_pyfile('settings.ini')
# 从环境变量中加载
# silent表示沉默，是否记载到环境变量的配置信息
# 如果True表示沉默，加载不到不报错
# 如果False表示不沉默，加载不到报错
app.config.from_envvar('SET',silent=True)

@app.route('/')
def index():
    # config是Flask中自带的配置对象，保存了程序的配置信息
    # print(app.config.get('MYSQL_URL'))
    # 获取配置信息
    # print(app.config.get('SECRET_KEY'))
    # 从环境变量文件中获取配置信息
    print(app.config.get("SECRET_KEY"))
    return 'hello world'

if __name__ == '__main__':
    app.run()