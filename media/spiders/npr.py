import datetime
import json
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import NewsItem
from ..items import ReporterItem


class Spider(scrapy.Spider):
    id = 24
    name = 'npr'
    media_name = 'NPR'
    allowed_domains = ['www.npr.org']
    start_urls = ['https://www.npr.org/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('\d{4}/\d{2}/\d{2}/', url):
                yield scrapy.Request(url, callback=self.news)
            elif re.search('https://www.npr.org/people', url):
                yield scrapy.Request(url, callback=self.reporter)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        # 解析详情页
        response_json = json.loads(response.css("script[type=application\/ld\+json]::text").extract_first().strip())
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-2]
        newsItem['news_title'] = response.css('div.storytitle > h1::text').extract_first()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css("div#storytext p *::text").extract()).replace('\n', '').replace(
            '  ', '')
        newsItem['news_content_cn'] = None
        newsItem['news_publish_time'] = datetime.datetime.strptime(response_json["datePublished"],
                                                                   "%Y-%m-%dT%H:%M:%S%z") \
            .strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []
        reporter_links = LinkExtractor(restrict_css='div.byline-container--block > div.byline > p > a').extract_links(
            response)

        for reporter_link in reporter_links:
            reporter_id = reporter_link.url.split('/')[-2]
            reporter_name = reporter_link.text.strip()
            newsItem['reporter_list'].append(
                {'reporter_id': reporter_id, 'reporter_name': reporter_name, 'reporter_url': reporter_link.url})
        self.logger.warn("保存新闻信息 %s", response.url)
        yield newsItem

        for reporter in newsItem['reporter_list']:
            yield scrapy.Request(reporter['reporter_url'], callback=self.reporter)
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('\d{4}/\d{2}/\d{2}/', url):
                yield scrapy.Request(url, callback=self.news)
            elif re.search('https://www.npr.org/people', url):
                yield scrapy.Request(url, callback=self.reporter)
            else:
                yield scrapy.Request(url)

    def reporter(self, response):
        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = response.url.split('/')[-2]
        reporterItem['reporter_name'] = response.css("meta[property=og\:title]::attr(content)").extract_first().strip()
        content_sub_title = response.css('div.articleTop h2.contentsubtitle::text').extract_first()
        content_content = "".join(response.css('div#storytext *::text').extract()).replace('\n', '')
        if content_sub_title and content_content:
            reporterItem['reporter_intro'] = content_sub_title + content_content
        elif content_sub_title:
            reporterItem['reporter_intro'] = content_sub_title
        elif content_content:
            reporterItem['reporter_intro'] = content_content
        reporterItem['reporter_url'] = response.url

        image_link = response.css('div.imagewrap > picture > img::attr(src)').extract_first()
        if image_link:
            reporterItem['reporter_image'] = f"{self.name}_{reporterItem['reporter_id']}.jpg"
            reporterItem['reporter_image_url'] = response.urljoin(image_link)

        share_data_list = LinkExtractor(restrict_css='#socialHandleLoc').extract_links(response)
        reporterItem['reporter_code_list'] = []
        for link in share_data_list:
            reporterItem['reporter_code_list'].append({'code_content': link.url, 'code_type': link.text.lower()})
        self.logger.warn("保存记者信息 %s", response.url)
        yield reporterItem

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('\d{4}/\d{2}/\d{2}/', url):
                yield scrapy.Request(url, callback=self.news)
            elif re.search('https://www.npr.org/people', url):
                yield scrapy.Request(url, callback=self.reporter)
            else:
                yield scrapy.Request(url)
