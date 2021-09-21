

## Elasticsearch

### 1 需求：

搜索

### 2 ES

* Elasticsearch 是一个**数据库**（其中保存的是索引数据，用于检索使用），在这个索引数据库的基础之上，实现了搜索引擎的功能

* Django 

    * haystack + es

    ```
    创建索引类
    配置es的地址
    python manage.py rebuild_index  # 在es中创建索引库（数据库），并且将mysql中的数据导入到es中
    
    搜索的时候，我们通过视图传递的关键词，是通过 haystack 先在es库中搜索出匹配的条目（商品sku id)，然后再去mysql中查找这些条目对应的具体数据信息 (商品的详细信息)
    ```
    * django  ->   django orm  ->    sql ->  mysql
    * django  ->   haystack   -> REST API -> Elasticsearch

* java实现的，但是提供**REST API** 来进行操作使用 （es对外提供了http网址，向特定的网址发送http请求就能完成数据的增删改查操作） 

* 9200 端口

* **Elasticsearch是分布式的**   （数据分布存储在不同的elasticsearch服务器上)

* **Elasticsearch 有2.x、5.x、6.x 三个大版本**,  **我们在黑马头条中使用5.6版本**

### 3  es的搜索引擎实现原理

* 倒排索引（反向索引）
* 分析  （分词 + 标准 + 过滤）
* 相关性分数计算 加以排序

#### 3.1  倒排索引

```
data_1. "The quick brown fox jumped over the , lazy+ dog"
data_2. "Quick brown foxes leap over lazy dogs in summer"
```

正向索引

```
索印列		 The quick brown fox  jumped over ....
data_1     1    1    1    1      1    1
data_2               1                1
```

select *   from  ...   where  data_id =xxxxx

正向索引 思考方向: 是查询每个记录中有哪些词

反向索引 （倒排索引）

```
Term索引列  data_1  data_2   data_3
-------------------------
Quick   |       |  X
The     |   X   |
brown   |   X   |  X
dog     |   X   |
dogs    |       |  X
fox     |   X   |
foxes   |       |  X
in      |       |  X
jumped  |   X   |
lazy    |   X   |  X
leap    |       |  X
over    |   X   |  X
quick   |   X   |
summer  |       |  X
the     |   X   |
itcast  |       |        |    X
------------------------
key = 'brown  quick  itcast' ->  ['brown' 'quick' 'itcast']

brown      X      X    
quick      X
itcast                       X
-----------------------
		  2 *0.2   1 *0.2    1*0.6
```

select    * from ...  where term = 'brown'  -> data_1   data_2

反向索引 思考方向： 根据词来查询，这词在哪些记录中出现过

#### 3.2 分析

* 分词

* 标准化

    * 字母大小写 统一

    * 单复数要统一

    * 单词的过去式等形式要统一

    * 同义词 关联补充

        * 跳   跳跃  跃

        ```
        Term      Doc_1  Doc_2
        -------------------------
        brown   |   X   |  X
        dog     |   X   |  X
        fox     |   X   |  X
        in      |       |  X
        jump    |   X   |  X
        lazy    |   X   |  X
        over    |   X   |  X
        quick   |   X   |  X
        summer  |       |  X
        the     |   X   |  X
        ------------------------         
        ```

* 过滤
    * 过滤掉 字符 汉字之外的字符     '中国,人' 去掉逗号
    * 过滤 没有实际意义的词      '一个苹果'  过滤掉 ’一个‘

#### 3.3 相关性分数计算

* 通过 TF/IDF 算法来计算相关性分数
* 再按照相关性分数  排序，分数越高 表示越匹配，排名越靠前

#### 3.4 全文检索 原理总结

* 保存词条token 的阶段
    1. 将要保存的数据 （字符串） 先进行分析 过程（ 分词 ->  标准化 -> 过滤）
    2. 将分析之后的形成的标准化的词条（token) 保存到反向索引中，形成反向索引库
