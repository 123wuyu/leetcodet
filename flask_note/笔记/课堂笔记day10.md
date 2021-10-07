##  即时通讯（Instant Messaging）  IM

### 1 需求：

* 在线聊天
* 消息通知  （关注通知   点赞通知等）

本质： 为了让消息数据传输的高效 即时性， 实际上是**服务器在主动向 客户端推送消息**  （Push）

   推送的越快  越即时，所以叫即时通讯 （IM）

### 2 实现方案：

在线与离线 前提都是已经联网， 指的是 是否打开了应用 （手机app 或者 网页） ，如果用户处于打开应用状态，就叫 **在线** ，否则没有打开应用 就叫**离线**

* 离线推送
    * 适用场景： 手机App端
    * 实现：
        * ios     需要使用 苹果提供的 APNs服务，
        * 安卓 国外采用google提供的 FCM服务， 在国内采用第三方服务 
    * 在开发手机应用的时候 由app开发同学解决，与后端开发 无关

* **在线推送**
    * 适用场景： 手机App  、网页
    * 实现：
         * 自己架设在线推送服务
            	* 自行 开发 原始的tcp服务器 （socket编程）
            	* HTTP/1.x 
            	* Websocket
            	* **Socket.IO**
            	* HTTP/2  ( 原生支持服务器主动向客户端发送消息，但是HTTP/2 推广还需要几年)
         * 采用第三方服务
            - 网易云信
            - 融云
            - 环信
            - LeanCloud

### 3  HTTP/1.x  实现即时通讯  （服务器推送消息） 的方式

HTTP/1.x  特征 是服务器是被动的，只有在客户端发起请求之后，才能做出响应 返回给客户端数据，服务器是不能主动向客户端发送的数据

实现原理： 让客户端不断的向服务器 询问（发起请求 ）查询是否有新数据，服务在接收请求之后 回复（返回响应） 是否有新数据

* 轮询  polling
    * 客户端每过一定的时间间隔 （比如 1s） 发起一个请求询问
    * 请求的周期（时间间隔） 越小，即时性越高，但是同时造成对服务器的压力（在单位时间内接收到的请求更多）
    * 实现方法：
        * 服务器需要编写一个接口（视图） 用于让客户端请求 询问是否有新数据
        * 重点： 前端， 在前端中 需要定时向服务器发送请求 （AJAX  或 axios）
* Comet
    * 目的 是针对于轮询机制 想要进行优化，减少请求次数
    * 原理： 利用了HTTP/1.x  长链接           
        * HTTP/1.0   默认不是长连接   请求头 keep-alive
        * HTTP/1.1  默认 声明长连接
    * 客户端向服务器发送请求询问是否有新数据，服务器直到有了新数据才做出响应（减少请求次数）
    * 效果并不是很理想
        * 原因： 长连接只是一种愿望 （一种声明）不是强制性的，通讯的双方都可以随时终止长连接，或者对于对方表达的长连接 愿望，予以拒绝

### 4 Websocket

* 用来解决即时通讯，通信双发（ 客户端与服务器）可以随时向对方发送数据消息

* 新的协议 ，但是 **不是HTTP/1.x 的演进版本** 

* H5标准（HTML 5）中提出的协议 websocket

    ```
    html
    
    <h1></h1>
    <p></p>
    ```

* Websocket vs HTTP
    * Websocket 没有采用新的标准端口，而是复用了HTTP的80端口
    * Websocket 通讯的建立 是依赖于HTTP， websocket的第一次握手（不是TCP的三次握手）是发送了一个HTTP请求，向服务器表达 想要进行websocket通讯，服务器如果支持websocket并且愿意进行websocket，则会返回一个HTTP响应来告知 同意切换到websocket通讯

* 网址  ws://
* 目前 主流的浏览器的最新版本 基本都已经支持websocket通讯

