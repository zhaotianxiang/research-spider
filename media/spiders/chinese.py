import datetime
import json

import scrapy
import uuid
from scrapy.linkextractors import LinkExtractor
from ..items import Item

class Spider(scrapy.Spider):
    id = 4
    name = 'chinese'
    allowed_domains = ['www.163.com']
    start_urls = ['https://news.163.com/world','https://news.163.com/domestic/','https://news.163.com/air/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body', allow=["https://www.163.com"]).extract_links(response)
        self.logger.info(links)
        for link in links:
            self.logger.info("成功搜索到 %s", link)
            yield scrapy.Request(link.url, callback=self.news)

    def news(self, response):
        stripped = [s.strip() for s in response.css("#content > div.post_body > p::text").extract()]
        text = "".join(stripped)
        data = {
            'id': str(uuid.uuid1()),
            'text': text,
            'label': ''
        }
        yield data
