from flask import Flask
# 导入转换器模块
from werkzeug.routing import BaseConverter
# 需求：处理请求信息：
# 提取url地址中的固定参数
# http://127.0.0.1:5000/2019
# 查询字符串：url地址栏中，问号后面、等号传值、与号分隔；
# http://127.0.0.1:5000/users/?mobile=13912345678

app = Flask(__name__)

# 语法：<>,里面是形参名称，必须传给视图函数
# 原理：转换器；类似于Django中的正则表达式
# 只接受整型值,int
@app.route('/<int:temp>')
def index(temp):
    return 'hello world %s' % temp

# 自定义转换器,用来匹配手机号
# - 1.定义转换器类，继承自baseconverter
# - 2.把自定义的转换器类，添加到转换器字典容器中
# - 3.在装饰器中使用转换器
class RegexMobileConverter(BaseConverter):
    # 如果是自己手动实现正则表达式，需要加上要加上$
    regex = r'1[3-9]\d{9}'

app.url_map.converters['mobile'] = RegexMobileConverter

@app.route('/users/<mobile:temp>')
def regex_mobile(temp):
    return 'hello world %s' % temp



if __name__ == '__main__':
    print(app.url_map)
    app.run()