* 优点： 见课件
* 缺点： 并不能兼容所有的浏览器， 古老的浏览器（比如ie 8 9 ） 是不支持websocket的

### 5 Socket.IO

* 是一个实现即时通讯的库（框架）     不是新的协议
* 背景：  为了兼容所有的浏览器，代码编写开发是 就要既支持http轮询，又要支持websocket， 为了只编写一套代码，同时完成轮询与websocket的支持 而开发出的一个工具

* 首先是由前端 开发出的一个js库， 后来后端发现觉得很好用，思路很正确，就改写成不同语言实现的框架
* 是目前主流开发即时通讯使用最多个工具框架
* **Socket.IO 不等价于 WebSocket**
    * socketio 是库 websocket是协议
    * socketio在实现websocket通讯的时候，对协议做了调整
        * 通讯的双发 （客户端和服务器）必须都得采用socketio编写才能完成通讯
        * 比如服务器使用socketio库编写完成的代码  前端如果仅仅使用原生的websocket js编写，是无法完成通讯的
* 优点： 编写一套代码，同时完成 轮询和websocket通讯 ，节省开发周期 开发成本
* 缺点： 要求前后端必须都采用socketio编写才可以

### 6 Python开发socketio服务器 端

#### 安装

```
pip install python-socketio
```

#### 使用

* 编写创建socketio服务器
* 编写即时通讯的业务（ 接收到客户端传来的数据之后，要做什么处理？ 在何时 向哪个用户推送什么数据）

#### socketio服务器创建

* 与现有的web应用框架 融合 ，把socketio作为web应用（django 或 flask）中的一部分

    * uwsgi + django
    * 采用多进程或 多线程模式运行
    * 每有一个客户端请求，就会创建一个子进程或者子线程来处理这个请求，请求处理完成的时候，再销毁这个子进程或子线程
    * 方案不好 
        * 需要分出来一些子进程或子线程来处理 即时通讯的请求，抢夺了原本用来处理web请求的资源
        * websocket使用真正的长连接，每一个长连接（对应一个客户端） 都是由一个子进程或子线程处理，连接不释放，进程或线程就不能回收， 服务器不能无休止的一直创建线程进程，所以支持的用户并发数量受限

* **独立架设socketio服务器**

    * 运行模式

        * 多进程或多线程

        * **协程模式**  （采用的方案）

            * 协程原理

            ```
            生成器
            
            def fun1():
            	print(100)
            	print(200)
            	yield   # 暂停代码 保存断点状态
            	print(100)
            	print(100)
            *	yield
            	print(100)
            	print(100)	
            	
            def fun2():
            	print(100)
            	print(200)
            	yield
            	print(100)
            	print(100)
            *	yield
            	print(100)
            	print(100)
            	
            gen_obj1 = fun1()  # 创建了生成器对象
            gen_obj2 = fun2()
            next(gen_obj1)
            next(gen_obj2)
            next(gen_obj1)
            next(gen_obj2)
            ```

            * 通常采用协程库（扩展库）来完成协程开发

                * 协程库能够自动帮助完成协程的执行切换

                * **eventlet**

                    ```
                    from multiprocessing import Process
                    p = Processs()
                    p.start()
                    
                    
                    from threading import Thread
                    t = Thread()
                    t.start()
                    
                    from eventlet import  Eventlet
                    
                    e1 = Eventlet()
                    e1.start()
                    e2 = Eventlet()
                    e2.start()
                    
                    ```

                * gevent

                * 协程库自动切换协程的原理： 偷天换日  狸猫换太子

                    * 切换时机： 一般是在程序代码中遇到io阻塞的时候（CPU无法继续执行，需要等待 内存中准备好数据 io操作 ，比如磁盘读写数据，网络收发数据）

                        ```
                        import eventlet
                        eventlet.monkey_patch()  # 替换python提供的io操作的标准函数 （比如 open  write read recv send)
                        
                        def fun1():
                        	a = 100
                        	b = 200
                        	c = a + b
                        	f = open("/xxx.txt", 'rb')
                        	f_data = f.read()
                        	...
                        ```

    * 协程运行socketio服务器的方式

        * pip install eventlet

        ```
          import eventlet
          eventlet.monkey_patch()
        
          import socketio
          import eventlet.wsgi
        
          #  Server对象理解为Flask里面的应用对象就可以
          #  sio对象是用来管理socketio即时通讯业务的
          sio = socketio.Server(async_mode='eventlet')  # 指明在evenlet模式下
          app = socketio.Middleware(sio)
          
          
          eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
        ```

