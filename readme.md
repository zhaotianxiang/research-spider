# Reseacrch Spider
  数据调研爬虫
## Getting Start
#### 1. 运行环境
安装 Python3 pip3 运行环境

#### 2. 运行前的准备
安装以下依赖：

```text

pip install -r requirements.txt

```

#### 3. 项目结构说明
项目跟路径下的每一个子项目都是一个自依赖的爬虫程序，都可以单独运行，每一个子项目下面目录说明：

```shell
 -- media                    爬虫项目
   | -- spiders              爬虫程序
   | -- middlewares.py       中间件
   | -- pipelines.py         数据清洗转换管道
   | -- settings.py          项目的配置
```

#### 4. 运行一个子爬虫项目

**选定一个需要运行的子项目meida 下的 cnn 需要如下步骤：**
1. 修改 scrapy.cfg

```python

[settings]
default = media.settings

```

2. 执行

```shell

scrapy crawl cnn

```

#### 5. Scrapy 的详细文档参见：
[Scrapy官方文档](https://docs.scrapy.org/en/latest/)

#### 6. 数据库设计：
[数据表设计](https://github.com/zhaotianxiang/MediaSpider/blob/master/database.md)
