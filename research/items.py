# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ResearchItem(scrapy.Item):
    搜索关键字 = scrapy.Field()
    联系页面 = scrapy.Field()
    机构名称 = scrapy.Field()
    别名 = scrapy.Field()
    官网 = scrapy.Field()
    邮箱 = scrapy.Field()
    电话 = scrapy.Field()
    传真 = scrapy.Field()
    地址 = scrapy.Field()
    国家地区 = scrapy.Field()
    银行账号 = scrapy.Field()
    微信公众号 = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    instagram = scrapy.Field()
    telegram = scrapy.Field()
    youtube = scrapy.Field()
    linkedin = scrapy.Field()
    备注 = scrapy.Field()

class CodeAddressItem(scrapy.Item):
    官网 = scrapy.Field()
    联系页面 = scrapy.Field()
    邮箱 = scrapy.Field()
    电话 = scrapy.Field()
    传真 = scrapy.Field()
    地址 = scrapy.Field()
    银行账号 = scrapy.Field()
    微信公众号 = scrapy.Field()
    facebook = scrapy.Field()
    twitter = scrapy.Field()
    instagram = scrapy.Field()
    telegram = scrapy.Field()
    youtube = scrapy.Field()
    linkedin = scrapy.Field()
