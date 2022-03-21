import scrapy
from scrapy.linkextractors import LinkExtractor

import sys
sys.path.append("../../")    # ..是上一级目录
from items.MongoDBItems import MediaItem


# 定义下载新闻分类的种子
def seed():
    return [
        'https://www.voanews.com/z/6715',
    ]


class MediaSpider(scrapy.Spider):
    name = 'nbc'
    start_urls = seed()

    def parse(self, response):
        yield {"id": "123", "age": "12", "name": "zhaotx"}