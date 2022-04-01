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


# 定义下载新闻分类的种子
def seed():
    return [
        'https://cn.reuters.com/news/archive/topic-cn-top-news?view=page&page=1&pageSize=10',
    ]


class Spider(scrapy.Spider):
    id = 6
    name = 'reuters_cn'
    start_urls = seed()

    def parse(self, response):
        news_links = LinkExtractor(restrict_css='#blogStyleNews > section > div > article').extract_links(response)
        for link in news_links:
            yield scrapy.Request(link.url, callback=self.parse_news)
        self.logger.info("URL %s 共 %s 条新闻", response.url, len(news_links))
        next_links = LinkExtractor(restrict_css='#content a.control-nav-next').extract_links(response)
        if next_links and len(next_links) == 1:
            for next_link in next_links:
                yield scrapy.Request(next_link.url)

    def parse_news(self, response):
        news_detail = json.loads(re.findall(r'(?<=json">)\{.*?\}(?=<)', response.text)[0])
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1].split('-')[-1].replace('^id', '')
        newsItem['news_title'] = response.css('h1.Headline-headline-2FXIq::text').extract_first()
        newsItem['news_title_cn'] = newsItem['news_title']
        newsItem['news_content'] = " ".join(response.css('div.ArticleBodyWrapper > p::text').extract())
        author_describe = response.css(
            'div.ArticleBodyWrapper div.Attribution-attribution-Y5JpY > p::text').extract_first()
        newsItem['news_content'] += "\n" + author_describe
        newsItem['news_content_cn'] = newsItem['news_content']
        newsItem['news_publish_time'] = news_detail['datePublished'].replace('Z', '')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['reporter_list'] = []
        newsItem['media_id'] = self.id
        newsItem['media_name'] = 'reuters'

        if author_describe:
            author_list = author_describe.split('；')
            if author_list and len(author_list):
                for authors in author_list:
                    for author in authors.split(" ")[1].split('/'):
                        reporterItem = ReporterItem()
                        reporterItem['reporter_id'] = author
                        reporterItem['reporter_name'] = author
                        reporterItem['reporter_image'] = None
                        reporterItem['reporter_image_url'] = None
                        reporterItem['reporter_intro'] = authors.split(" ")[0]
                        reporterItem['reporter_url'] = None
                        reporterItem['media_id'] = self.id
                        reporterItem['media_name'] = 'reuters'
                        newsItem['reporter_list'].append(reporterItem)
                        yield reporterItem
        yield newsItem
