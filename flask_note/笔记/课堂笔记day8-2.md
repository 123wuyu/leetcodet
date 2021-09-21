## 定时任务

### 需求：

用户发表文章 的时候，用户的文章数量统计指标中 该用户的文章数量要累加（通过我们自己封装的redis工具来累加redis数据）



用户发表文章 接口 （保存文章的接口）

```
POST  /articles

请求参数： json
	title
	content
	channel_id
	
	请求头 Authorization: Bearer jwt token
	
返回值 json
201
{
	"message": "OK",
	"data": {
		"article_id": xx
	}
}
```

```python
from models.news import Article

class ArticlesResource(Resource):
    
    method_decorators = [login_required]
    def post(self):
        # 检验参数
        ...
        # 业务处理
        # 保存数据库
        # mysql 操作
        try:
        article = Article()
        db.session.add(article)
        db.session.commit()
        except :
            xxx
        else:
        	pass
        
        # 累计用户的文章数量   附属品 为了用户的体验 维护用户的数量 额外做的
        # redis操作
        try:
        	UserArticleCountStorage.incr(g.user_id, 1)
        except :
            db.session.rollback()
        else:
            db.session.commit()
        
        # 返回
        return {}
```

从底层本质上讲 ，这可以算是一个**分布式事务**

从用户的角度上考虑，维护redis的数据不是当前视图业务中的核心，如果redis没有保存成功，但是数据库中保存了用户的文章数量，我们的产品可以告知用户保存文章成功，对于redis的异常 允许出现，此时忽略 (redis 的异常不是经常发生，小概率事件)
    

    from models.news import Article
    
    class ArticlesResource(Resource):
        method_decorators = [login_required]
        def post(self):
            # 检验参数
            ...
            # 业务处理
            # 保存数据库
            # mysql 操作
            try:
            article = Article()
            db.session.add(article)
            db.session.commit()
            except :
                logger
                return 


​    
            # 累计用户的文章数量   附属品 为了用户的体验 维护用户的数量 额外做的
            # redis操作
            try:
                UserArticleCountStorage.incr(g.user_id, 1)
            except :
                logger
    
            # 返回
            return {},201
即时小概率的redis真发生了异常，还可以通过 mysql中的数据查询，查询到真实的用户文章数量，可以依此为依据，纠正redis中的数据

需要使用定时任务  周期性的 查询mysql数据 纠正（修正）redis中保存的统计数据

### 解决方案：

* crontab 

    * Linux 系统提供的定时任务命令

    * Linxu操作系统本身自己会有一些定时任务，又考虑到用户也可能要周期执行某些用户自己的定时任务，所以Linux就提供了一个crontab命令，允许用户添加自己的定时任务，由Linux统一管理素有的定时任务

    * 是Linux系统帮助完成的定时 （计时）

    * django-crontab 扩展  是对crontab命令 在django框架中使用时为 了方便进行的封装

        ```
    1 编写定时任务的脚本程序 （python文件，定时执行这个文件） 解决到点执行什么事？
        2 配置文件中 配置了定时任务的周期
        3 python manage.py crontab add 添加定时任务
        4 python manage.py crontab start 启动定时任务
        ```
    
    * 优点： 

        * 由操作系统进行计时，不占用应用程序的资源（不需要应用程序自己创建线程来进行计时）

    * 缺点：
    
        * 定时任务是独立于 应用程序单独运行的（由操作系统进行计时，定时任务也是操作系统调用完成的）,  应用程序与 定时任务之间的交互 不方便（应用程序django flask运行期间不能灵活的添加新的定时任务）
    
            * 保存订单 ->  产生30分钟计时的任务  30分钟之后判断用户是否支付
    
                ​               ->订单支付

* APScheduler

    * APScheduler （advanceded python scheduler）是一款Python开发的定时任务工具。
    * 定时是有应用程序自己来完成的，是这个python编写的工具自己来完成的计时，不是操作系统的定时
    * 优点：
        * 灵活， 应用程序（django  flask） 可以与这个定时任务工具 （apscheduler) 有很好的交互，可以在应用程序运行前 或者 运行中 随时添加 暂停 删除 定时任务，可以很好的管理

    * 缺点：
        * 需要应用程序 使用apscheduler 自己进行计时，所以会占用应用程序的资源

### APScheduler 使用

#### 1 安装

```shell
pip install apscheduler
```

#### 2 使用

```python
from apscheduler.schedulers.background import BackgroundScheduler

# 创建定时任务的调度器对象
scheduler = BackgroundScheduler()

# 定义定时任务
def my_job(param1, param2):
    pass

def my_job2(param1, param2):
    pass

# 向调度器中添加定时任务
#				 定时任务函数  执行的周期时间   args是任务函数被执行时的传入参数
scheduler.add_job(my_job,       'date',     args=[100, 'python'])
scheduler.add_job(my_job2, 'date', args=[100, 'python'])

# 启动定时任务调度器工作
scheduler.start()
```

