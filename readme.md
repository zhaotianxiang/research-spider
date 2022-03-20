# Media Spider
  本项目的目的是抓取新闻媒体内容，用于测试自主研发的语言翻译识别程序的准确度，因此在互联网上采集一些新闻媒体信息作为训练集。
## Getting Start
#### 1. 运行环境

  - Python3+
  - scrapy2+
  - Pilliow

#### 2. 运行前的准备
1. 安装 Python3 pip3 运行环境
2. 安装以下依赖：
```shell
pip3 install scrapy
pip3 install pillow
...
```

#### 3. 项目结构说明
项目跟路径下的每一个子项目都是一个自依赖的爬虫程序，都可以单独运行，每一个子项目下面目录说明：

```shell
 -- voa                    爬虫子项目示例
   | -- data               爬虫抓取的数据文件
   | -- spiders            爬虫程序
   | -- 
   | -- middlewares.py     中间件
   | -- pipelines.py       数据清洗转换管道
   | -- settings.py        子项目的配置
```

#### 4. 运行一个子爬虫项目

**选定一个需要运行的子项目如 voa 需要如下步骤：**
  1. 修改根目录下 scrapy.cfg 文件如下
```text

-- scrapy.cfg file
default = voa.settings   # 指定要运行的子项目下的配置文件

```
  2. 在跟路径下执行
```shell

scrapy crawl voa

```

  3. 程序开始执行，结果见子项目下 data 文件

#### 5. Scrapy 的详细文档参见：
[Scrapy官方文档](https://docs.scrapy.org/en/latest/)

#### 6. 任务列表参见：
[任务列表](https://github.com/zhaotianxiang/MediaSpider/blob/master/summary.md)

#### 7. 数据库设计：
[数据表设计](https://github.com/zhaotianxiang/MediaSpider/blob/master/database.md)