* 搜索 的阶段
    1. 首先将用户输入的关键词 进行分析 （包含 分词 -> 标准化 -> 过滤）
    2. 在将关键词分析之后形成的标准化词条 在反向索引库中进行查询检索
    3. 将匹配的结果进行相关性分数计算 
    4. 按照相关性分数结算的结果 由大到小排序返回

### 4 ES的概念

```
Relational DB -> Databases 数据库 -> Tables 表 -> Rows 行 -> Columns 列
Elasticsearch -> Indices 索引库 -> Types 类型 -> Documents 文档 -> Fields 字段/属性
```

### 5 ES 集群

* ES天生是分布式集群的，也就是说 ES实现了分布式存储，即使只有一台es服务器，es程序也是分布式存储的，目的是方便扩容

* ES在将数据进行分割存储的时候，首先考虑的不是 当前有几台机器，而是以虚拟的概念来划分 数据的不同分片， 也就是说 在创建每一个索引库的时候， 使用者都需要指明想将这个索引库的数据分成几个分片，然后 es 才会考虑根据当前有几台机器，再将这几部分分片平均分配到 不同的机器上

* ES分布式集群能够自动进行故障转移

* 设置

    ```
    PUT /blogs    # blogs，索引库名字
    {
       "settings" : {
          "number_of_shards" : 5,  # 主分片的数量，将数据分割成几部分
          "number_of_replicas" : 1   # 对于每一个主分片的数据，想要保存几个副本数据
       }
    }
    ```

    * number_of_shards 主分片的设置，只能在创建索引库的时候 设置一次，后续不允许修改
    * number_of_replicas  副本数量的设置，后续是可以修改的

    * 如果创建索引库的时候没有指明 分片数量 ，则使用默认值 ： number_of_shards=5      number_of_replicas=1

* 查询集群的状态

    ```
    GET  /_cluster/health
    ```

### 6 curl 

* Linux 系统提供的用于发送http请求的命令

* 利用 curl 命令，直接访问 ES的REST API 来完成es的操作

    ```
    curl -X http请求方式  网址  -H 请求头 -d 请求体数据
    
    curl -X GET www.itcast.cn 
    
    如果是GET请求，请求中又不需要携带请求体数据，则 -X GET 可以省略
    curl www.itcast.cn
    
    curl 127.0.0.1:9200/_cluster/health?pretty
    
    ?pretty 美化 es 返回的json数据
    ```

### 7 中文分析器

* es 安装完成后 ，有标准分析器 standard，能对英文进行分析处理。

* es 默认没有中文分析器。 让 es支持中文的分析处理（ 分词 标准化 过滤） ， 需要安装扩展  ik中文分析器  （elasticsearch-analysis-ik）

* 测试分析效果的接口命令

    ```
    GET  /_analyze
    
    curl -X GET 127.0.0.1:9200/_analyze?pretty -d '
    {
      "analyzer": "ik_max_word",
      "text": "我是&中国人"
    }'
    ```

### 8 库操作 （索引库）

* 创建

    ```
    # ES 2.x
    PUT /库名 
    {
    	"settings": { ... any settings ... },  # 库的设置
        "mappings": {  # 库中类型表的结构
            "type_one": { ... any mappings ... },
            "type_two": { ... any mappings ... },
            ...
        }
    }
    
    # ES 5.x  之后
    PUT /库名 
    {
    	"settings": { ... any settings ... },  # 库的设置
    }
    
    eg： PUT /blogs
    {
       "settings" : {
          "number_of_shards" : 3, 
          "number_of_replicas" : 1
       }
    }
    
    curl -X PUT 127.0.0.1:9200/blogs -H 'Content-Type:application/json' -d '
    {
       "settings" : {
          "number_of_shards" : 3, 
          "number_of_replicas" : 1
       }
    }
    '
    ```

