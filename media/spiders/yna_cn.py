import json
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import datetime

from ..items import NewsItem
from ..items import ReporterItem


class Spider(scrapy.Spider):
    id = 21
    name = 'yna_cn'
    allowed_domains = ['cn.yna.co.kr']
    start_urls = ['https://cn.yna.co.kr/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("%s --- %s 个子页面", response.url, len(links))
        for link in links:
            url = link.url
            # 判断是详情页
            if 'view/ACK' in url.split('cn.yna.co.kr')[-1]:
                yield scrapy.Request(url, priority=10, callback=self.news)

    def news(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, priority=10)

        # 解析详情页
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('cn.yna.co.kr/view/')[-1].split("?")[0]
        newsItem['news_title'] = response.css("#container > section > article > header > h1::text").extract_first()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css(
            "#container > section > article > div.view-body > div.sub-content > div.article-story p::text").extract()).strip()
        newsItem['news_content_cn'] = None
        publish_time = response.css("meta[property=article\:published_time]::attr(content)").extract_first()
        newsItem['news_publish_time'] = datetime.datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%S%z").strftime(
            '%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"yna_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"yna_{newsItem['news_id']}.pdf"
        author_list = response.css(
            "#container > section > article > div.view-body > div.sub-content > div.article-story > div.comp-box.text-group > div.inner p::text").extract()
        newsItem['reporter_list'] = []
        for author in author_list:
            if "@yna.co.kr" in author:
                author_name = author.split("@")[0].strip()
                author_email = author.strip()
                self.logger.warn("抓到记者 %s", author_email)
                reporterItem = ReporterItem()
                reporterItem['reporter_id'] = author_name
                reporterItem['reporter_name'] = author_name
                reporterItem['reporter_code_list'] = [{'code_content': author_email, 'code_type': 'email'}]
                newsItem['reporter_list'].append(reporterItem)
                yield reporterItem
        newsItem['media_id'] = 21
        newsItem['media_name'] = 'yna'
        yield newsItem
