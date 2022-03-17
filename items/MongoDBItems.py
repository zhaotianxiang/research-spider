from scrapy.item import Item, Field


class MediaItem(Item):
    media_id = Field()
    media_name_en = Field()
    media_name_cn = Field()
    media_content_type = Field()
    media_official_website = Field()


class NewsItem(Item):
    news_id = Field()
    news_title = Field()
    news_title_cn = Field()
    news_content = Field()
    news_content_cn = Field()
    news_publish_time = Field()
    news_url = Field()
    news_pdf = Field()  # （媒体名称_新闻编号.pdf）
    news_pdf_cn = Field()  # （媒体名称_新闻编号_cn.pdf）
    reporter_list = Field()
    media_id = Field()
    media_name = Field()


class ReporterItem(Item):
    reporter_id = Field()  # (社交媒体编号_人员内部编号) (_id)
    reporter_name = Field()
    reporter_image = Field()  # (媒体名称_人员名称_人员内部编号.[jpg|png|jpeg])
    reporter_image_url = Field()
    reporter_intro = Field()
    reporter_url = Field()
    reporter_code_list = Field()  # [{ code_content:"tiaasxgmail.com", code_type:"email"}]
    media_id = Field()
    media_name = Field()


class SocialDynamicsItem(Item):
    dynamics_id = Field()  # 社交媒体类型+社交动态内部编号 (_id)
    dynamics_publish_time = Field()
    dynamics_content = Field()
    dynamics_content_cn = Field()
    dynamics_favourite_count = Field()
    dynamics_keywords = Field()
    dynamics_keyword_cn = Field()
    dynamics_image_list = Field()  # { image_name:"xxx.jpg", image_url:"..."}
    social_media_id = Field()
    social_media_type = Field()
    reporter_id = Field()
    reporter_name = Field()
