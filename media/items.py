from scrapy.item import Item, Field


class NewsItem(Item):
    news_id = Field()
    news_title = Field()
    news_title_cn = Field()
    news_content = Field()
    news_content_cn = Field()
    news_publish_time = Field()
    # 新增文章关键字
    news_keywords = Field()
    news_url = Field()
    news_pdf = Field()  # （媒体名称_新闻编号.pdf）
    news_pdf_cn = Field()  # （媒体名称_新闻编号_cn.pdf）
    reporter_list = Field()
    media_id = Field()
    media_name = Field()


class ReporterItem(Item):
    reporter_id = Field()  # (人员内部编号)
    reporter_name = Field()
    reporter_image = Field()  # (媒体名称_人员内部编号.[jpg|png|jpeg])
    reporter_image_url = Field()
    reporter_intro = Field()
    reporter_url = Field()
    reporter_code_list = Field()  # [{ code_content:"tiaasxgmail.com", code_type:"email"}]
    media_id = Field()
    media_name = Field()
