# 路透社

## 分析

1. 翻页地址 
  - 咨讯： https://cn.reuters.com/news/archive/topic-cn-top-news?view=page&page=2&pageSize=10
  - 深度分析： https://cn.reuters.com/news/archive/CNAnalysesNews?view=page&page=2&pageSize=10
  - 实时要闻： https://cn.reuters.com/news/archive/CNTopGenNews?view=page&page=2&pageSize=10
  - 生活   ： https://cn.reuters.com/news/archive/topic-cn-lifestyle?view=page&page=2&pageSize=10
  - 投资   ： https://cn.reuters.com/news/archive/companyNews?view=page&page=2&pageSize=10

2. 国际版本大分类(section_id)有：
  - /word
  - /business
  - /legal
  - /markets


```json
{
    "arc-site": "reuters",
    "called_from_a_component": true,
    "fetch_type": "sophi_or_collection_or_section",
    "offset": 30,
    "section_id": "/world",
    "size": 10,
    "sophi_page": "china",
    "sophi_widget": "topic",
    "website": "reuters"
}

```
3. 运行情况
   1. 中文板块作者信息抽取有脏数据，需要再对多种情况特殊处理
   2. 英文翻页有点奇怪，设置每页 100 条，前5页只显示20条，后面得到基本每页 100 || 99 条，但是数据库中有部分脏数据, 路透社文章挺犀利，但程序是不咋地～
   3. 英文板块只跑了 /word 分类