import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import json


# 定义下载新闻分类的种子
def seed():
    return [
        # news
        'https://www.yomiuri.co.jp/y_ajax/latest_list_news_more/category/2,54,48,47,59,1538,2277,2702,2949,154,194,3005/0/1/50/1939/50/0/'
        # # 社会
        # 'https://www.yomiuri.co.jp/y_ajax/latest_list/category/1524/1/1/20//',
        # # 政治
        # 'https://www.yomiuri.co.jp/y_ajax/latest_list/category/1561/1/1/20//',
        # # 经济
        # 'https://www.yomiuri.co.jp/y_ajax/latest_list/category/41/1/1/20//',
        # # 国际
        # 'https://www.yomiuri.co.jp/y_ajax/latest_list/category/1648/1/1/10//',
        # # 地区
        # 'https://www.yomiuri.co.jp/y_ajax/latest_list/category/455/1/1/20//local/',
    ]

class Youmiui(scrapy.Spider):
    name = 'youmiuri'
    start_urls = seed()

    def parse(self, response):
        response_obj = json.loads(response.body)
        if not response_obj.get("has_next_data"):
            self.logger.error("unexcepted response ", response.url)
            return None
        self.logger.info(response_obj.get("contents"))
        articles = Selector(text=response_obj.get("contents")).xpath('//article')

        for item in articles:
            article = {
                "news_title": item.xpath('./div/h3/a/text()').extract_first(),
                "news_url": item.xpath('./div/h3/a/@href').extract_first(),
                "released_time": item.xpath('./div/div/time/@datetime').extract_first(),
            }
            self.logger.info("articles: %s", article)
        self.logger.info("LIST ---- URL: %s SIZE: %s",response.url, len(articles))
        yield scrapy.Request(url="https://www.yomiuri.co.jp/world/20220307-OYT1T50139/", callback=self.parse_reporter_articles)

    def parse_reporter_articles(self, response):
        self.logger.info("REPORTER'S ARTICLE ---- %s", response.url)
        article_body = response.css("div.layout-contents__main article.article-content div.p-main-contents > p").extract()
        self.logger.info(article_body)
        yield None
