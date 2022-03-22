import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re
import json

import sys

sys.path.append("../../")
from items.MongoDBItems import MediaItem
from items.MongoDBItems import ReporterItem
from items.MongoDBItems import NewsItem


# 定义下载新闻分类的种子
def seed():
    return [
        'https://cn.reuters.com/news/archive/topic-cn-top-news?view=page&page=1&pageSize=10',
    ]


class Spider(scrapy.Spider):
    name = 'upi'
    start_urls = seed()

    def parse(self, response):
        news_links = LinkExtractor(restrict_css='#blogStyleNews > section > div > article').extract_links(response)
        for link in news_links:
            yield scrapy.Request(link.url, callback=self.parse_news)
        self.logger.info("URL %s 共 %s 条新闻", response.url, len(news_links))
        next_links = LinkExtractor(restrict_css='#content a.control-nav-next').extract_links(response)
        if next_links and len(next_links) == 1:
            for next_link in next_links:
                yield scrapy.Request(next_link.url)

