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


# 大纪元
class Spider(scrapy.Spider):
    id = 20
    name = 'epochtimes'
    allowed_domains = ['www.epochtimes.com']
    start_urls = ['https://www.epochtimes.com/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url.replace('featureFlag=false', '')
            if re.search('https://www.epochtimes.com/gb/\d{2}/\d{1,2}/\d{1,2}/n', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1].replace('.htm', '')
        newsItem['news_title'] = response.css("h1.title::text").extract_first().strip()
        newsItem['news_title_cn'] = newsItem['news_title']
        content = response.css("div.whitebg > *::text").extract()
        if not content:
            content = response.css("div#artbody > *::text").extract()
        newsItem['news_content'] = " ".join(content).replace("\n", ' ').strip()
        newsItem['news_content_cn'] = newsItem['news_content']
        publish_time = response.css("time::attr(datetime)").extract_first()
        newsItem['news_publish_time'] = datetime.datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%S%z") \
            .strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []

        search_result1 = re.findall(r'(?<=大纪元记者).{2,10}(?=[报|)|@|#])', newsItem['news_content'])
        for reporter_name1 in search_result1:
            reporterItem1 = ReporterItem()
            reporterItem1['reporter_id'] = reporter_name1.strip().replace("综合","")
            reporterItem1['reporter_name'] = reporterItem1['reporter_id']
            reporterItem1['reporter_intro'] = '大纪元记者'
            newsItem['reporter_list'].append(reporterItem1)
            yield reporterItem1
        search_result2 = re.findall(r'(?<=责任编辑：).{2,5}(?=[)|@|#|\s|◇])$', newsItem['news_content'])
        for reporter_name2 in search_result2:
            reporterItem2 = ReporterItem()
            reporterItem2['reporter_id'] = reporter_name2.strip().replace("综合","")
            reporterItem2['reporter_name'] = reporterItem2['reporter_id']
            reporterItem2['reporter_intro'] = '责任编辑'
            newsItem['reporter_list'].append(reporterItem2)
            yield reporterItem2
        yield newsItem

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url.replace('featureFlag=false', '')
            if re.search('https://www.epochtimes.com/gb/\d{2}/\d{1,2}/\d{1,2}/n', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)
