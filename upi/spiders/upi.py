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
        # 置顶新闻
        'https://www.upi.com/Top_News/p1',
    ]


class Spider(scrapy.Spider):
    name = 'upi'
    allowed_domains = ['www.upi.com']
    start_urls = seed()

    def parse(self, response):
        news_links = LinkExtractor(
            restrict_css='div.container').extract_links(
            response)
        # 下一页
        next_links = LinkExtractor(restrict_css='#pn_arw a').extract_links(response)
        if next_links and len(next_links) > 0:
            for next_link in next_links:
                if next_link.text == 'Next':
                    yield scrapy.Request(next_link.url)

        for link in news_links:
            yield scrapy.Request(link.url, callback=self.parse_news)
        self.logger.warn("URL %s 共 %s 条新闻", response.url, len(news_links))

    def parse_news(self, response):
        newsItem = NewsItem()
        if not response.css('div.article-date::text').extract_first():
            self.logger.warn("页面不是新闻详情页 %s", response.url)
            reporter_news_links = LinkExtractor(restrict_css='div.container').extract_links(response)
            if reporter_news_links and len(reporter_news_links) > 0:
                self.logger.warn("详情页衍生出来 %s 条新闻", len(reporter_news_links))
                for news_link in reporter_news_links:
                    if 'https://www.upi.com/' in news_link.url and 'Top_News/p' not in news_link.url:
                        yield scrapy.Request(news_link.url, callback=self.parse_news)
        else:
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
            reporter_links = LinkExtractor(restrict_css='div.author-social > div').extract_links(response)
            if reporter_links and len(reporter_links):
                for reporter_link in reporter_links:
                    url = reporter_link.url
                    if 'author' in url:
                        newsItem['reporter_list'].append(
                            {"reporter_name": reporter_link.text, "reporter_id": url.split('/')[-2]})
                        yield scrapy.Request(url, callback=self.parse_reporter)

    def parse_reporter(self, response):
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

        reporter_news_links = LinkExtractor(restrict_css='div.container').extract_links(response)
        if reporter_news_links and len(reporter_news_links) > 0:
            self.logger.warn("作者页衍生出来 %s 条新闻", len(reporter_news_links))
            for news_link in reporter_news_links:
                if 'https://www.upi.com/' in news_link.url and 'Top_News/p' not in news_link.url:
                    yield scrapy.Request(news_link.url, callback=self.parse_news)
        yield reporterItem
