import json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor

from ..items import NewsItem
from ..items import ReporterItem


# 共同通讯社
# 记者数量很少很少
class Spider(scrapy.Spider):
    id = 22
    name = 'kyodo'
    media_name = 'Kyodo'
    allowed_domains = ['english.kyodonews.net', 'china.kyodonews.net', 'www.47news.jp']
    start_urls = ['https://china.kyodonews.net/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('net/news/.*?.html$', url) or re.search('\d{7}.html$', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        if re.search('www.47news.jp', response.url):
            if response.css("script[type=application\/ld\+json]::text").extract_first():
                response_json = json.loads(
                    response.css("script[type=application\/ld\+json]::text").extract_first().strip())
            else:
                return None
        else:
            response_json = \
                json.loads(response.css("script[type=application\/ld\+json]::text").extract_first().strip())[0]

        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1].split('.html')[0]
        newsItem['news_title'] = response.css("meta[property=og\:title]::attr(content)").extract_first().strip()
        newsItem['news_keywords'] = response.css("meta[name=keywords]::attr(content)").extract_first().strip()
        newsItem['news_content'] = response.css("meta[property=og\:description]::attr(content)").extract_first().strip()
        if 'datePublished' in response_json:
            newsItem['news_publish_time'] = response_json["datePublished"]
        else:
            newsItem['news_publish_time'] = response.css("div.writer > span::text").extract_first()
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []
        if re.search("china.kyodonews.net", response.url):
            newsItem['news_title_cn'] = newsItem['news_title']
            newsItem['news_content_cn'] = newsItem['news_content']

        if 'name' in response_json["author"]:
            reporter_name = response_json["author"]["name"].strip()
            reporterItem = ReporterItem()
            reporterItem['reporter_id'] = "-".join(reporter_name.split(" "))
            reporterItem['reporter_name'] = reporter_name
            newsItem['reporter_list'].append(reporterItem)
            yield reporterItem
        yield newsItem
