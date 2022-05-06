import datetime
import json
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import NewsItem
from ..items import ReporterItem


def get_content(content):
    if content.get("content"):
        return content["content"]
    return ""


class Spider(scrapy.Spider):
    id = 6
    name = 'reuters'
    media_name = 'Reuters'
    allow_domains = ['www.reuters.com', 'cn.reuters.com', ]
    start_urls = ['https://www.reuters.com/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))

        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allow_domains).extract_links(response):
            if re.search('reuters.com/.*?\d{2,4}-\d{2}-\d{2}/', link.url):
                yield scrapy.Request(link.url, callback=self.news)
            else:
                yield scrapy.Request(link.url)

    def news(self, response):
        response_json = json.loads(response.css("script[type=application\/ld\+json]::text").extract_first().strip())
        global_content = json.loads(re.findall(r'(?<=globalContent=){.*?}(?=;)', response.text)[0])
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-2]
        newsItem['news_title'] = response_json['headline']
        newsItem['news_keywords'] = response.css("meta[name=article\:tag]::attr(content)").extract_first().strip()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "\n".join(list(map(get_content, global_content["result"]["content_elements"])))
        newsItem['news_content_cn'] = None
        newsItem['news_publish_time'] = datetime.datetime.strptime(response_json["datePublished"][0:19],
                                                                   "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []

        for author in global_content["result"]["authors"]:
            reporterItem = ReporterItem()
            if author.get('id'):
                reporterItem['reporter_id'] = author['id']
            else:
                reporterItem['reporter_id'] = author['name']
            reporterItem['reporter_name'] = author['name']
            reporterItem['reporter_code_list'] = []
            if author.get('social_links'):
                for social in author["social_links"]:
                    reporterItem['reporter_code_list'].append({
                        "code_type": social["site"],
                        "code_content": social["url"].replace('mailto:', '')
                    })
            reporterItem['reporter_intro'] = author.get('description')
            reporterItem['reporter_url'] = response.urljoin(author["topic_url"])
            reporterItem['media_id'] = self.id
            reporterItem['media_name'] = 'reuters'
            newsItem['reporter_list'].append(reporterItem)
            # 进入作者详情页面
            yield scrapy.Request(url=reporterItem['reporter_url'],
                                 meta={"reporterItem": reporterItem, "news_url": newsItem['news_url']},
                                 callback=self.reporter)
        yield newsItem

    def reporter(self, response):
        # 能补充获取头像 作者简介
        reporterItem = response.meta["reporterItem"].copy()
        response_json = None
        try:
            response_json = json.loads(re.findall(r'(?<=globalContent=){.*?}(?=;)', response.text)[0])
        except:
            pass
        if response_json:
            author = response_json["result"]["topics"][0]
            reporterItem["reporter_image_url"] = author['thumbnail']['url']
            reporterItem['reporter_image'] = f"reuters_{reporterItem['reporter_id']}.jpg"
            if author.get('description'):
                reporterItem["reporter_intro"] = author['description']
        yield reporterItem

        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allow_domains).extract_links(response):
            if re.search('reuters.com/.*?\d{2,4}-\d{2}-\d{2}/', link.url):
                yield scrapy.Request(link.url, callback=self.news)
            else:
                yield scrapy.Request(link.url)