### Socket.IO 业务编写

在websocket 编程中 ，收发的数据一般称为消息数据 ，为了区分 通讯双方发送的消息数据，我们会为消息数据来分类，每一类数据 叫做一个事件 （event)

* 接收客户端发送的事件消息数据

    * 按消息的事件类型来接受，实际就是编写事件消息的处理函数

        ```
        @sio.on(事件类型)  # 当接收到客户端传来的这一类事件消息数据的时候，处理的方法
        def handle_func():
        	"""事件处理函数“”“
        	pass
        ```

        * 事件类别：

            * connect  连接

                ```
                @sio.on('connect')
                def on_connect(sid, environ):
                    """
                    与客户端建立好连接后被执行
                    :param sid: string sid是socketio为当前连接客户端生成的识别id
                    :param environ: dict 在连接握手时客户端发送的握手数据(HTTP报文解析之后的字典)
                    """
                    pass
                ```

            * disconnect 断开连接

            * 自定义的事件  （起的字符串的名字）

                

* 向客户端发送事件消息数据

    ```
    sio.emit(事件类型, 消息数据内容, 接收人)
    ```

    如果发送的事件 是message事件

    ```
    sio.emit('message', {}, room=)
    sio.send({}, room=)
    ```

    

    * 全部发送

        ```
        sio.emit('following notify', {'user_id': 1, 'timestamp': xxx})
        ```

    * 单一发送

        * sid 是socketio为每一个连接的客户端分配的唯一id，与业务场景中的user_id没有直接的对应关系

        ```
        sio.emit('following notify', {'user_id': 1, 'timestamp': xxx}, room=sid)
        ```

    * 群组发送

        * socketio中群组就是房间的概念  room
        * 创建组  sio.enter_room(sid,  组名/房间名 字符串)
        * 离开组  sio.leave_room(sid, 组名/房间名 字符串 )
        * 查询组   sio.rooms(sid) -> 列表  包含了sid客户端所在的所有组名

        ```
        sio.emit('following notify', {'user_id': 1, 'timestamp': xxx}, room=房间名)
        ```

### 头条项目中聊天机器人的业务实现

#### 1 提取命令行参数

```
import sys

# sys.argv  存放了启动命令的命令行参数
# python server.py 8080
# sys.argv -> 列表
# sys.argv -> ['server.py', '8080']
```

#### 2 业务

* 连接事件  connect

    * 用户在客户端中连接之后 ，服务器主动向客户端 发送第一声问候

* 与前端达成约定 ，聊天的消息数据事件类型 message

    * 数据格式

        ```
        {
            "msg": 聊天内容,
            "timestamp":  发送的时间戳
        }
        ```

### 头条项目消息推送通知功能

* **关注通知**  点赞通知 评论通知

* A 关注了 B

    * A用户 请求 flask web程序， 要关注b用户

    * flask web程序接收到http请求之后，在关注接口中保存 数据库记录A关注B

    * 在返回给A 之前，应该向B用户推送 关注通知（A关注了你）

    * flask 的关注接口 返回http响应给A ，告知A 关注成功

    * 但是推送是需要有Socketio服务器完成了，推送给B

        

* 本质：  需要flask程序与socketio服务器配合完成

