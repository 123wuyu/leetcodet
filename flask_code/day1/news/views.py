from . import news_bp

# 2.定义视图函数和路由
@news_bp.route("/news")
def get_news():
    return 'news info'
