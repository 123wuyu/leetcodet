## 每日反馈

1. celery  与 多线程多进程的选择对比

celery：

优点：  

​	将异步任务与 产生任务的生产者（django 或者 flask）独立开，让异步任务的执行者 （celery worker ）在单独的机器上执行，可以不占用 应用程序（django 或flask）的资源 。

缺点：

  结构属于**重量级** ， 需要借助额外的消息队列 broker （redis 或者 rabbitmq）

2.  web找工作加分项：

*  突出 架构设计能力。 
*  突出 数据库设计 数据库优化  缓存设计 缓存选型 redis复制集和分布式的设计  elasticsearch   即时通讯  rpc
*  python自动化运维  shell编程
*  前端 vue.js（除了css样式之外的js代码）
*  数据结构（多）和算法（6个排序 2个查找）
*  设计模式

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
       	# ret = user_recomm(user_id, channel_id)
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

    * HTTP调用    HTTP/1.x

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

        * 缺点： HTTP  报文比较大 （ 为了传输几个参数，还需要补充 header 和body ）， 而是header是字符串类型，占用大，传输效率不高

        * 优点：  是标准的协议，几乎任何编程语言或者任何平台都可以发送和处理HTTP请求，通用，不强调 调用的客户端必须是专属的

        * 应用场景：

            * 外部通用调用。如果提供的服务要公开，提供给任何用户客户端来进行调用，通常采用公开标准标准的HTTP通讯  （REST API）  RESTful风格的HTTP网址 （接口）

                

    * RPC调用

        * 不再采用标准的HTTP协议传输数据，而是采用自定协议传输二进制数据，达到高效调用
        * 缺点： 因为是自定义的二进制 数据协议，传输的网络数据 不是标准的HTTP协议数据，发送和接收的一方必须都能遵守和处理这个自定的数据协议才可以完成调用，不通用，强调专用的客户端调用（必须专门编写特殊的客户端程序和服务器程序才能完成）
        * 优点： 传输的数据 采用压缩的二进制，数据量小，传输效率高，调用效率高
        * 应用场景： 
            * 内部专属调用。公司内部子系统之间调用，不把接口服务公开提供给外部用户访问，只是内部系统调用，可以自己定制专属的客户端与服务器程序。不考虑通用性，只考虑通讯的高效性，通常就选择rpc通讯

### 3 RPC

**远程过程调用**（英语：**Remote Procedure Call**，缩写为 **RPC**，也叫**远程程序调用**）

通过计算机网络 完成远程调用 

* 广义：

    * 通过计算机网络 完成远程调用 
    * HTTP 也是一种RPC的实现方式

* **狭义**：

    * 除了HTTP标准协议之外，采用专属协议来完成远程调用 

        

RPC协议包含：

* **数据协议**    解决网络上调用传输的数据格式是什么样的？  （rpc 自定）
* 传输协议  网络数据的传输怎么控制 是采用TCP 还是其他自定义的传输控制



```
需要传输的数据：
user_id = 123
channel_id = 12

HTTP协议
GET /xxxx
Content-Type: application/json
Content-Length: xxx
\r\n\r\n
{"user_id": 123, "channel_id": 12}

自定义协议举例
user_reco:123:12
```



开源的RPC通讯方案： （python）  RPC框架

* google   ->  **gRPC**  -> 数据协议 protobuf  (proto)
* facebook -> Thrift -> Thrift协议



RPC框架 实现的目标：

* 通讯高效
* 封装 ， 尽量隐藏底层上网络收发数据的实现，和应用数据 与网络传输数据的转换工作，  目的 是让使用rpc的用户在进行开发的时候，就像进行本地函数编写调用一样 来完成rpc编写调用
* 跨平台跨 语言   尽量能支持更多的编程语言和运行平台

### gRPC

* google
* 支持很多语言和运行平台
* 数据协议 protobuf
* 传输控制 HTTP/2

#### 安装

```shell
pip install grpc   # 在编写程序时 使用的库，其中包含了如何编写rpc服务器和rpc客户端程序需要的库
pip install grpcio-tools  # 一个编译工具，用来将rpc的接口定义文件 IDL文件 编译生成python代码 或其他语言代码
```

####  使用

1. 使用Protocol Buffers（proto3）的IDL接口定义语言定义接口服务，编写在文本文件（以`.proto`为后缀名）中。
2. 使用protobuf编译器生成服务器和客户端使用的stub代码
3. 编写补充服务器和客户端逻辑代码





