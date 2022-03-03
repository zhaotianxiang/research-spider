# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaspiderItem(scrapy.Item):
    news_id=scrapy.Field()
    news_title=scrapy.Field()
    news_contents=scrapy.Field()
    broad_time=scrapy.Field()
    reporter_id = scrapy.Field()
    reporter_name = scrapy.Field()
    reporter_email=scrapy.Field()
    reporter_twitter=scrapy.Field()
    reporter_facebook=scrapy.Field()
    reporter_job_name=scrapy.Field()
    reporter_image_url = scrapy.Field()