* 解决思路：  引入消息队列（rabbitmq  或者 redis) ,flask将推送的任务存入消息队列中， socketio服务器从消息队列中 取出推送的任务，完成推送

    （思路过程很类似于celery的实现原理）

* 实现方法：

    * 工具

        * socketio框架中提供了一个Manager 的工具类，可以帮助我们想消息队列中添加 推送的任务（flask web程序），也能帮住我们从消息队列中 取出推送的任务 （socketio服务器）
        * 可以选择redis 或者**rabbitmq** 充当其中的消息队列

    * ```shell
        pip install kombu
        
        							# rabbitmq地址
        mgr = socketio.KombuManager('amqp://')
        ```

    * 编写代码

        * flask web程序

             借助mgr 帮住flask 将 需要推送给指定接收人推送的指定的事件类型的消息数据内容  任务存放到rabbitmq中

            ```
            # 在工厂函数里编写
            mgr = socketio.KombuManager('amqp://', write_only=True)
            
            # 在flask的视图中编写
            mgr.emit(事件类型，消息数据内容，接收人room= taget_user_id)
            ```

            ```
            # 关注视图
            POST /user/following
            请求参数 json
            {
            	"target": 被关注的用户id
            }
            Authorization: Bearer jwt token
            返回值 JSON
            ```

            

        * socketio服务器

            添加给sio对象的 mgr能够自动的从rabbtimq中取出推送任务，并且通过sio对象完成这个推送任务

            ```
            mgr = socketio.KombuManager('amqp://')
            sio = socketio.Server(async_mode='eventlet', client_manger=mgr)
            ```

        * 还需要连带解决的问题：

            * flask中不知道被关注用户B  连接socketio服务器时的客户端id （sid） 也就是意味着 flask不能直接通过指明用户B所在客户端id（sid） 来明确消息通知的接收人？

            * 解决的方式

                 让flask与socketio服务器之间达成约定，flask能够知道被关注用户B的user_id ,如果用户B的客户端连接了socketio服务器之后，socketio服务器为用户B创建了一个专属房间room ，房间名为用户B的user_id, 那flask也能通过指明接收人为用户B的user_id的房间号 就可以执行接收人

            * 实现：

                * flask 服务器

                    ```
                    # target是被关注的用户user_id
                    mgr.emit(.., {}, room=str(target))
                    ```

                * socketio服务器

                    * 被关注的用户B 在链接socketio服务器的时候 需要携带用户身份，socketio服务器才能识别出用户B的user_id， 进而将用户B添加到专属房间中
                    * 用户的身份凭证 可以直接使用flask web中签发的jwt token
                    * sio.on('connect')事件处理方法中检验用户的身份token
                    * sio.enter_room(sid,  str(user_id))

    * 测试消息通知  A关注B

        * 启动flask 与socketio服务器
        * B用户 13911111111 请求flask登录接口   jwt token
        * B用户携带token 连接socketio服务器
        * B用户 订阅 following notify 事件
        * A用户13922222222 请求flask登录  jwt token
        * 携带token 请求flask关注接口 

### 注意：

* 在flask中使用socketio  工作模式  production
* 关于 socketio中 connect事件函数的定义  实际上只有一个

### 总结

* 什么是即时通讯  服务器主动推送消息
* 在线推送如何实现
    * HTTP/1.x   轮询 & comet
    * Websocket 
* Websocket
    *  与HTTP的关系
    * websocket  vs  http  vs  tcp
    * 优缺点
* SocketIO   库 框架
    * 背景 使用原因
    * python服务器 开发
        * 协程创建socketio服务的原因和 方法
        * 接收数据和发送数据的方法  sio.on()     sio.emit()

* 业务

    * 聊天业务

    * 关注消息通知的推送
        * 问题的背景   flask 与socketio配合
        * 解决思路    rabbitmq
        * 实现    KombuManager
        * flask 与socketio 关于消息接收人的配合问题  创建房间





