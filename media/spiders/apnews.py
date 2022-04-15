import json
import re
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import MediaItem
from ..items import NewsItem
from ..items import ReporterItem


class Spider(scrapy.Spider):
    id = 8
    name = 'apnews'
    allowed_domains = ['apnews.com']
    start_urls = ['https://apnews.com/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('^https://apnews.com/article', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        # 解析详情页
        response_json = json.loads(re.findall(r'(?<=ld\+json">){.*?}(?=</script)', response.text)[0])
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1]
        newsItem['news_title'] = response_json["headline"]
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css("div.Article *::text").extract())
        if len(newsItem['news_content']) < 5:
            newsItem['news_content'] = " ".join(response.css("div.Body > div > article *::text").extract())

        newsItem['news_content_cn'] = None
        publish_time = response_json["datePublished"]
        newsItem['news_publish_time'] = datetime.datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%S%z").strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []

        for reporter_name_str in response_json["author"]:
            reporter_name_list = reporter_name_str.strip().replace("^By ", "")
            for reporter_list2 in reporter_name_list.split(','):
                for reporter_name in reporter_list2.split('And'):
                    reporter_name = reporter_name.strip()
                    reporter_id = reporter_name
                    reporterItem = ReporterItem()
                    reporterItem['reporter_id'] = reporter_id
                    reporterItem['reporter_name'] = reporter_name
                    newsItem['reporter_list'].append(reporterItem)
                    yield reporterItem
        self.logger.warn("保存新闻和记者信息 %s", response.url)
        if len(newsItem['reporter_list']) == 0:
            yield None
        yield newsItem
