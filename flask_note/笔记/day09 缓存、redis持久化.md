## 缓存

### 1 需求背景

* 缓存不是必须的，是为了提升性能而增加的
* 目标： 减少磁盘数据库的查询，比如mysql的查询 ，更多的从内存中读取数据
    * mysql查询 通常在1s左右 （几百毫秒， 0.xxs），1s以上通常认为是慢查询
    * redis 查询的性能 1s/1w+ 操作（更高 可达10W+)
* 使用场景
    * 前提： 读取频繁
        * 数据不经常变化，如省市区数据，一定会做缓存处理
        * 数据虽然变化频繁，但数据是产品的核心数据，比如评论数据，可以构建缓存，但缓存时间设置短一些，比如即时缓存5分钟。

### 2 缓存架构

数据存在哪？

多级缓存

* 本地缓存，一级缓存
    * 全局变量保存，内存中
    * orm框架的 queryset  查询集（查询结果集）   起到本地缓存的作用
        * django orm
        * sqlalchemy
* 外部缓存
    * 可以构建多级。二级缓存，三级缓存。区别在于有效期不同。
    * 外部存储
        * **redis**
        * memcached

### 3 缓存数据

保存哪些数据 ？ 数据以什么 类型 保存？

#### 3.1 缓存的数据内容粒度

* 一个数值

    * 比如手机短信验证码
    * 比如用户的状态数据  user:status ->  0 / 1

* 数据库记录

    * 不以单一视图单独考虑，而是考虑很多视图可能都会用到一些公共数据，就把这些公共的数据缓存，哪个视图用到，哪个视图就读取缓存取数据 ，（比如用户的个人信息，文章的信息）
    * 比较通用，缓存一个数据可以被多个视图利用，节省空间

    * 方式：

        * **Caching at the object level**  缓存数据对象级别

            * 通用

            ```
            mysql 中有用户的个人信息表
            每条记录 是一个用户的数据    一个数据实体
            
            user:1 ->  user_id ,name  mobile profile_photo intro  certi
            user:20 ->  user_id ,name  mobile profile_photo intro  certi
            ```

        * **Caching at the database query level**  缓存数据库查询级别

            * 相比缓存数据对象级别 不太通用，只适用于比较复杂的查询，才考虑使用

            ```
            sql = 'select  * from ..inner join  where ... group by  order by  limit'  -> query_results
            
            
            hash(sql) -> 'wicwiugfiwuegfwiugiw238'  md5(sql)
            
            缓存
            数据名称  					数据内容
            'wicwiugfiwuegfwiugiw238' ->  query_results
            
            使用的时候
            sql ->  md5(sql) -> 'wicwiugfiwuegfwiugiw238' 
            ```

* 一个视图的响应结果

    * 考虑单一的视图 ，只对特定的视图结果进行缓存

    ```python
      @route('/articles')
      @cache(exipry=30*60)
      def get_articles():
          ch = request.args.get('ch')
          articles = Article.query.all()
          for article in articles:
              user = User.query.filter_by(id=article.user_id).first()
              comment = Comment.query.filter_by(article_id=article.id).all()
            results = {...} # 格式化输出
         return results
    
    # /articles?ch=123   视图的结果resuls 缓存
    # 下一次再访问  ‘/articles?ch=123’
    ```

* 一个页面
    *  只针对 h5页面  （html5）  网页

    * 方式

        * 如果是服务器端渲染  （前后端不分离）

            ```
              @route('/articles')
              @cache(exipry=30*60)
              def get_articles():
                  ch = request.args.get('ch')
                  articles = Article.query.all()
                  for article in articles:
                      user = User.query.filter_by(id=article.user_id).first()
                      comment = Comment.query.all()
                 results = {...}
                 return render_template('article_temp', results)
            
              #  redis
              # '/artciels?ch=1':  html
            ```

        * 页面静态化。保存到 nginx 服务器，由 nginx 服务器返回给前端。

#### 3.2  缓存数据保存形式

针对的是外部缓存  redis

* 字符串形式

    ```
    user:1 ->  user_id ,name  mobile profile_photo intro  certi
    user1 -> User()对象 -> user1_dict
    
    key          value
    user:1   ->  json.dumps(user1_dict)
    			 pickle.dumps()
    			 
    json:
       1. 只能接受 列表 字典 bytes类型
       2. json转换成字符串 效率速度慢
    pickle ：django 中的 @cache() 使用的是 pickle 转成字符串
    	1. 基本支持python中的所有类型，（包括自定义的类的对象)
    	2. pickle 转换成字符串 效率速度 快
    ```

    * 优点： 保存一组数据的时候，存储占用的空间 相比其他类型可能节省空间
    * 缺点：整存整取 ，如果想获取其中的单一字段 不是很方便，需要整体取出 再序列化或反序列化， 更新某个字段 类似 ， 不灵活

