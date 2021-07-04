class DefaultConfig(object):
    MYSQL_URL = 'mysql address'
    REDIS_URL = 'redis address'

# 定义其它模式下的配置信息，生产模式、开发模式
class ProductionConfig(DefaultConfig):
    MYSQL_URL = 'production mysql address'
    REDIS_URL = 'production redis address'

