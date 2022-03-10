# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class AsahiItem(scrapy.Item):

    url = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    reporter = scrapy.Field()
    broad_datetime = scrapy.Field()
    content = scrapy.Field()


class AsahiReporterItem(scrapy.Item):

    url = scrapy.Field()
    name = scrapy.Field()
    department = scrapy.Field()
    twitter = scrapy.Field()
    facebook = scrapy.Field()
    introduction = scrapy.Field()