#### 3  调度器 Scheduler

* BlockingScheduler  阻塞调度器

    ```
      from apscheduler.schedulers.blocking import BlockingScheduler
    
      scheduler = BlockingScheduler()
      
      scheduler.start()  # 此处程序会发生阻塞  卡住了  start方法不会返回
      
      print()  # 不能执行到
    ```

    执行start方法的时候，apscheduler 创建了一个子线程 ，在子线程中进行计时， 主线程中的start() 阻塞主，主线程不再往下执行

    作为独立进程时使用， 场景就是 需要单独写一个定时任务程序，独立于任何其他程序执行，仅仅就是为了完成定时任务而已，此时单独编写的程序 中 使用BlockingScheduler ，防止主程序退出

    

* BackgroundScheduler  后台调度器  非阻塞

    ``` 
     from apscheduler.schedulers.background import BackgroundScheduler
    
      scheduler = BackgroundScheduler()
      
      scheduler.start()  # 此处程序不会发生阻塞  不会卡住当前线程，start方法会立即返回，程序往下执行
      
      print()  # 能执行到
    ```

    * 作为其他应用程序（比如django 或flask ）中的一部分，属于附加的功能，不应该阻塞主程序（django 或flask）的执行

#### 4 执行器 executors

解决的 在同一个时间节点中 可能有多个定时任务都要被执行，此时 让调度器对象 scheudler 如何同时执行这些定时任务

* ThreadPoolExecutor  多线程

    ```
      from apscheduler.executors.pool import ThreadPoolExecutor
      # ThreadPoolExecutor(max_workers)  
      # ThreadPoolExecutor(20)
      
      executors = {
          'default': ThreadPoolExecutor(20)
      }
      scheduler = BackgroundScheduler(executors=executors)
    ```

* ProcessPoolExecutor  多进程

#### 5  触发器 Trigger

解决 定时任务执行的时间周期

* date 在特定的时间日期执行
* interval 经过指定的时间间隔执行
* cron 按指定的周期执行

#### 6 扩展用法

* 配置
* 任务管理
    * 添加定时任务
    * 暂定定时任务
    * 删除定时任务
    * 重新规划定时任务执行的周期时间

### 头条项目中 定时任务编写实现

定时任务有两类

* 程序运行前 就已经明确执行周期时间的 定时任务 （比如定时静态化页面 ）
* 程序运行中 需要新添加的定时任务  （比如 定时判断新订单的支付状态， 是视图产生的）



需求：  定时修正redis的统计数据  -> 运行前就明确的



* 创建调度器对象
    * 放到flask的工厂函数里创建，好处是  将scheduler对象保存到flask app中，可以方便在任何视图中随时使用current_app.scheduler.add_job 添加新的定时任务
    * BackgroundScheduler  后台调度器  非阻塞

### python解包

```
* 解列表或元祖
** 解字典
```



## RPC

### 1. 需求

头条首页 新闻文章列表查询

接口设计

```
GET  /articles?channel_id=12&page=xx&per_page=xxx

返回值 json
{
	"message": "OK",
	"data": {
		"results": [
			{
				"artilce_id": xxx,
				"title": xx,
				"aut_name": xx,
				“comment_count:xxx,
				..
            }, 
			{
			
			},
			..
		]
	}
}


```

视图编写

```python
class ArticlesResource(Resource):
    def get(self):
        # 检验参数
        channel_id
        page
        per_page
        
        # 业务处理
        # 调用推荐系统 获取当前用户的推荐文章里列表
        recomment_article_id_list -> [aid10, 11, 20, 23, ..]
        
        # 查询文章数据 （从缓存工具 redis&mysql）
        results = []
        for article_id in recomment_article_id_list:
            article_data = cache_aritlce.ArticleInfoCache(artice_id).get()
            results.append(article_data)
        # 返回
        return results
```

总结需求： 需要在两个子系统间调用，如何完成这样的子系统间**高效**调用？



### 2. 解决方式

* 本地调用

    * 将两个子系统的代码放到一个工程里，一起维护，相互导包完成调用

* 网络调用

    * HTTP调用

        ```
        # Web程序
        class ArticlesResource(Resource):
            def get(self):
                # 检验参数
                channel_id
                page
                per_page
                
                # 业务处理
                # 调用推荐系统 获取当前用户的推荐文章里列表
                # python发送http请求的模块 urllib  requests
                ret = urllib.request.urlopen('http://192.168.10.5:5000/recommends')
                recomment_article_id_list ->ret [aid10, 11, 20, 23, ..]
                
                # 查询文章数据 （从缓存工具 redis&mysql）
                results = []
                for article_id in recomment_article_id_list:
                    article_data = cache_aritlce.ArticleInfoCache(artice_id).get()
                    results.append(article_data)
                # 返回
                return results
        ```

        

    * RPC调用

        * 不再采用标准的HTTP协议传输数据，而是采用自定协议传输二进制数据，达到高效调用































