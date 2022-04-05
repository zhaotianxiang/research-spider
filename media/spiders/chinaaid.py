import datetime
import json
import re
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import NewsItem
from ..items import ReporterItem


class YanSpider(scrapy.Spider):
    id = 23
    name = 'chinaaid'
    allowed_domains = ['www.chinaaid.net', 'www.voachinese.com']
    start_urls = ['https://www.chinaaid.net/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            if re.search('https://www.chinaaid.net/\d{4}/\d{2}/', link.url):
                yield scrapy.Request(link.url, callback=self.news)
            else:
                yield scrapy.Request(link.url)

    def news(self, response):
        newsItem = NewsItem()
        newsItem['news_id'] = '-'.join(response.url.split('www.chinaaid.net/')[-1]
                                       .split('/')).replace('.html', '').replace('_', '-')
        newsItem['news_title'] = response.css("div.post-outer > h2::text").extract_first().strip()
        newsItem['news_title_cn'] = newsItem['news_title']
        newsItem['news_content'] = "".join(response.css("div.post-entry *::text").extract()).replace("\n", ' ').replace(
            '\xa0', ' ')
        newsItem['news_content_cn'] = newsItem['news_content']
        publish_time = response.css("div.post-outer > span::text").extract_first()
        publish_time_list = publish_time.split('/')
        newsItem['news_publish_time'] = datetime.datetime(int(publish_time_list[2]), int(publish_time_list[0]),
                                                          int(publish_time_list[1])).strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"

        reporter_links = LinkExtractor(restrict_css='div.post-entry > ul').extract_links(response)
        if len(reporter_links) > 0:
            for reporter_link in reporter_links:
                if 'author' in reporter_link.url:
                    reporter_id = reporter_link.url.split('/')[-1].replace('_', '-')
                    reporter_name = reporter_link.text
                    if reporter_id:
                        newsItem['reporter_list'] = [{
                            'reporter_id': reporter_id,
                            'reporter_name': reporter_name
                        }]
                        self.logger.info("发出获取记者信息请求 %s", reporter_link.url)
                        reporterItem = ReporterItem()
                        reporterItem['reporter_id'] = reporter_id
                        reporterItem['reporter_name'] = reporter_name
                        reporterItem['reporter_intro'] = 'voa chinese author'
                        yield reporterItem

        search_result1 = re.findall(r'(?<=对华援助网特约记者).*?(?=报道)', newsItem['news_content'])
        for reporter_name1 in search_result1:
            reporterItem = ReporterItem()
            reporterItem['reporter_id'] = reporter_name1
            reporterItem['reporter_name'] = reporter_name1
            reporterItem['reporter_intro'] = '对华援助网特约记者'
            yield reporterItem
        search_result2 = re.findall(r'(?<=对华援助协会特约通讯员).*?(?=\))', newsItem['news_content'])
        for reporter_name2 in search_result2:
            reporterItem = ReporterItem()
            reporterItem['reporter_id'] = reporter_name2
            reporterItem['reporter_name'] = reporter_name2
            reporterItem['reporter_intro'] = '对华援助网特约记者'
            yield reporterItem
        search_result3 = re.findall(r'(?<=对华援助协会记者).*?(?=\))', newsItem['news_content'])
        for reporter_name3 in search_result3:
            reporterItem = ReporterItem()
            reporterItem['reporter_id'] = reporter_name3
            reporterItem['reporter_name'] = reporter_name3
            reporterItem['reporter_intro'] = '对华援助协会记者'
            yield reporterItem

        yield newsItem

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            if re.search('https://www.chinaaid.net/\d{4}/\d{2}/', link.url):
                yield scrapy.Request(link.url, callback=self.news)
            else:
                yield scrapy.Request(link.url)
