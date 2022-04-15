import datetime
import json
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from ..items import MediaItem
from ..items import ReporterItem
from ..items import NewsItem


class Spider(scrapy.Spider):
    id = 7
    name = 'upi'
    start_urls = ['https://www.upi.com/']
    allowed_domains = ['www.upi.com']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search(r'News.*?20\d{2}/\d{2}/\d{2}/.*?/\d*?/', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        response_json = json.loads(response.css("script[type=application\/ld\+json]::text").extract_first().strip())
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-2]
        newsItem['news_title'] = response_json["headline"]
        newsItem['news_content'] = " ".join(response.css('p::text').extract())
        newsItem['news_publish_time'] = datetime.datetime \
            .strptime(response_json["datePublished"], "%Y-%m-%dT%H:%M:%S%z") \
            .strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []
        if "author" in response_json:
            for reporter in response_json["author"]:
                reporterItem = ReporterItem()
                reporterItem['reporter_id'] = reporter["name"]
                reporterItem['reporter_name'] = "-".join(reporter["name"].split(" "))
                newsItem['reporter_list'].append(reporterItem)
                yield reporterItem
                if "url" in reporter:
                    yield scrapy.Request(reporter["url"], callback=self.reporter, priority=10)
        yield newsItem

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
        yield reporterItem
