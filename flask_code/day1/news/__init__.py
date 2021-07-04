from flask import Blueprint
# 1.创建蓝图对象
news_bp = Blueprint('news_bp',__name__,url_prefix='/v1_0')
# 把视图蓝图对象的文件，在创建蓝图对象的下面导入
from . import views

