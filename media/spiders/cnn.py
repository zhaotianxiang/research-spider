import datetime
import json
import re
import scrapy
import time
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import NewsItem
from ..items import ReporterItem


class Spider(scrapy.Spider):
    id = 16
    name = 'cnn'
    media_name = 'CNN'
    allowed_domains = ['us.cnn.com']
    start_urls = ['https://us.cnn.com/specials/profiles',
                  'https://us.cnn.com/specials/tv/anchors-and-reporters',
                  'https://us.cnn.com/specials/more/cnn-leadership']

    def parse(self, response):
        for link in LinkExtractor(restrict_css='body', allow=['https://us.cnn.com/profiles/']).extract_links(response):
            yield scrapy.Request(link.url, callback=self.reporter)

    def reporter(self, response):
        reporter = ReporterItem()
        reporter["reporter_id"] = response.url.split('/')[-1]
        reporter["reporter_name"] = response.css("div.cd_profile-headline > div.cd__profile-name::text").extract_first()
        reporter["reporter_intro"] = "\n".join(
            response.css("article.cd div.cd__description--wrapper > div.cd__description *::text").extract()).strip()
        reporter["reporter_code_list"] = []
        reporter["reporter_url"] = response.url
        if response.css("div.pg__background__image_wrapper > img::attr(data-src-medium)").extract_first():
            reporter["reporter_image_url"] = "https:" + response.css(
                "div.pg__background__image_wrapper > img::attr(data-src-medium)").extract_first()
            reporter["reporter_image"] = "%s_%s.jpg" % (self.name, reporter["reporter_id"])
        for link in LinkExtractor(restrict_css='div.social-description__follow-links').extract_links(response):
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

        for link in LinkExtractor(restrict_css='body',
                                  allow=[r'https://us.cnn.com/\d{4}/\d{2}/\d{2}/']).extract_links(response):
            yield scrapy.Request(link.url, meta={"reporter": reporter}, callback=self.news)

    def news(self, response):
        reporter = response.meta['reporter']

        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-2]
        newsItem['news_title'] = response.css("meta[property=og\:title]::attr(content)").extract_first().strip()
        newsItem['news_keywords'] = response.css("meta[name=keywords]::attr(content)").extract_first().strip()
        newsItem['news_content'] = response.css("meta[name=description]::attr(content)").extract_first().strip()
        newsItem['news_content_cn'] = None
        newsItem['news_title_cn'] = None
        published_time = response.css("meta[property=og\:pubdate]::attr(content)").extract_first()
        if not published_time:
            response_json = json.loads(response.css("script[type=application\/ld\+json]::text").extract_first())
            if "dateCreated" in response_json:
                published_time = response_json["dateCreated"]
            if "uploadDate" in response_json:
                published_time = response_json["uploadDate"]
        newsItem['news_publish_time'] = datetime.datetime.strptime(published_time,
                                                                   "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = [reporter]
        yield newsItem
