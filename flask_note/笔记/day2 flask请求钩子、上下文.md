### 1.请求信息

* 固定参数：
  * 语法：<默认的是字符串，兼容数值>
  * 限制数据类型<int、float>
  * 转换器：Flask中默认6种
    * 整型值、字符串、浮点值、any、path、uuid

* 当内置转换器无法满足需求是，可以自定义转换器

  * 步骤：

    * 1.定义转换器类，继承自baseconverter

    * 2.把自定义的转换器类，添加到转换器字典容器中

    * 3.在装饰器中使用转换器

      

* 请求对象：request，args/form/method/url/headers/files/cookies；request.json/request.get_json()

### 2.响应信息

* 模板：render_template，第一个参数为模板文件名
* 重定向：redirect，参数为具体的url地址
* json：jsonify，不仅会把数据转成json字符串，还会把响应的类型改成application/json；参数为python的数据类型，例如字典
* 返回元组信息：Flask中返回的数据都是存入元组中，(字符串，状态码，响应头)
* 作业：请问能够返回数值、字典、列表吗？

### 3.状态保持

* cookie：实现状态保持的方案；存储的位置不同，key/value都存在浏览器中

  ~~~python
  @app.route('/set')
  def index():
      # 使用make_response生成响应信息
      resp = make_response('set cookie info')
      # 设置cookie信息，并且设置有效期，单位为秒
      resp.set_cookie('itcast','python42',max_age=60)
      return resp
  
  # cookie获取
  @app.route('/get')
  def get_cookies():
      # 使用request对象，获取cookie信息
      itcast = request.cookies.get('itcast')
      return itcast
  
  ~~~

  

* session：实现状态保持的方案；key存在浏览器中，value存在服务器中；

  ~~~python
  # 设置session
  @app.route('/set')
  def index():
      # session信息的设置
      session['itcast'] = 'python42'
      return 'hello world'
  
  # 获取session
  @app.route('/get')
  def get_session():
      # session信息的设置
      itcast = session.get('itcast')
      return itcast
  
  ~~~

  

### 4.异常处理

* abort，参数为异常状态码，只能是符合http协议的异常状态码

* 应用场景：配合error_handler装饰器实现自定义错误页面；

  

### 5.请求钩子

* 请求前执行
  * before_first_request只执行一次
  * before_request每次请求前都执行
* 请求后执行
  * after_request请求后执行，没有异常的情况下，需要接受参数，参数为响应对象
  * teardown_request请求后执行，即使有异常，需要接受参数，参数为异常信息

* 作业：after_request在代码中出现abort异常信息时，为什么依然执行？异常是指什么异常？

### 6.上下文对象

* 请求上下文：
  * request：获取请求信息，比如表单参数、查询字符串等；
  * session：操作用户会话信息，session['key'] = value,session.get('key')
* 应用上下文：
  * current_app：用来获取程序的各种配置信息，也可以用来记录项目日志
  * g：在请求过程临时记录数据；

* 生命周期：current_app生命周期最长，request和g在请求后会被销毁，session根据会话的有效期决定

### 7.手动开启上下文

* 应用场景：当代码没有运行时，我们可以通过手动开启上下文，获取程序相关信息和数据，一般用来测试代码；
* 手动开启应用上下文：app.app_context()
* 手动开启请求上下文：app.request_context(请求的数据信息，字典数据)