* 查询

    ```
    GET  /_cat/indices       
    curl 127.0.0.1:9200/_cat/indices?pretty
    ```

* 修改

    ```
    PUT  /库名
    {
    	"settings" : {
          "number_of_replicas" : 2
       }
    }
    ```

* 删除

    ```
    DELETE  /库
    
    DELETE /index_one,index_two
    DELETE /index_*
    
    DELETE /_all
    DELETE /*
    ```

### 9 types 类型操作 （表）

* 明确 es 中保存什么数据 （以头条项目为例）

    查询什么数据 就保存什么数据

    用户输入关键词的时候，产品中要给用户查询的是匹配的 新闻文章，所以，用户的关键词能够进行检索的来源 应该是匹配我们所有的新闻文章中可能出现的词条  保存文章的数据

    分析文章用户关键词可能出现的字段

    * title
    * content
    * article_id
    * user_id
    * status  -> （用于搜索是过滤使用 ）
    * create_time

- 创建

    - mapping  映射，一种结构信息，表示es的一个类型表中 具备哪些字段，每个字段是什么类型，这种结构关系 就叫做映射

    - es 2.x  字符串 string

    - es 5.x 字符串 text

    - `_all` es自己隐式维护， 字符串类型， 内容默认是将类型表中的所有字段的内容 以字符串加空格的方式 拼接起来之后的数据

        ```
        {
        	title: 'python web',
        	"content": xxx,
        	article_id: 12,
        	user_id: 24,
        	status: 2,
        	create_time: xxxxx
        }
        _all: 'python web xxx 12 24 2 xxxxx'
        ```

    * boost 加速 ，干预 es 的自动相关性分数计算，如果想让关键词匹配某个字段的结果排名更靠前，可以使用boost参数来调整相关性分数计算的权重

        

    ```
    PUT  /库名/_mappings/类型表名 
    PUT /articles/_mappings/article
    {
    	"_all": {
    		"analyzer": "ik_max_word"
    	},
    	"properties": {
    		"title": {
    			"type": "text",
    			"analyzer": "ik_max_word",
    			"include_in_all": true,
    			"boost": 2  # 表示相关性分数乘以2倍
    		},
    		"content": {
    			"type": "text",
    			"analyzer": "ik_max_word",
    			"include_in_all": true
    		},
    		"article_id": {
    			"type": "long",
    			"include_in_all": false
    		},
    		"user_id": {
    			"type": "long",
    			"include_in_all": false
    		},
    		"status": {
    			"type": "integer",
    			"include_in_all": false
    		},
    		"create_time": {
    			"type": "date",
    			"include_in_all": false
    		}
    	}
    }
    
    ```

- 查询

    ```
    GET  /库名/_mappings/表名
    
    curl 127.0.0.1:9200/articles/_mappings/article?pretty
    ```

- 修改

    - 增加新的字段  （支持）

        ```
        PUT  /库名/_mappings/表名
        {
        	"properties": {
        		"new_tag": {
        			"type": "text"
        		}
        	}
        }
        ```

    - 修改原有字段 （不支持）

        解决方式：

        * 从新创建索引库和表

        * 将原库中的数据 导入到新库中

            ```
            curl -X POST 127.0.0.1:9200/_reindex -H 'Content-Type:application/json' -d '
            {
              "source": {
                "index": "articles"
              },
              "dest": {
                "index": "articles_v2"
              }
            }
            '
            ```

        * 删除原有索引库，为新库起别名

            ```
            curl -X DELETE 127.0.0.1:9200/articles  删库
            
            curl -X PUT 127.0.0.1:9200/articles_v2/_alias/articles
            ```

        工程实践方法

        ```
        PUT  /articles_v1 
        PUT  /articles_v1/_alias/articles  起别名 artilces
        
        PUT /articles_v2
        PUT /articles_v2/_alias/articles 
        ```

- 删除

    - es 5.x 建议我们 一个索引库中只创建一个 类型表 
    - 删除库 就删除了表