```
web 服务
需要使用grpc框架中提供的python代码 导入user_reco函数
(因为 grpc框架提供的user_reco 函数中会分装参数转换 和网络数据传输)

推荐系统服务
需要定义user_reco 被调用的函数，但是这个函数不是简单的def声明即可，也需要使用
grpc框中提供的父类，在父类中定义user_reco 函数，
原因： 是grpc提供的父类中 帮助我们完成了 数据的转换 和网络数据的接收

->

调用的user_reco 函数 和被调用的user_reco 类  grpc从哪里有了这些代码？
需要我们声明给grpc ，让grpc产生这些代码

-> 
怎么声明给grpc？

因为考虑到要生成的代码可能包含不同的编程语言，使用任何一个编程语言都不能通用，所以
采用一个独立于任何编程语言之外的语法，只有grpc能够看到的语法来声明，让grpc根据我们声明
的东西生成 代码（比如python代码 或者 java等其他语言代码）


```

### 头条项目首页新闻推荐业务实现

#### 1  编写rpc 声明文件 （接口定义文件）

```
调用的函数名称 ： user_reco
调用的参数： 
	 user_id
	 channel_id
	 article_count
	 timestamp  明确给推荐系统， 让推荐系统知道返回新的推荐数据还是 历史的推荐数据
	       如果timestamp 传递最新的当前时间戳，推荐系统返回新的推荐数据
	       如果timestamp web传递历史的时间戳，推荐系统返回老的历史推荐数据

函数返回的参数：
      expousre  曝光埋点参数
      recommends  推荐文章列表 [
      	 {
      	 	article_id:xx
      	 	trace  埋点参数 
          		click  点击 (字符串）
          		collect
          		liking
          		read
      	 },
      	 {
      	 	aritlce_Id:xx
      	 	trace: 
      	 		click:
      	 		..
      	 }
      
      ]
      pre_timestamp  用于获取前一页历史推荐数据的时间戳 （应用在发送请求的时候）
      
```

#### 2  编译生成python代码

```shell
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. reco.proto
```

* `-I`   需要导入的proto文件从哪个目录中寻找  （`-I.` 表示从当前目录中查找）
* `--python_out`   proto文件中定义的message 字段生成的python代码文件保存到哪个目录
* `--grpc_python_out`   proto文件中定义的service 字段生成的python代码文件保存到哪个目录



生成的两个文件

* reco_pb2_grpc.py  保存的是proto文件中 使用servcie字段定义的方法 python代码
* reco_pb2.py 保存的是proto文件中 使用message字段定义的 数据类型的python代码

#### 3  编写客户端的调用代码 和 服务端的被调用代码

* 编写rpc服务端 （ 推荐系统的 rpc函数代码）
    * 把被调用的函数代码补全
    * 补充rpc服务器运行的代码 （主要是设置ip地址和端口号 对外提供rpc服务）
* 编写rpc客户端代码 （web系统的rpc调用代码）



#### 首页新闻推荐 Web视图编写

接口设计

```
GET /articles?channel_id=xx&timestamp=xxx

不强制用户登录  jwt token可传可不传

返回值： json
{
	"message": "OK",
	"data": {
		"pre_timestamp": xx
		"results": [
			{
				"artilce_id": xxx,
				"title": xx,
				"aut_name": xx,
				“comment_count:xxx,
				“track": {
					"click": xx,
					"share": xxx,
					"read": xx,
					...
				}
				..
            }, 
			{
			
			},
			..
		]
	}
}


```





### RPC 简易案例

```
# 原始目的
def add(num1, num2):
	return num1 + num2
	
# gRPC实现的样子
class Nums(object): 
	pass
	
class Sum(object):
    pass


# grpc_server 代码
class Calculate(gprc.xxxxx):

    def add(Nums_obj):
        num1 = Nums_obj.num1
        num2 = Nums_obj.num2
        result = num1 + num2

        Sum_obj = Sum()
        Sum_obj.result = result

        return Sum_obj
```



```
# 原始目的  100 + 200 
# grpc_client 代码
ret = add(100, 200) -> 300

import 工具类

stub = 工具类()

nums_obj = Nums()
nums_obj.num1 = 100
nums_obj.num2 = 200

stub.add(nums_obj) ->  Sum_obj对象  Sum_obj.result a
```













