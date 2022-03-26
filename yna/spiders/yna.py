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


class YanSpider(scrapy.Spider):
    name = 'yna'
    allowed_domains = ['www.yna.co.kr']
    start_urls = ['https://www.yna.co.kr/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(restrict_css='body').extract_links(response):
            url = link.url
            if 'view/AKR' in url.split('cn.yna.co.kr')[-1]:
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        # 解析详情页
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('www.yna.co.kr/view/')[-1].split("?")[0]
        newsItem['news_title'] = response.css("article header > h1::text").extract_first()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css("article > p::text").extract())
        newsItem['news_content_cn'] = None
        newsItem['news_publish_time'] = newsItem['news_id'][3:11]
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['media_id'] = 21
        newsItem['media_name'] = self.name
        newsItem['reporter_list'] = []
        reporter_links = LinkExtractor(restrict_css='article > div.writer-zone > a').extract_links(response)
        if reporter_links and len(reporter_links) == 1:
            for reporter_link in reporter_links:
                yield scrapy.Request(url=reporter_link.url, meta={'newsItem': newsItem}, callback=self.reporter)

                newsItem['reporter_list'].append({
                    "reporter_name": response.css("a > div > strong::text").extract_first(),
                    "reporter_id": reporter_link.url.split('?id=')[-1]
                })
                self.logger.warn("保存新闻信息 %s", response.url)
                yield newsItem
        # 泛查询
        for link in LinkExtractor(restrict_css='body').extract_links(response):
            url = link.url
            if 'view/AKR' in url.split('cn.yna.co.kr')[-1]:
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def reporter(self, response):
        image_link = response.css('div.area img::attr(src)').extract_first()
        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = response.url.split('?id=')[-1]
        reporterItem['reporter_name'] = response.css(
            "#container > div > div:nth-child(2) > div > div > figure > div > strong::text").extract_first()
        reporterItem['reporter_image'] = f"{self.name}_{reporterItem['reporter_id']}.jpg"
        reporterItem['reporter_intro'] = response.css(
            '#container > div > div:nth-child(2) > div > div > div::text').extract_first()
        reporterItem['reporter_url'] = response.url
        reporterItem['reporter_image_url'] = response.urljoin(image_link)

        share_data_list = response.css('div > a.mail::text').extract()
        for share_data in share_data_list:
            if "@yna.co.kr" in share_data:
                reporterItem['reporter_code_list'] = [{'code_content': share_data.strip(), 'code_type': 'email'}]
        reporterItem['media_id'] = 21
        reporterItem['media_name'] = self.name
        self.logger.warn("保存记者信息 %s", response.url)
        yield reporterItem

        # 泛查询
        for link in LinkExtractor(restrict_css='body').extract_links(response):
            url = link.url
            if 'view/AKR' in url.split('cn.yna.co.kr')[-1]:
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)