### 10  文档数据操作 （数据行）

* 文档说明

    es每条记录都是一个文档，文档除了我们声明的字段之外，还有额外的 元数据

    * `_index`

        文档在哪存放  索引库

    * `_type`

        文档表示的对象类别

    * `_id`

        文档唯一标识

    

- 创建 增加

    * 使用自定义的文档id

        ```
        PUT  /库名/类型名/id
        
        curl -X PUT 127.0.0.1:9200/articles/article/150000 -H 'Content-Type:application/json' -d '
        {
          "article_id": 150000,
          "user_id": 1,
          "title": "python是世界上最好的语言",
          "content": "确实如此",
          "status": 2,
          "create_time": "2019-04-03"
        }'
        ```

    * 自动生成文档id

        ```
        PUT  /库名/类型名
        ```

- 查询

    - 根据文档id查询文档数据

    ```
    GET /库名/类型名/id
    
    curl 127.0.0.1:9200/articles/article/150000?pretty
    
    curl 127.0.0.1:9200/articles/article/150000?_source=article_id,title
    
    curl 127.0.0.1:9200/articles/article/150000?_source=article_id,title\&pretty
    ```

    - 判断文档是否存在

    ```
    HEAD  /库名/类型名/id
    
    curl -i -X HEAD 127.0.0.1:9200/articles/article/150000
    状态码 200 存在 404 不存在
    ```

- 修改

    ```
    POST/PUT  /库名/类型名/id
    
    curl -X POST 127.0.0.1:9200/articles/article/150000 -d '   错误
    {
    	"title": "确实如此"
    }
    '
    
    curl -X PUT 127.0.0.1:9200/articles/article/150000 -H 'Content-Type:application/json' -d '
    {
      "article_id": 150000,
      "user_id": 1,
      "title": "确实如此",
      "content": "确实如此",
      "status": 2,
      "create_time": "2019-04-03"
    }'
    ```

    * es修改的处理 仍然是先删除文档 后 新建文档
    * 注意 修改文档数据的时候 那些不修改的字段也要传递
    * `_version` es为每个文档数据维护的版本号，文档数据只要发生变化，版本号就会自动增加

- 删除

    ```
    DELETE  /库名/类型名/id
    ```

- 取回多个文档

    ```
    curl -X GET 127.0.0.1:9200/_mget -d '
    {
      "docs": [
        {
          "_index": "articles",
          "_type": "article",
          "_id": 150000
        },
        {
          "_index": "articles",
          "_type": "article",
          "_id": 150001
        }
      ]
    }'
    ```

### 11 ES中数据的来源

* 初始阶段，是将其他数据库的数据导入到es中
    * django  haystack    python manage.py rebuild_index
    * 使用logstash 工具 从mysql中导入数据到es
* 运行中的阶段， 可以程序中，在保存mysql数据的时候，同时也将数据保存到es中
    * django  haystack  配置文件中   haystack_realtime_signal
    * 自己编写程序，在视图中保存数据库mysql的时候一起也保存到es中

#### 11.1 logstash

* 是es公司提供的，但是 不是随着elasticsearch 一同安装的，需要单独安装
* 也是java写
* 作用： 可以用来同步数据

* 安装 参考课件

使用

```
sudo /usr/share/logstash/bin/logstash -f logstash配置文件
```

关于配置文件