* 非字符串形式

    * list  set  hash  zset 
    * 需要针对特定的数据来选型

    ```
    user:1 ->  user_id ,name  mobile profile_photo intro  certi
    user1 -> User()对象 -> user1_dict
    
    key    value 
    user:1  ->  hash {
    		name: xxx,
    		moible: xxx
    		photo: xxx
    }
    ```

    * 优点： 可以针对特定的字段进行读写，相对灵活
    * 缺点： 保存一组数据的时候，占用的空间相比字符串会稍大

### 4  缓存数据的有效期  TTL  (time to live)

缓存数据一定要设置有效期，原因/作用：

* 即时清理可以节省空间
* 保证数据的一致性，（弱一致性） ，保证mysql中的数据与redis中的数据，在更新数据之后还能保持一致。   虽然在 缓存数据的有效期内 redis与mysql中的数据不同 ，但是过了有效期后 redis会清理数据， 当再次查询数据时 会形成新的缓存数据，redis与mysql中的数据又相同了。

#### 4.1  redis的有效期策略

通用的有效期策略：

* **定时过期**

    ```
    set a 100  有效期 10min
    set b 100  有效期 20min
    ```

    开启一个计时器计时，当有效期到达之后 清理数据, 可以理解为每条数据都要单独维护一个计时器

    缺点： 耗费性能 

* **惰性过期**

    保存数据 设置有效期后 不主动计时，只有当再次访问这个数据（读写）的时候，去判断数据是否到期。如果到期清理并返回空，如果没到期，返回数据

* **定期过期**

    * 周期性检查数据是否过期。比如每100ms判断一次数据是否过期，如果有过期的数据，进行清理。

**Redis的有效期策略  ： 惰性过期 + 定期过期**

* redis实现定期过期的时候，还不是查询所有数据，而是每100ms 随机选出一些数据判断是否过期，再过100ms 再随机选出一些判断

思考：

如果在redis中保存了一条数据，设置有效期为10min，但是数据设置之后 再无操作， 请问 10min之后 这条数据是否还在redis的内存中？  答案： 可能存在也可能不存在

### 5 缓存淘汰  （内存淘汰）

背景： redis的数据有效期策略不能保证数据真正的即时被清理，可能造成空间浪费，再有新的数据的时候，没地方可以存存储， 为了存储新数据，需要清理redis中的一批数据，腾出空间保存新数据

淘汰策略 指 删除哪些数据

#### 通用的内存淘汰算法： LRU  &  LFU

* LRU（Least recently used，时间上最近最少使用）  以使用时间点来考虑

    思想： 认为 越是最近用过的数据，接下来使用的机会越大，应该清理那些很久以前使用过的数据

    ```
    cache_data = [
    	cache1      时间最近
    	cache2
    	cache5
    	cache4
    	cache3     时间最远
    ]
    
    操作过cache3
    cache_data = [
    	cache3
    	cache1      时间最近
    	cache2
    	cache5
    	cache4
    ]
    
    增加cache6
    cache_data = [
    	cache6
    	cache3
    	cache1      时间最近
    	cache2
    	cache5
    ]
    ```

    

* LFU （Least Frequently Used， 频率上最少使用）  以频率 次数来考虑

    思想： 认为使用次数越多的数据，接下来使用的机会越大，应该清理那些使用次数少的数据

    ```
    cache_data = {
    	cache1 : 100     
    	cache2: 2
    	cache5: 23
    	cache4: 89
    	cache3  :  10000   
    }
    
    操作了cache2
    cache_data = {
    	cache1 : 100     
    	cache2: 3
    	cache5: 23
    	cache4: 89
    	cache3  :  10000   
    }
    
    新增 cache6
    cache_data = {
    	cache1 : 100     
    	cache5: 23
    	cache4: 89
    	cache3  :  10000   
    	cache6: 1
    }
    
    cache_data = {
    	cache1 : 100     -> 50 
    	cache5: 23  -> 11
    	cache4: 89 -> 45
    	cache3  :  10000    -> 5000
    	cache6: 1 -> 1
    }
    ```

    * 效果更好 
    * 缺点： 牺牲了redis的部分存储性能，需要额外记录次数 频率，   还需要**定期衰减**

#### Redis的内存淘汰策略 （3.x版本以后）

