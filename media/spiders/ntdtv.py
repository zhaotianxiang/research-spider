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


# 新唐人电视台
class Spider(scrapy.Spider):
    id = 15
    name = 'ntdtv'
    allowed_domains = ['www.ntdtv.com']
    start_urls = ['https://www.ntdtv.com/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url.replace('featureFlag=false', '')
            if re.search('https://www.ntdtv.com/.*?/\d{2,4}/\d{1,2}/\d{1,2}/', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1].replace('.html', '')

        title = response.css("div.article_title > h1::text").extract_first()
        if not title:
            title = response.css("div.title *::text").extract_first()
        newsItem['news_title_cn'] = title.strip()
        content = response.css("div.post_content > *::text").extract()
        newsItem['news_content'] = " ".join(content).replace("\n", ' ').strip()
        newsItem['news_content_cn'] = newsItem['news_content']
        publish_time = response.css("div.article_info > div.time > span::text").extract_first()
        newsItem['news_publish_time'] = datetime.datetime.strptime(publish_time, "%Y-%m-%d %H:%M").strftime(
            '%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []
        search_result1 = re.findall(r'(?<=新唐人記者：).{2,40}(?=採訪報導)', newsItem['news_content'])
        for reporter_name1 in search_result1:
            reporter_name1_list = reporter_name1.split('、')
            for reporter_name in reporter_name1_list:
                reporterItem1 = ReporterItem()
                reporterItem1['reporter_id'] = reporter_name.strip()
                reporterItem1['reporter_name'] = reporter_name
                reporterItem1['reporter_intro'] = '新唐人記者'
                newsItem['reporter_list'].append(reporterItem1)
                yield reporterItem1

        search_result2 = re.findall(r'(?<=記者).{2,10}(?=綜合報導)', newsItem['news_content'])
        for reporter_name1 in search_result2:
            reporter_name1_list = reporter_name1.split('、')
            for reporter_name in reporter_name1_list:
                reporterItem1 = ReporterItem()
                reporterItem1['reporter_id'] = reporter_name.strip()
                reporterItem1['reporter_name'] = reporter_name
                reporterItem1['reporter_intro'] = '新唐人記者'
                newsItem['reporter_list'].append(reporterItem1)
                yield reporterItem1

        search_result3 = re.findall(r'(?<=責任編輯：).{2,10}(?=）)', newsItem['news_content'])
        for reporter_name3 in search_result3:
            reporterItem3 = ReporterItem()
            reporterItem3['reporter_id'] = reporter_name3.strip()
            reporterItem3['reporter_name'] = reporterItem3['reporter_id']
            reporterItem3['reporter_intro'] = '責任編輯'
            newsItem['reporter_list'].append(reporterItem3)
            yield reporterItem3

        search_result5 = re.findall(r'(?<=責任編輯：).{2,10}(?=\))', newsItem['news_content'])
        for reporter_name5 in search_result5:
            reporterItem5 = ReporterItem()
            reporterItem5['reporter_id'] = reporter_name5.strip()
            reporterItem5['reporter_name'] = reporterItem5['reporter_id']
            reporterItem5['reporter_intro'] = reporter_name5
            newsItem['reporter_list'].append(reporterItem5)
            yield reporterItem5

        yield newsItem

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url.replace('featureFlag=false', '')
            if re.search('https://www.ntdtv.com/.*?/\d{2,4}/\d{1,2}/\d{1,2}/', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)