```
#  从哪里读取数据
input{
     jdbc {
     	 # java读取mysql数据程序的驱动库
         jdbc_driver_library => "/home/python/mysql-connector-java-8.0.13/mysql-connector-java-8.0.13.jar"
         jdbc_driver_class => "com.mysql.jdbc.Driver"
         
         # mysql的地址
         jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/toutiao?tinyInt1isBit=false"
         jdbc_user => "root"
         jdbc_password => "mysql"
         
         # logstash 工具读取mysql数据的时候 是否分页读取
         jdbc_paging_enabled => "true"
         jdbc_page_size => "1000"
         jdbc_default_timezone =>"Asia/Shanghai"
         
         # logstash 在mysql中执行什么sql语句来读取数据
         statement => "select a.article_id as article_id,a.user_id as user_id, a.title as title, a.status as status, a.create_time as create_time,  b.content as content from news_article_basic as a inner join news_article_content as b on a.article_id=b.article_id"
         
         # 是否是让logstash工具追踪mysql的每条记录中的特定字段
         use_column_value => "true"
         tracking_column => "article_id"
         
         clean_run => true
     }
}

# 将数据导出到哪里
output{
      elasticsearch {
         hosts => "127.0.0.1:9200"
         index => "articles"
         document_id => "%{article_id}"
         document_type => "article"
      }
      stdout {
         codec => json_lines
     }
}
```

### 12 ES的查询

#### 12.1 基本查询



```
GET /库名/类型表/_search?q=查询关键字
```

* 根据文档id查询

* 查询所有

    ```
    curl 127.0.0.1:9200/articles/article/_search?_source=article_id,title\&pretty
    ```

    es默认开启分页，每页10条

    * from  从第几条开始
    * size 每页几条

    ```
    curl 127.0.0.1:9200/articles/article/_search?_source=article_id,title\&from=11\&size=5\&pretty
    ```

* 全文检索

    ```
    curl 127.0.0.1:9200/articles/article/_search?q=title:python\&_source=title\&pretty
    
    curl 127.0.0.1:9200/articles/article/_search?q=_all:python\&_source=title\&pretty
    
    keyword关键词 "python web"  %20表示空格
    curl 127.0.0.1:9200/articles/article/_search?q=_all:python%20web\&_source=title\&pretty
    ```

#### 12.2 高级查询

```
GET /库名/类型表/_search -d
{
  查询条件
}
```

* **全文检索 match**

    ```
    curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
    {
    	"_source": ["article_id", "title"],
    	"from": 11,
    	"size": 5,
    	"query": {
    		"match": {
    			"_all": "python web"
    		}
    	}
    }
    '
    ```

* 短语搜索 match_phrase

    * 如果关键词为'python web'， es在检索时要求数据的字段中必须完整包含"python web" (对关键词不再分词处理)

    ```
    curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
    {
    	"_source": ["article_id", "title"],
    	"query": {
    		"match_phrase": {
    			"_all": "python web"
    		}
    	}
    }
    '
    ```

* 精确查找 term

    ```
    curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
    {
    	"_source": ["article_id", "title"],
    	"query": {
    		"term": {
    			"user_id": 1
    		}
    	}
    }
    '
    ```

* 范围查找 range

    ```
    curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
    {
    	"_source": ["article_id", "title"],
    	"query": {
    		"range": {
    			"article_id": {
    				"gte": 3,
    				"lte": 20
    			}
    		}
    	}
    }
    '
    ```

    * gte     greater than equal  大于等于
    * lte  less than equal 小于等于
    * gt   greater than 大于
    * lt  less than  小于

* 高亮搜索 highlight

    针对全文检索，会将结果中出现了关键词的部分 ”高亮“展示  （突出标识  `<em>`）

    ```
     curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
      {
          "size":2,
          "_source": ["article_id", "title", "user_id"],
          "query": {
              "match": {
                   "title": "python web 编程"
               }
           },
           "highlight":{
                "fields": {
                    "title": {}
                }
           }
      }
      '
    ```

* 组合查询

    - must

        文档 *必须* 匹配这些条件才能被包含进来。

    - must_not

        文档 *必须不* 匹配这些条件才能被包含进来。

    - should

        如果满足这些语句中的任意语句，将增加 `_score` ，否则，无任何影响。它们主要用于修正每个文档的相关性得分。

    - filter

        *必须* 匹配，但它以不评分、过滤模式来进行。这些语句对评分没有贡献，只是根据过滤标准来排除或包含文档。