- **noeviction**：当内存不足以容纳新写入数据时，新写入操作会报错。 默认
- allkeys-lru：当内存不足以容纳新写入数据时，在键空间中，移除最近最少使用的key。
- allkeys-random：当内存不足以容纳新写入数据时，在键空间中，随机移除某个key。
- **volatile-lru**：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，移除最近最少使用的key。
- volatile-random：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，随机移除某个key。
- volatile-ttl：当内存不足以容纳新写入数据时，在设置了过期时间的键空间中，有更早过期时间的key优先移除。

redis 4.x 版本之后 增加了两种

* allkeys-lfu
* **volatile-lfu**

redis中的配置

```
maxmemory <bytes>   指明redis使用的最大内存上限
maxmemory-policy volatile-lru  指明内存淘汰策略
```

#### 总结：

1. 如果将redis作为持久存储 ，内存淘汰策略 采用默认配置 noeviction
2. 如果将redis作为缓存，需要配置内存淘汰策略   选择合适的淘汰策略  

### 6.  缓存模式

应用程序如何使用缓存

* **读缓存**
    * 场景： 需要频繁读取查询数据 的场景
    * 方式 在应用程序与mysql数据库中间架设redis 作为缓存 ，读取数据的时候先从缓存中读取， 但是写入新数据的时候，直接保存到mysql中
* 写缓存
    * 场景： 需要频繁的保存数据 的场景
    * 方式 在应用程序与mysql数据库中间架设redis 作为缓存 ，保存数据的时候先保存到缓存redis中，并不直接保存的mysql中， 后续再从redis中同步数据到mysql中

#### 读缓存的数据同步问题：

修改了mysq中的数据，如何处理redis缓存中的数据

* 先更新数据库，再更新缓存

* 先删除缓存，再更新数据库
* **先更新数据库，再删除缓存**   发生问题的几率最小 ，负面影响最小

### 7 缓存使用过程中可能存在的问题

* 缓存穿透
    * 问题： 访问不存在的数据， 数据库没有 缓存也没有存储，每次访问都落到数据查询 
    * 解决：
        * 缓存中保存不存在的数据，比如将数据以-1保存，表示数据不存在，可以拦截 这种攻击，减少数据库查询
        * 需要引入其他工具  ，过滤器  ，按照规则来判断 是否可能存在，  比如 布隆过滤器
* 缓存雪崩
    * 问题： 同一批产生 的缓存数据 可能在同一时间失效，如果在同一时间大量的缓存失效，查询时又会落到数据库中查询，对数据库并发的有大量的查询，数据库吃不消，数据库又可能崩溃
    * 解决：
        * 将数据的有效期增加偏差值，让同一批产生的缓存数据不在同一时间 失效，将失效时间错开
        * 架设多级缓存， 每级缓存有效期不同
        * 以保护数据库出发， 为数据库的操作 添加锁 或者 放到队列中，强行的将并行的数据库操作改为串行操作，一个一个执行，防止数据库崩溃

### 8 头条项目的缓存的设计

* 服务器硬件层面的架设
    * 本地缓存
        * orm 查询结果集缓存
    * 一级外部缓存
        * redis  cluster  配置了缓存淘汰策略  （无需配置 持久化策略）  volatile-lru    4.0.13
* 程序编写开发上
    * 缓存 的数据  **Caching at the object level**   数据库对象级别，可以被多个视图利用
    * 缓存数据一定要设置有效期 ， 为了防止缓存雪崩，有效期要设置偏差值
    * 为了防止缓存穿透，缓存数据时 不存在的数据也要缓存下来
    * 读缓存
    * 大多数情况选择 先更新数据库 再删除缓存

### 9 头条项目缓存的数据保存形式

redis数据类型的设计 （redis数据类型选型）

redis 的list set hash zset 数据是不允许嵌套的， 数据元素都是字符串

* 用户个人信息数据 （类似参考的 文章缓存  评论缓存）

    ```
    user1 -> User1 -> name mobile photo
    user2 -> User2 -> 
    ```

    * 设计方式1 所有用户在redis中以一条记录保存

    ```
    key              value
    users:info  -> str X
    				  json.dumps({'user1': cache_data, 'user2': cache_data})
    				  
    			   list   set  X
    			   [json.dumps(user1_dict), json.dumps(user2_dict)]
    			   
    			   hash
    			   {
    			   	   'user1': json.dumps(user1_dict),
    			   	   'user2': json.dumps(user2_dict)
    			   }
    			   
    			   zset X
    			   	  member 成员     			score  分数/权重
    			   	json.dumps(user1_dict)      user_id
    ```

    考虑有效期:

    redis中的有效期不能对一条记录中的不同字段单独设置，最小只能给一条记录设置有效期

     所有数据只能有一个有效期，会造成缓存雪崩

    不采用

    * 方式2  每个用户在redis中单独一条记录

        ```
        user1 -> User1 -> name mobile photo
        user2 -> User2 -> 
        
        key                   value
        user:{user_id}:info 
        user:1:info
        user:2:info   ->    str     json.dumps(user2_dict)
        					hash  
        					{
        						"name": xxx,
        						"mobile": xx
        						'photo':xxx
        					}
        					
        
        str： 占用空间小 头条项目 为了保存更多的缓存数据 选择字符串
        hash: 存取灵活 
        ```

