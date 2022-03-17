from scrapy.item import Item, Field


class MediaItem(Item):
    _id = Field()
    media_name_en = Field()
    media_name_cn = Field()
    media_type = Field()


class NewsItem(Item):
    _id = Field()
    news_id = Field()
    news_title = Field()
    news_title_cn = Field()
    news_content = Field()
    news_content_cn = Field()
    news_publish_time = Field()
    news_url = Field()
    news_pdf = Field()  # （新闻标题_媒体编号_新闻编号.pdf）
    news_pdf_cn = Field()  # （新闻标题_媒体编号_新闻编号_cn.pdf）
    reporter_list = Field()
    media_id = Field()


class NewsItem(Item):
    _id = Field()
    news_id = Field()
    news_title = Field()
    news_title_cn = Field()
    news_content = Field()
    news_content_cn = Field()
    news_publish_time = Field()
    news_url = Field()
    news_pdf = Field()  # （新闻标题_媒体编号_新闻编号.pdf）
    news_pdf_cn = Field()  # （新闻标题_媒体编号_新闻编号_cn.pdf）
    reporter_list = Field()
    media_id = Field()
