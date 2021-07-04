from flask import Flask

# 实现Flask基本程序
# 步骤：
# 1、导入Flask类
# 2、创建Flask类的实例对象
# 3、定义路由和视图函数
# 4、启动服务器

# 创建Flask类的实例对象
# 参数：必须是字符串，__name__的作用确定程序启动文件所在的位置；
# 实例路径会影响静态文件的访问；
# http://127.0.0.1:5000/static/hello.html

# static_url_path:表示的url中的静态路径
# static_path:表示的静态文件夹的名称

# abc不行、ab行、abcd行；
# 结论：如果传入的参数为标准模块名，会影响静态文件的访问，不会影响视图函数的访问；
app = Flask(__name__)

# 定义路由和视图函数
@app.route("/")
def hello():
    return 'hello world'

# 程序入口
# 当前文件独立运行时，该表达式成立
# 当前文件被导入到其它文件中调用，该表达式不成立，__name__ == demo1_hello
if __name__ == '__main__':
    app.run()

