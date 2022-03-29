# 数据库设计 (media)

## 数据库访问

```text
host: 39.107.26.235
port: 27017
database: media
mongo user: root
password  : aini1314
```

## 数据表设计

### 数据表 media （媒体机构 24+）

| 字段名称 | 字段含义   | 字段说明 |
| ----|--------|----|
| media_id | 媒体机构编号 | 主键 |
| media_name_cn | 媒体机构中文名称 |    |
| media_name_en | 媒体机构英文缩写 |    |

### 数据表 news 新闻报道

| 字段名称 | 字段含义 | 字段说明       |
| ----|--------|------------|
| media_id | 媒体机构编号 | 主键         |
| news_id | 新闻编号 | 主键         |
| news_title | 新闻标题 |            |
| news_title_cn | 中文新闻标题 |            |
| news_content | 新闻内容 |            |
| news_content_cn | 中文新闻内容 |            |
| news_publish_time | 新闻发布时间 |            |
| news_url | 新闻详情页地址 |            |
| news_pdf | 新闻详情原文对应的pdf名称 |            |
| news_pdf_cn | 新闻详情中文对应的pdf名称 |            |
| reporter_list | 记者列表 | [reporter] |
| media_name | 媒体英文名称 |            |

### 数据表 reporter 记者信息

| 字段名称 | 字段含义   | 字段说明                                        |
| ----|--------|---------------------------------------------|
| media_id | 媒体机构编号 | 主键                                          |
| reporter_id | 记者编号   | 主键                                          |
| reporter_name | 记者名称   |                                             |
| reporter_image | 记者图片名称 | 媒体英文名称_内部编号                                 |
| reporter_image_url | 记者图片地址 |                                             |
| reporter_intro | 记者简介   |                                             |
| reporter_url | 记者详情地址 |                                             |
| reporter_code_list | 记者mz列表 | [{ code_content:"13423334", code_type:"phone"}] |
| media_name | 媒体英文名称 | kbs voa                                     |

### 数据表 social_dynamics 社交动态信息

| 字段名称                     | 字段含义   | 字段说明 |
|--------------------------|--------|----|
| media_id                 | 媒体机构编号 | 主键       |
| reporter_id              | 记者编号   | 主键        |
| dynamics_id              | 社交动态编号 | 主键        |
| dynamics_url             | 社交动态地址 |         |
| dynamics_publish_time    | 发布时间   |          |
| dynamics_content         | 动态内容   |          |
| dynamics_content_cn      | 中文动态内容 |          |
| dynamics_favourite_count | 点赞喜欢人数 |          |
| dynamics_keywords        | 关键字    |          |
| dynamics_keyword_cn      | 中文关键字  |          |
| dynamics_image_list      | 动态图片列表 |          |
| social_media_type        | 社交账号类别 |          |
| reporter_name            | 记者名称   |          |
| media_name | 媒体名称   |  |
