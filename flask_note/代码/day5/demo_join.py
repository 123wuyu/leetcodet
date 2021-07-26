from flask import Flask
from datetime import datetime
# - 1.导入扩展包flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# - 2.配置数据库的连接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/toutiao'
# 关闭动态追踪修改的警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 展示sql语句
app.config['SQLALCHEMY_ECHO'] = True

# - 3.实例化sqlalchemy对象，并且和程序实例关联
db = SQLAlchemy(app)



# 三张表：
# User存的是用户常用的基本信息，UserProfile存的用户不常用信息
# Relation表：User表和Relation表示一对多的关系

# 连接查询：
# Foreignkey一对多：一方定义关系，多方定义外键
class User(db.Model):
    """
    用户基本信息
    """
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean, default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer, default=0, doc='发帖数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = db.Column(db.Integer, default=0, doc='累计点赞人数')
    read_count = db.Column(db.Integer, default=0, doc='累计阅读人数')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用')

    # 定义关系,relationship函数，第一个参数表示另外一方的类名
    # 反向引用：fackref:给另外一方查询到当前模型类中的字段使用
    # follows = db.relationship('Relation',backref='u',uselist=False)
    # follows = db.relationship('Relation')

    # 定义连接条件primaryjoin
    follows = db.relationship('Relation',primaryjoin='User.id==foreign(Relation.user_id)')


class UserProfile(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    gender = db.Column(db.Integer, default=0, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')

    area = db.Column(db.String, doc='地区')
    company = db.Column(db.String, doc='公司')
    career = db.Column(db.String, doc='职业')

class Relation(db.Model):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2
    # ForeignKey函数，不对应数据库中的外键这个概念；
    # 只是用来标识当前字段在查询数据时，指向另外一张表的主键id
    # id = db.Column('relation_id', db.Integer,db.ForeignKey('user_basic.user_id') ,primary_key=True, doc='主键ID')
    id = db.Column('relation_id', db.Integer,primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer,doc='用户ID')
    target_user_id = db.Column(db.Integer, doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


if __name__ == '__main__':
    app.run()