```
# 例子
curl -X 127.0.0.1:9200/articles/article/_search?pretty -d '
{
	"query": {
		"bool": {
			"must": {
				"match": {
					"_all": "python web"
				}
			},
			"must_not": {
				"term": {
					"user_id": 1
				}
			},
			"should": {
				"match": {
					"title": "python ai"
				}
			},
			"filter": {
				"term": {
					"status": 2
				}
			}
		}
	}
}
'

# 头条项目查询案例
curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
{
	"_source": ["article_id"],
	"query": {
		"bool": {
			"must": {
				"match": {
					"_all": "python ai"
				}
			},
			"filter": {
				"term": {
					"status": 2
				}
			}
		}
	}
}
'

```

* 排序

    * es中默认对于结果使用相关性分数 进行排序

    * 按照自己的字段排序

        ```
          curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
          {
              "size": 5,
              "_source": ["article_id","title"],
              "query" : {
                  "match" : {
                      "_all" : "python web"
                  }
              },
              "sort": [
                  { "create_time":  { "order": "desc" }},
                  { "_score": { "order": "desc" }}
              ]
          }'
        ```

    * 还是根据相关性分数排序，但是想要调整相关性分数的计算结果

        * 在定义类型表结构映射的时候，通过设置字段的boost参数，来将匹配这个字段的结果的分数提升，排名靠前

        * 在查询条件中 声明哪个字段的boost加速，提升权重，提升分数

            ```shell
              curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
              {
                  "size": 5,
                  "_source": ["article_id","title"],
                  "query" : {
                      "match" : {
                          "title" : {
                              "query": "python web",
                              "boost": 4
                          },
                          "content": "python web"
                      }
                  }
              }'
            ```

### 13 Python 中原生使用ES

#### 安装

```shell
pip install elasticsearch
```

#### 使用

```
from elasticsearch5 import Elasticsearch

# elasticsearch集群服务器的地址
ES = [
    '127.0.0.1:9200'
]

# 创建elasticsearch客户端
es = Elasticsearch(
    ES,
    # 启动前嗅探es集群服务器
    sniff_on_start=True,
    # es集群服务器结点连接异常时是否刷新es结点信息
    sniff_on_connection_fail=True,
    # 每60秒刷新结点信息
    sniffer_timeout=60
)


# 搜索
es.search(index=索引库, doc_type=类型表, body=查询条件)  # body就是按照原生REST API编写json字符串格式一样 来定义字典即可
```



### 14 头条项目搜索业务

#### 14.1 用户输入完关键词 点击确定之后 进行检索查询

```
GET /search?q=用户输入的关键词&page=xxx&per_page=xxx

返回值json
{
	"message": "OK",
	"data": {
		"total_count": xxx,
		"page": xxx,
		"per_page": xxx,
		"results": [
			{
				"article_id": xx,
				"title": xx,
				"author_name": xx,
				"author_id": xx,
				"cover": xxx,
				...
			},
			{
			
			},
			...
		]
	}
}
```

#### 14.2 自动补全提示搜索业务

* 拼写纠错建议查询

    * 考虑到用户输入的关键词 都可能是以文章查询为目的，进行拼写纠错时 数据基础以我们数据库中拥有的文章数据作为基础，文章数据中出现了哪些词，我们就能对用户输入的相关词进行拼写建议
    * 头条项目中 不再单独建索引库，直接使用文章的索引库即可

    ````
    pyhton 
    -> python
    ````

    ```
    curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
    {
        "_source": false,
        "suggest": {
            "text": "phtyon web",
            "word-phrase": {   # 自己定义的 用于获取查询结果的
                "phrase": {
                    "field": "_all",
                    "size": 1
                }
            }
        }
    }'
    ```

    ```
    {
      "took" : 218,
      "timed_out" : false,
      "_shards" : {
        "total" : 3,
        "successful" : 3,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : 0,
        "max_score" : 0.0,
        "hits" : [ ]
      },
      "suggest" : {
        "word-phrase" : [
          {
            "text" : "phtyon web",
            "offset" : 0,
            "length" : 10,
            "options" : [
              {
                "text" : "python web",
                "score" : 0.0011466473
              }
            ]
          }
        ]
      }
    }
    ```