* 用户关注列表信息数据 ( 类似的还有 用户的文章列表 文章的评论列表 用户的粉丝列表等)

    需要缓存的是关注里中 关注的用户的user_id

    ````
    1号用户关注过 2 3 4 5 6 7
    ````

    每个人单独一条redis记录

    ```
    key                      value
    user:{user_id}:follows
    user:1:follows
    user:2:follows ->      str
    						   json.dumps([2,3,4,5..user_id])
    						
    					   list   set  X
    					       ['2','3','4', 'use_id',..]
    					       
    					   hash  X
    					        field      value
    					        user_id_2  follow_time  
    					        user_id_3   follow_time
    					        
    					   zset  有序集合  既能去重 还有序
    					        member       score
    					        user_id_2   follow_time
    					        user_id_3    follow_time 时间戳
    					        
    str  用户如果关注的人过多，整取数据不方便，而且列表一般是要分页取
    zset  可以批量分页取数据  还能排序  头条项目选择zset  
             更新数据库后 添加数据
    ```

### 10  头条项目redis持久保存的数据保存形式

* 服务器硬件层面的架设
    * redis  单机存储容量足够 ，再构建复制集 做高可用，防止主机redis挂掉
    * 配置持久化存储策略  RDB + AOF
    *  内存淘汰策略 配置  noeviction

* 保存的数据

    * 阅读历史   搜索历史
    * 统计数据 （之前使用数据库反范式设计的 冗余字段）比如用户的关注数量 粉丝数量等

* 阅读历史     （文章id列表）

    方式一： 所有人一条记录  X

    ```
    key    					value
    users:read:history      str json.dumps({'user_1': [], user_2:[]})
    							
    						list  set  X
    						hash
    						  {
    						  	"user_1": '2,3,4,5',
    						  	"user_2": '100, 20, 30'
    						  }
    						 zset
    						    member    score
    						    article_id   user_id
    						    ‘2，3,4,5'   user_id1
    						    '100, 20, 30'  user_id2
    ```

    方式二： 每人一条记录

    ```
    key       						value
    user:{user_id}:read:history
    user:1:read:history
    user:2:read:history     ->      list  
    							 [artilce_id, 2, 3, 4, ...]
    								set   没有顺序  X
    							(artilce_id, 2, 3, 4, ...)
    								hash  X
    								article_id   read_time
    								2             16724383275342
    								3             163232763827822
    								
    								zset  选择
    								member      score
    								article_id   read_time
    								2             16724383275342
    								3             163232763827822
    ```

* 统计数据

    方式一

    ```
    key   							value
    user:{user_id}:statistic
    user:1:statistic 
    user:2:statistic     -> 	hash
    						{
    							'article_count': 120,
    							"follow_count": xx,
    							"fans_count": xxx,
    							..
    						}
    ```

    方式二： 采用

    考虑运营平台可能需要对产品进行全平台大排名，比如 筛选发布文章数量最多的前20名用户   top问题 

    每个统计指标 一条redis记录（保存所有用户这个统计指标的数据）

    ```
    key							value
    statistic:user:follows
    statistic:user:fans
    statistic:user:articles  -> zset
    							mebmer   	score
    							user_id    article_count
    								1		100
    								2		3
    								3      11
    ```

    * list  set  zset hash 一条记录能保存的元素数量上限  42亿



#### 扩展  - 加密算法

* 散列  hash  （比如密码的处理）
    * 特点：
        * 不同的数据 计算之后得到的结果一定不同
        * 相同的数据计算之后得到的结果相同 
        * 不可逆
    * md5
    * sha1
    * sha256
    * 破解：彩虹表。穷举明文和密文的所有组合。
* 签名   (比如jwt token)
    * HS256   签名与验签时 使用相同的秘钥字符串  进行sha256计算 -> 签名值
    * RS256  签名与验签时 使用不同的秘钥字符串  进行sha256计算 -> 签名值
* 加密 （可以解密的)
    * 对称加密
        * 加密与解密使用相同的秘钥
        * AES
        * DES
    * 非对称加密
        * 加密 与解密使用不同的秘钥 （公钥私钥）
        * RSA    git、SSH公钥登陆，生成rsa公钥，上传到服务器。











