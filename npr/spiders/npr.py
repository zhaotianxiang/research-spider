import json
import re
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
    name = 'npr'
    id = 24
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
            if re.search('^https://www.npr.org/\d{4}/\d{2}/\d{2}/', url):
                yield scrapy.Request(url, callback=self.news)
            elif re.search('https://www.npr.org/people', url):
                yield scrapy.Request(url, callback=self.reporter)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        # 解析详情页
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('www.npr.org/')[-1].split('/')[3]
        newsItem['news_title'] = response.css('div.storytitle > h1::text').extract_first()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css("div#storytext p *::text").extract()).replace('\n', '').replace(
            '          ', '')
        newsItem['news_content_cn'] = None
        newsItem['news_publish_time'] = ''.join(response.url.split('www.npr.org/')[-1].split('/')[0:3])
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['media_id'] = self.id
        newsItem['media_name'] = self.name
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
            if re.search('^https://www.npr.org/\d{4}/\d{2}/\d{2}/', url):
                yield scrapy.Request(url, callback=self.news)
            elif re.search('https://www.npr.org/people', url):
                yield scrapy.Request(url, callback=self.reporter)
            else:
                yield scrapy.Request(url)

    def reporter(self, response):
        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = response.url.split('/')[-2]
        reporterItem['reporter_name'] = response.css("div.storytitle > h1::text").extract_first()
        reporterItem['reporter_image'] = f"{self.name}_{reporterItem['reporter_id']}.jpg"
        reporterItem['reporter_intro'] = "".join(response.css('div.storytext *::text').extract()).replace('\n', '')
        reporterItem['reporter_url'] = response.url

        image_link = response.css('div.imagewrap > picture > img::attr(src)').extract_first()
        reporterItem['reporter_image_url'] = response.urljoin(image_link)

        share_data_list = LinkExtractor(restrict_css='#socialHandleLoc > a').extract_links(response)
        for link in share_data_list:
            if "twitter" in link.url:
                reporterItem['reporter_code_list'] = [{'code_content': link.text, 'code_type': 'twitter'}]
            if "@" in link.url:
                reporterItem['reporter_code_list'] = [{'code_content': link.text, 'code_type': 'email'}]
            if "facebook" in link.url:
                reporterItem['reporter_code_list'] = [{'code_content': link.text, 'code_type': 'facebook'}]
            if "instagram" in link.url:
                reporterItem['reporter_code_list'] = [{'code_content': link.text, 'code_type': 'instagram'}]
            else:
                reporterItem['reporter_code_list'] = [{'code_content': link.text, 'code_type': 'account'}]
        reporterItem['media_id'] = self.id
        reporterItem['media_name'] = self.name
        self.logger.warn("保存记者信息 %s", response.url)
        yield reporterItem

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('^https://www.npr.org/\d{4}/\d{2}/\d{2}/', url):
                yield scrapy.Request(url, callback=self.news)
            elif re.search('https://www.npr.org/people', url):
                yield scrapy.Request(url, callback=self.reporter)
            else:
                yield scrapy.Request(url)
