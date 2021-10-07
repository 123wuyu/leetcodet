## 单元测试

不是产品全部功能的完整测试，而是仅测试其中的某个函数 类，单元测试， 不仅测试人员要编写，通常开发人员也要编写单元测试。

### 1 需求：

* 每次修改代码（接口视图函数 、普通工具函数、工具类） 都要从新进行测试，而测试的过程基本不变，为了方便每次快速完成测试工作，可以编写测试代码来完成 测试  （单元测试）
* 测试过程不是只测试正常情况，也要测试 异常情况，看代码是否能对异常情况作出预期的处理，这也属于测试的过程，测试过程比较麻烦，所以编写一次测试代码，以后一直用这个测试代码来完成测试

### 2 断言 assert

```
if  resp.status_code != 200:
	print(’代码出错')
	raise('')
	
# 等价
assert resp.status_code == 200
```

通过assert断言 来表达预期的结果，python对于assert的处理类似于if else的处理，如果assert后面的表达式为真（达到了我们的预期），assert不做任何处理，代码继续执行，如果assert后面的表达式结果为假（表示没有符合我们的预期） ，assert 直接抛出异常 AssertionError

* assert不仅可以应用在单元测试中，有时自己也可以使用assert来代替if else的逻辑编写

### 3 unittest

* python的标准库，可以用来辅助编写单元测试

```python
import unittest

class TestClass(unittest.TestCase):
    """测试案例"""

    # 该方法在执行其他test_ 的方法之前先被执行，一般用来做测试前的准备工作
    def setUp(self):
        pass

    # 测试代码
    def test_xxxx(self):
        # 测试方法为了能让unittest帮助调用起来，方法名必须以test_开头
        pass
    
    def test_fun1(self):
        pass
    
    def test_fun2(self):
        pass  
    
    # 该方法会在测试代码test_执行完后执行，相当于做测试后的扫尾工作, 如果测试中有产生测试数据，一般用来进行测试数据的清理
    def tearDown(self):
        pass
  
if __name__ == "__main__":
    unittest.main()
    
# setUp() -> test_xxx() -> test_fun1() -> test_fun2() -> tearDown()
```



## 查看端口被哪个进程占用

```
sudo netstat -apn | grep 端口号
sudo netstat -apn | grep 5000

tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      28128/python

其中28128就是进程pid
kill -9 28128
```

## Gunicorn

WSGI的服务器 ，可以运行python web框架的程序 （django  flask)

uwsgi + django     gunicorn + django 

gunicorn + flask  uwsgi + flask

### 安装

```
pip install gunicorn
```

### 启动命令

```
gunicorn -b 0.0.0.0:8000 -w 4 --access-logfile /home/python/logs/access_app.log --error-logfile /home/python/logs/error_app.log toutiao.main:app

-b   bind 绑定ip地址端口
-w   workers 进程数量
--threads 线程数量
--access-logfile   记录的http请求访问日志文件保存的位置
--error-logfile  gunicorn服务器运行错误时记录的日志文件位置
toutiao.main:app ->  模块文件:应用程序对象 
					django   wsgi.py -> application
--help 查询帮助信息
```

头条项目  运行的目录   tbd_42/

## Supervisor

进程管理工具，可以帮助我们管理进程， 启动、停止、自动重启进程



### 安装

安装到系统环境，不用虚拟环境。

```
sudo pip install supervisor

# 生成主配置文件
echo_supervisord_conf > /etc/supervisord.conf

[include]
files = /etc/supervisor/*.conf

# 创建子配置文件
sudo vi /etc/supervisor/toutiao.conf
 
```

### 使用

编写配置文件

* 主配置文件  /etc/supervisord.conf   设置supervisor的运行方式
* 子配置文件   /etc/supervisor/*.conf    包含了 supervisor 看护的程序的启动命令  

```
supervisord -c /etc/supervisord.conf  # 启动supervisor

supervisorctl  命令，通过这个命令可以 管理 由supervisor看护的进程程序
```



子配置文件

```
[group:toutiao]     # 声明一个组，可以通过supervisor一起启动或停止这个组中的所有进程
programs=toutiao-app
programs=toutiao-mp
programs=toutiao-mis

[program:toutiao-app]  # 声明一个需要管理的进程 自定义的进程名
command=/home/python/scripts/toutiao_app.sh  # 启动进程的命令
directory=/home/python/toutiao-backend  # 程序运行时的工作目录
user=python  # 以哪个系统用户身份运行这个程序
autorestart=true  # 是否自动重启
redirect_stderr=false  # 程序中向屏幕输出的内容是否还输出到屏幕
loglevel=info  # supervisor管理这个程序的时候 记录的日志级别
stopsignal=KILL  # supervisor 停止这个程序的时候 使用哪个系统命令
stopasgroup=true  # 停止主进程的时候 是否连通子进程一同杀死
killasgroup=true

[program:toutiao-mp] 
...


[program:toutiao-mis] 
```



编写的 toutiao_app_start.sh

```shell
 #!/bin/bash    # 以终端运行下面的 linux 命令
 
source /home/python/.bash_profile    # 激活 bash 配置文件，使安装的第三方包命令可以使用
cd /home/python/tbd_42
workon toutiao
exec gunicorn -b 0.0.0.0:8000 -w 4 --access-logfile /home/python/logs/access_app.log -        -error-logfile /home/python/logs/error_app.log toutiao.main:app
```

添加可执行权限

```
chmod +x  toutiao_app.start.sh
```



## 接口文档

接口名称：

接口功能：

请求方式：

请求路径

请求参数： （表格）

| 参数名称 | 类型 | 是否必传 | 备注 |
| -------- | ---- | -------- | ---- |
|          |      |          |      |
|          |      |          |      |
|          |      |          |      |

返回值：

| 返回值名称 | 类型 | 是否必传 | 备注 |
| ---------- | ---- | -------- | ---- |
|            |      |          |      |
|            |      |          |      |
|            |      |          |      |

附加说明：

* 接口调用的注意事项
* 接口返回的可能状态码



网络层级

* 应用层  HTTP  Websocket  DNS SMTP
    * 应用层
    * 会话层
    * 表示层
* 传输层  TCP  UDP
* 网络层  IP  ICMP
* 数据链路层  RJ45  WIFI  3G  4G 光纤
    * 链路层
    * 物理层











