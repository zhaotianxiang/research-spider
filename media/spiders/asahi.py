import datetime
import json

import scrapy
from scrapy.linkextractors import LinkExtractor

from ..items import NewsItem
from ..items import ReporterItem


class Spider(scrapy.Spider):
    id = 4
    name = 'asahi'
    media_name = 'Asahi'
    allowed_domains = ['www.asahi.com']
    start_urls = ['https://www.asahi.com/sns/reporter/']

    def parse(self, response):
        for link in LinkExtractor(
                restrict_css='#MainInner > div.Section.KishaList',
                allow=["https://www.asahi.com/sns/reporter/"]).extract_links(response):
            yield scrapy.Request(link.url, callback=self.reporter)

    def reporter(self, response):
        reporter = ReporterItem()
        reporter["reporter_id"] = response.url.split('/')[-1].replace(".html", "")
        reporter["reporter_name"] = response.css("#Main > div.BreadCrumb > h1::text").extract_first()
        reporter["reporter_intro"] = "\n".join(response.css("div.PlainMod p.TxtSmall::text").extract()).strip()
        reporter["reporter_code_list"] = []
        reporter["reporter_image"] = None
        reporter["reporter_image_url"] = None
        reporter["reporter_url"] = response.url
        for link in LinkExtractor(restrict_css='div.Title').extract_links(response):
            if 'twitter' in link.url:
                reporter["reporter_code_list"].append({
                    "code_type": "twitter",
                    "code_content": link.url,
                })
            if 'facebook' in link.url:
                reporter["reporter_code_list"].append({
                    "code_type": "facebook",
                    "code_content": link.url,
                })
            if 'instagram' in link.url:
                reporter["reporter_code_list"].append({
                    "code_type": "instagram",
                    "code_content": link.url,
                })
            if 'linkedin' in link.url:
                reporter["reporter_code_list"].append({
                    "code_type": "linkedin",
                    "code_content": link.url,
                })
        yield reporter

        for link in LinkExtractor(restrict_css='ul.List',
                                  allow=[r'http://www.asahi.com/articles/']).extract_links(response):
            yield scrapy.Request(link.url, meta={"reporter": reporter}, callback=self.news)

    def news(self, response):
        reporter = response.meta["reporter"]
        response_json = json.loads(response.css("script[type=application\/ld\+json]::text").extract_first().strip())

        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1].replace(".html", "")
        newsItem['news_title'] = response.css("meta[name=TITLE]::attr(content)").extract_first().strip()
        newsItem['news_keywords'] = response.css("meta[name=keywords]::attr(content)").extract_first().strip()
        newsItem['news_content'] = response_json['description']
        newsItem['news_content_cn'] = None
        newsItem['news_title_cn'] = None
        published_time = response_json['datePublished']
        newsItem['news_publish_time'] = datetime.datetime.strptime(published_time,
                                                                   "%Y-%m-%dT%H:%M:%S%z").strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = [reporter]
        yield newsItem
