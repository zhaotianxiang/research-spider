import scrapy


class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['us.cnn.com']
    start_urls = ['http://us.cnn.com/']

    def parse(self, response):
        pass
