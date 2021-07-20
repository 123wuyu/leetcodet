### 1.ORM

*  object-relation-mapping：对象关系映射；
  * 类<====>表
  * 属性<===>字段
  * 对象<===>行、记录、数据

* 特点：
  * 缺点：执行效率相对较低；
  * 优点：开发效率较高；一次编写可以适配多个数据库；
    * **在数据库表名或字段名发生变化时，只需修改模型类的映射，无需修改数据库操作的代码**

* ORM用法：
  * Django：先有模型类，实现数据库迁移，创建表；
  * Flask：先有表，再创建模型类，实现和表的映射；
    * 先创建模型类，再迁移到数据库中
      - 优点：简单快捷，定义一次模型类即可，不用写sql
      - 缺点：不能尽善尽美的控制创建表的所有细节问题，表结构发生变化的时候，也会难免发生迁移错误
    * 先用原生SQL创建数据库表，再编写模型类作映射
      - 优点：可以很好的控制数据库表结构的任何细节，避免发生迁移错误
      - 缺点：可能编写工作多（编写sql与模型类，似乎有些牵强）

* SQLAlchemy

  * python中的一个数据库ORM框架；

  * Flask-SQLAlchemy是对SQLAlchemy的进一步封装，主要是兼容Flask框架。

    * 需要安装使用pip install flask-sqlalchemy会默认安装SQLAlchemy

    

* 数据库连接：

  * Django：settings.py—host/port/user/password/db

  * Flask: 类似于url地址的形式；SQLALCHEMY_DATABASE_URI

  * 两种方式：

    ~~~python
    # 第一种：
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/db'
    # 简写方式：
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost/db'
    # 第二种：
    # 定义配置对象
    class Config:
      SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost/db'
    app.config.from_object(Config)
    
    ~~~

  * 其它基本配置信息：
    * SQLALCHEMY_TRACK_MODIFICATIONS：表示动态追踪修改，可以不配置，但是，会提示警告信息，可以设置为True或False，如果为True，会跟踪数据库的变化，会对计算机性能产生一定的影响，消耗内存，一般情况下，设置False；
    * SQLALCHEMY_ECHO：如果为True，会在代码执行过程中，把代码中执行的ORM语句转成sql语句在终端输出。

  * 了解：SQLALCHEMY_POOL_SIZE：连接池的大小，默认值5；

### 2.模型类创建

* 基本步骤：

  * 1.导入扩展包flask_sqlalchemy

  * 2.配置数据库的连接信息

  * 3.实例化sqlalchemy对象，并且和程序实例关联

    ~~~python
    # 两种方式：
    # 第一种：直接实例化，传入app
    db = SQLAlchemy(app)
    # 第二种：工厂函数
    db = SQLAlchemy()
    def create_app():
      app = Flask(__name__)
    	# 通过手动调用初始话app的函数
      db.init_app(app)
      return app
      
    app.run()
    ~~~

    

  * 4.定义模型类，必须继承自db.Model

###  3.模型类基本操作

* 增加数据，需要通过模型类的数据库会话对象，db.session，封装了对数据库的基本操作，比如提交数据、回滚、添加、删除等。

  ~~~python
  from db_query import User,db
  # 添加一个数据
  user = User(mobile='13066669999',name='python42')
  # 把创建的模型类对象，添加给数据库会话对象
  db.session.add(user)
  # 提交数据到数据库中
  db.session.commit()
  
  # 添加多个数据
  user1 = User(mobile='13166669999',name='python43')
  user2 = User(mobile='13266669999',name='python44')
  # 把创建的模型类对象，添加给数据库会话对象
  db.session.add_all([user1,user2])
  # 提交数据到数据库中
  db.session.commit()
  
  ~~~

* 基本查询语句

  * all方法：查询所有数据，列表形式返回

  ~~~python
  sql:
    select * from 表名;
  orm:
    User.query.all()
  
  ~~~

  * first方法：查询第一个数据

  ~~~python
  sql:分页limit
    select * from user_basic limit 1;
  orm:
    User.query.first()
  
  ~~~

  * get方法：参数为主键id，如果不传会报错
    * Django：如果数据不存在，DoesNotExists；
    * Flask：如果数据不存在，不会报错，返回结果None；

  ~~~python
  sql:
    select * from user_basic where user_basic.user_id=1;
  orm:
    User.query.get(1)
    
  ~~~

* 过滤查询：filter和filter_by

  * filter_by函数：：查询条件可以为空，默认查询所有，参数为模型类的字段名，只能使用赋值运算符，必须使用查询执行器；

  ~~~python
  # 根据手机号查询数据
  sql:
    select mobile from user_basic where mobile='1300000000'
  orm:
    # [<User 1146784652967542785>]
    User.query.filter_by(mobile='13066669999').all()
    # <User 1146784652967542785>
    User.query.filter_by(mobile='13066669999').first()
  
  ~~~

  * filter函数：查询条件可以为空，默认查询所有，参数为模型类名加上字段名，可以使用丰富的运算符，保修使用查询执行器；

  ~~~python
  # 根据手机号查询
  User.query.filter(User.mobile=='13066669999').all()
  
  ~~~

  

