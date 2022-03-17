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

### 1. media
  - media_id (_id)
  - media_name_cn
  - media_name_en
  - media_type   en/ch/jp/ka

### 2. news
  - news_id (_id)
  - news_title
  - news_title_cn
  - news_content
  - news_content_cn
  - news_publish_time
  - news_url
  - news_pdf（新闻标题_媒体编号_新闻编号.pdf）
  - news_pdf_cn（新闻标题_媒体编号_新闻编号_cn.pdf）
  - --------------
  - reporter_list
    - { reporter_id:123, reporter_name:"xxxx"} 
  - media_id

### 3. reporter
  - reporter_id (社交媒体编号_人员内部编号) (_id)
  - reporter_name
  - reporter_image (媒体编号_人员名称_人员内部编号.[jpg|png|jpeg])
  - reporter_image_url
  - reporter_intro
  - reporter_url
  - reporter_code_list:
    - { code_content:"tiaasxgmail.com", code_type:"email"}
    - { code_content:"1523255666222", code_type:"手机"}
    - { code_content:"1234466661233", code_type:"twitter"}
  - --------------
  - media_id
  - media_name

### 4. social_dynamics
  - dynamics_id    社交媒体类型+社交动态内部编号 (_id)
  - dynamics_publish_time
  - dynamics_content
  - dynamics_content_cn
  - dynamics_favourite_count
  - dynamics_keywords
    - string list
  - dynamics_keyword_cn
    - string list
  - dynamics_image_list
    - { image_name:"xxx.jpg", image_url:"..."} 
  - social_media_id
  - social_media_type
  - ---------------
  - reporter_id
  - reporter_name
  