* 补全提示建议查询

```
pyt
-> python
python 
-> python web 开发
```

因为补全提示建议查询的库 基础数据的字段类型必须是completion ，不是一般的字符串或者整型，所以之前建立的索引库不能继续使用，需要单独建库

```
curl -X PUT 127.0.0.1:9200/completions -H 'Content-Type: application/json' -d'
{
   "settings" : {
       "index": {
           "number_of_shards" : 3,
           "number_of_replicas" : 1
       }
   }
}
'

curl -X PUT 127.0.0.1:9200/completions/_mapping/words -H 'Content-Type: application/json' -d'
{
     "words": {
          "properties": {
              "suggest": {    # 字段
                  "type": "completion",  # 字段类型是completion 才能提供补全提示
                  "analyzer": "ik_max_word"
              }
          }
     }
}
'
```

头条产品考虑 用户输入的关键词 假定为文章标题，我们数据库中有大量的文章标题数据，可以对用户提供文章标题 补全提示的建议，所以 新库中的数据 我们导入文章标题

使用logstash工具导入数据

```
input{
     jdbc {
         jdbc_driver_library => "/home/python/mysql-connector-java-8.0.13/mysql-connector-java-8.0.13.jar"
         jdbc_driver_class => "com.mysql.jdbc.Driver"
         jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/toutiao?tinyInt1isBit=false"
         jdbc_user => "root"
         jdbc_password => "mysql"
         jdbc_paging_enabled => "true"
         jdbc_page_size => "1000"
         jdbc_default_timezone =>"Asia/Shanghai"
         # 查询mysql中的文章标题保存到es库中的suggest字段
         statement => "select title as suggest from news_article_basic"
         clean_run => true
     }
}
output{
      elasticsearch {
         hosts => "127.0.0.1:9200"
         index => "completions"
         document_type => "words"
      }
}
```

ES 补全建议的语法

```
curl -X GET 127.0.0.1:9200/completions/words/_search?pretty -d '
{
    "suggest": {  # 建议查询的关键词
        "title-suggest" : {  # 自己起名 用于获取结果
            "prefix" : "pyth",   # 用户输入的需要补全的关键词
            "completion" : {   # 补全建议
                "field" : "suggest"   # 从当前表中的哪个字段（suggest)提供补全建议
            }
        }
    }
}
'



# 结果
{
  "took" : 51,
  "timed_out" : false,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 0,
    "max_score" : 0.0,
    "hits" : [ ]
  },
  "suggest" : {
    "title-suggest" : [
      {
        "text" : "pyth",
        "offset" : 0,
        "length" : 4,
        "options" : [
          {
            "text" : "Python 大神 kennethreitz 又搞事了",
            "_index" : "completions",
            "_type" : "words",
            "_id" : "AWxz6qpyDpgo9OgmVNlN",
            "_score" : 1.0,
            "_source" : {
              "@version" : "1",
              "@timestamp" : "2019-08-09T01:07:28.425Z",
              "suggest" : "Python 大神 kennethreitz 又搞事了"
            }
          },
```

#### 用户输入提示功能 业务实现思路：

* 首先假定用户拼写没有错，进行 补全提示建议查询
* 如果查询有结果，将结果返回
* 如果查询没有结果，表示用户可能拼写出错，尝试进行拼写纠错建议查询
* 将拼写建议查询结果返回

```
GET /suggest?q=用户输入的部分

返回json
{
	"message": "OK",
	"data": {
		"options": [
			"建议1",
			"建议2",
			...
		]
	}
}
```















