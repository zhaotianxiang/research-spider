import scrapy


class DownfilesItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    files = scrapy.Field()
    file_name = scrapy.Field()
