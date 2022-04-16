import datetime
import json
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import NewsItem
from ..items import ReporterItem


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
                deny=["www.upi.com/News_Photos"],
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
        newsItem['news_keywords'] = response.css("meta[name=keywords]::attr(content)").extract_first().strip()
        newsItem['news_content'] = " ".join(response.css('p::text').extract()).strip()
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
                reporter["name"] = reporter["name"].replace("By ","")
                reporterItem['reporter_id'] = "-".join(reporter["name"].split(" "))
                reporterItem['reporter_name'] = reporter["name"]
                newsItem['reporter_list'].append(reporterItem)
                yield reporterItem
                if "url" in reporter:
                    yield scrapy.Request(reporter["url"], meta={
                        "reporter_name": reporterItem['reporter_name'],
                        "reporter_id": reporterItem['reporter_id'],
                    }, callback=self.reporter, priority=10)
        else:
            result = re.findall(r'(?<=async_config.authors = \').*?(?=\')', response.text)
            if len(result) >= 1 and len(result[0]) > 0:
                author_name = result[0].split(",")[0]
                author_name = author_name.replace("By ","")
                author_id = "-".join(author_name.split(" "))
                reporterItem = ReporterItem()
                reporterItem['reporter_id'] = author_id
                reporterItem['reporter_name'] = author_name
                yield reporterItem
                newsItem['reporter_list'].append(reporterItem)
        yield newsItem

    def reporter(self, response):
        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = response.url.split('/')[-2]
        reporterItem['reporter_name'] = response.meta["reporter_name"]
        reporterItem['reporter_image'] = None
        reporterItem['reporter_image_url'] = None
        reporterItem['reporter_intro'] = response.css(
            'div.sections-header > div.breadcrumb.l-s-25 > div::text').extract_first()
        reporterItem['reporter_url'] = response.url
        reporterItem['reporter_code_list'] = []

        twitter_list = re.findall(r'https://.{0,4}twitter.com/.*?(?=[",\s])', response.text)
        for twitter in twitter_list:
            if re.search('share', twitter):
                continue
            self.logger.info("找到了 twitter %s", twitter)
            twitter = twitter.replace("\"", "").replace(";", "").replace("'", "").strip().split("?")[0]
            reporterItem['reporter_code_list'].append({
                "code_type": "twitter",
                "code_content": twitter,
            })
        yield reporterItem
