# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DomainsearchItem(scrapy.Item):
    # define the fields for your item here like:
    domain = scrapy.Field()
    subdomain = scrapy.Field()
    url = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()