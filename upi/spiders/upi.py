import json
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

sys.path.append("../../")
from items.MongoDBItems import MediaItem
from items.MongoDBItems import ReporterItem
from items.MongoDBItems import NewsItem


# 定义下载新闻分类的种子
def seed():
    return [
        # 置顶新闻
        'https://www.upi.com/Top_News/p1',
    ]


class Spider(scrapy.Spider):
    name = 'upi'
    allowed_domains = ['www.upi.com']
    start_urls = seed()

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))

        # 泛查询
        for link in LinkExtractor(restrict_css='body').extract_links(response):
            url = link.url
            if '_News' in url.split('www.upi.com')[-1] and '20' in url.split('www.upi.com')[-1]:
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-2]
        newsItem['news_title'] = response.css('title::text').extract_first()
        constents = response.css('p::text').extract()
        newsItem['news_content'] = ''
        for constent in constents:
            constent = constent.strip()
            newsItem['news_content'] += " " + constent
        newsItem['news_publish_time'] = response.css('div.article-date::text').extract_first().strip()
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []
        newsItem['media_id'] = 7
        newsItem['media_name'] = self.name
        newsItem['reporter_list'] = []

        # 记者详情页面
        reporter_links = LinkExtractor(restrict_css='div.author-social a').extract_links(response)
        if reporter_links and len(reporter_links):
            for reporter_link in reporter_links:
                url = reporter_link.url
                if 'author' in url:
                    yield scrapy.Request(url, callback=self.reporter, priority=10)
                    newsItem['reporter_list'] = [{
                        'reporter_name': reporter_link.text,
                        'reporter_id': response.url.split('/')[-2]
                    }]
                    self.logger.warn("保存新闻信息 %s", response.url)
                    yield newsItem

        # 泛查询
        for link in LinkExtractor(restrict_css='body').extract_links(response):
            url = link.url
            if '_News' in url.split('www.upi.com')[-1] and '20' in url.split('www.upi.com')[-1]:
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def reporter(self, response):
        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = response.url.split('/')[-2]
        reporterItem['reporter_name'] = response.css(
            'div.sections-header > div.category-header > h1::text').extract_first()
        reporterItem['reporter_image'] = None
        reporterItem['reporter_image_url'] = None
        reporterItem['reporter_intro'] = response.css(
            'div.sections-header > div.breadcrumb.l-s-25 > div::text').extract_first()
        reporterItem['reporter_url'] = response.url
        reporterItem['reporter_code_list'] = None
        reporterItem['media_id'] = 7
        reporterItem['media_name'] = self.name
        self.logger.warn("保存作者 %s", response.url)
        yield reporterItem

        # 泛查询
        for link in LinkExtractor(restrict_css='body').extract_links(response):
            url = link.url
            if '_News' in url.split('www.upi.com')[-1] and '20' in url.split('www.upi.com')[-1]:
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)
