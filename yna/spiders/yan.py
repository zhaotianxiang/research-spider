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
    name = 'yan'
    allowed_domains = ['yna.co.kr', 'www.yna.co.kr']
    start_urls = ['https://www.yna.co.kr/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("%s --- %s 个子页面", response.url, len(links))
        # yield scrapy.Request("https://www.yna.co.kr/reporter/index?id=30313839393837", callback=self.reporter)
        for link in links:
            url = link.url
            # 判断是详情页
            if 'view/AKR' in url.split('cn.yna.co.kr')[-1]:
                yield scrapy.Request(url, callback=self.news)

    def news(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("新闻页面 %s %s 页面", response.url, len(links))
        for link in links:
            yield scrapy.Request(link.url)

        # 解析详情页
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('cn.yna.co.kr/view/')[-1].split("?")[0]
        newsItem['news_title'] = response.css("#container > section > article > header > h1::text").extract_first()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css(
            "#container > section > article > div.view-body > div.sub-content > div.article-story p::text").extract())
        newsItem['news_content_cn'] = None
        newsItem['news_publish_time'] = newsItem['news_id'][3:11]
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}.pdf"

        reporter_links = LinkExtractor(
            restrict_css='article > div.writer-zone > a').extract_links(response)
        if reporter_links and len(reporter_links) == 1:
            for reporter_link in reporter_links:
                yield scrapy.Request(url=reporter_link.url, meta={'newsItem': newsItem}, callback=self.reporter)
        else:
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
                    reporterItem['reporter_image'] = None
                    reporterItem['reporter_image_url'] = None
                    reporterItem['reporter_intro'] = None
                    reporterItem['reporter_url'] = None
                    reporterItem['reporter_code_list'] = [{'code_content': author_email, 'code_type': 'email'}]
                    reporterItem['media_id'] = 21
                    reporterItem['media_name'] = self.name
                    newsItem['reporter_list'].append(reporterItem)
                    yield reporterItem
            newsItem['media_id'] = 21
            newsItem['media_name'] = self.name
            yield newsItem

    def reporter(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("记者页面 %s %s 页面", response.url, len(links))
        for link in links:
            yield scrapy.Request(link.url)
        self.logger.warn("抓到了详细的记者 %s", response.url)
        newsItem = response.meta["newsItem"].copy()
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

        share_data_list = response.css('div.share-data.display-none::attr(data-share-body)').extract()
        for share_data in share_data_list:
            if "@yna.co.kr" in share_data:
                reporterItem['reporter_code_list'] = [{'code_content': share_data.strip(), 'code_type': 'email'}]
        reporterItem['media_id'] = 21
        reporterItem['media_name'] = self.name
        yield reporterItem

        newsItem['reporter_list'].append(reporterItem)
        yield newsItem