* 运算符：

  * 逻辑运算符：与或非都需要导入使用，多条件默认是and关系，非就是不等于

  ~~~python
  # 查询手机号13066669999,或者手机号尾号为9
  # or_是sqlalchemy提供的运算函数，需要导入使用
  from sqlalchemy import or_,not_,and_
  User.query.filter(or_(User.mobile=='13066669999',User.mobile.endswith('9'))).all()
  # .all() 是 查询执行器，最后执行，后面不能再加操作
  
  ~~~

  * 比较运算符：>、<、>=、<=、!=、==

* 偏移offset和限制条目数limit：

  * offset：参数为数值，表示起始位置
  * limit：参数为数值，限制返回条目数

  ~~~python
  # limit和offset的先后顺序，不影响查询结果；因为不是管道操作
  User.query.limit(1).offset(1).all()
  User.query.offset(1).limit(1).all()
  
  ~~~

* 排序：

  * order_by：asc表示升序，desc表示降序

  ~~~python
  User.query.filter().order_by(User.id.desc()).all()
  
  ~~~

* 复合查询：

~~~python
# 多条件：
# 把手机号尾号为9，按照用户id倒序排序
User.query.filter(User.mobile.endswith('9')).order_by(User.id.desc()).all()
# 把手机号尾号为9，按照用户id倒序排序的数量？
User.query.filter(User.mobile.endswith('9')).order_by(User.id.desc()).count()

~~~

* 优化查询：

  * ORM默认是全表扫描，使用load_only函数可以指定字段，优化查询；

  ~~~python
  from sqlalchemy.orm import load_only
  User.query.options(load_only(User.mobile)).filter().all()
  ~~~

  

* 聚合查询：

  ~~~python
  # 查询所有用户所有的粉丝数
  sql:
    select user_id,count(target_user_id) from user_relation group by user_id;
  orm:
    from sqlalchemy import func
  	from demo_query import Relation
    db.session.query(Relation.user_id,func.count(Relation.target_user_id)).filter().group_by(Relation.user_id).all()
  ~~~

  

* 关联查询：

  * 两种实现形式：
    * 第一种：Foreignkey

  ~~~python
  # 一对多：User和Relation
  class User():
    	# 一方定义关系,relationship函数，第一个参数表示另外一方的类名
      # relationship函数定义的关系选项，不对应数据库中的实体字段，只是在关联查询时，从一张表找到另外一张表
      follows = db.relationship('Relation',backref='user')
  class Relation():
    	# 多方定义外键
    	id = db.Column('relation_id', db.Integer,db.ForeignKey('user_basic.user_id') ,primary_key=True, doc='主键ID')
  
  # 一对多的查询
  user = User.query.get(1)
  user.follows
  # 多对一的查询
  r = Relation.query.get(1)
  r.user
      # 如果再flask-sqlalchemy中需要返回模型类对象的数据
      # 类似于__str__方法，实现对象的可读字符串；
      def __repr__(self):
        user = {
          'user_id':self.user_id,
          'mobile':self.mobile
        }
        return user
      
  ~~~

  ~~~python
  
  # Flask中没有迁移功能，需要使用扩展包实现，需要安装使用；
  flask-script和flask-migrate
  flask-script：提供脚本参数，类似于django中在终端执行命令；
  flask-migrate：提供的迁移框架，
  python demo_query.py db init 创建迁移文件夹
  python demo_query.py db migrate 创建迁移脚本文件
  python demo_query.py db upgrade 执行迁移脚本文件，创建表
  python demo_query.py db history 查看历史版本号
  python demo_query.py db downgrade 回退到历史版本
  
  ~~~

  

   * 第二种方式：primaryjoin：主要连接条件

     ~~~python
     class User():
       # 定义主要连接条件primaryjoin
         follows = db.relationship('Relation',primaryjoin='User.id==foreign(Relation.user_id)')
     
     user = User.query.get(1)
     user.follows
     ~~~

     

  * 指定字段连接查询：

    ~~~python
    # 查询用户手机号18516952650，关注了那些人？
    sql:连表查询
      select user_basic.user_id,user_basic.mobile,user_relation.target_user_id 
      from user_basic join user_relation on user_basic.user_id=user_relation.user_id 
      where user_basic.mobile='18516952650';
    
    orm:连表、过滤字段；
      from sqlalchemy.orm import contains_eager,load_only
    
     
    User.query.join(User.follows).options(load_only(User.id),contains_eager(User.follows).load_only(Relation.target_user_id)).filter(User.mobile=='18516952650').all()
    
    # SQL和ORM对比：
      User.query.join(User.follows)《===》user_basic join user_relation
      options(load_only(User.id),contains_eager(User.follows).load_only(Relation.target_user_id))《====》on user_basic.user_id=user_relation.user_id 
      
      filter(User.mobile=='18516952650')《====》 where user_basic.mobile='18516952650'
    ~~~

    

* 更新和删除

  * 都必须要commit提交数据

* 事务
  * flask-sqlalchemy中自带事务支持，会默认开启事务；
  * 也可以手动触发回滚：db.session.rollback()