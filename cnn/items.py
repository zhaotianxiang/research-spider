# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CNNReporterItem(scrapy.Item):

    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    code_list = scrapy.Field()
    introduction = scrapy.Field()
