import json
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from ..items import NewsItem
from ..items import ReporterItem


# 定义下载新闻分类的种子
def seed():
    return [
        # news
        'https://www.yomiuri.co.jp/y_ajax/latest_list_news_more/category/2,54,48,47,59,1538,2277,2702,2949,154,194,3005/0/1/50/1939/50/0'
        # 社会
        'https://www.yomiuri.co.jp/y_ajax/latest_list/category/1524/1/1/20//0',
        # 政治
        'https://www.yomiuri.co.jp/y_ajax/latest_list/category/1561/1/1/20//0',
        # 经济
        'https://www.yomiuri.co.jp/y_ajax/latest_list/category/41/1/1/20//0',
        # 国际
        'https://www.yomiuri.co.jp/y_ajax/latest_list/category/1648/1/1/10//0',
    ]


class Spider(scrapy.Spider):
    id = 3
    name = 'youmiuri'
    start_urls = seed()

    def parse(self, response):
        response_obj = json.loads(response.body)
        if not response_obj.get("has_next_data"):
            self.logger.error("unexcepted response ", response.url)
            return None
        else:
            current_url = response.url.split("/")
            page = int(current_url[-1])
            page += 1
            current_url.pop()
            next_page_url = "/".join(current_url) + "/" + str(page)
            self.logger.info("next_page_url is %s", next_page_url)
            yield scrapy.Request(url=next_page_url)
        articles = Selector(text=response_obj.get("contents")).xpath('//article')
        self.logger.info("LIST ---- URL: %s SIZE: %s", response.url, len(articles))
        for item in articles:
            article = {
                "news_title": item.xpath('./div/h3/a/text()').extract_first(),
                "news_url": item.xpath('./div/h3/a/@href').extract_first(),
                "released_time": item.xpath('./div/div/time/@datetime').extract_first(),
            }
            request = scrapy.Request(url=article.get("news_url"), meta={'article': article},
                                     callback=self.parse_reporter_articles)
            request.cookies = {
                'HSSID': '842B85A7AB51AA740834CF9BCDAC6B7F9BBB0487C2101472CC75297D1B8D6CE4',
                'YOMISESSID': 'kdts9r9o7c9jp7d1671qtnem6g'
            }
            yield request

    def parse_reporter_articles(self, response):
        self.logger.info("REPORTER'S ARTICLE ---- %s", response.url)
        article_body = " ".join(response.css("article.article-content div.p-main-contents p::text").getall()).strip()
        newItem = NewsItem()
        newItem["reporter_list"] = []
        if article_body:
            author_list = re.findall(r'(?<=【).*?(?=】)', article_body)
            if author_list and len(author_list) > 0:
                for author_str in author_list:
                    author_area_list = author_str.split("、")
                    self.logger.info("author_area_list ---- %s", author_area_list)
                    for author_area_str in author_area_list:
                        self.logger.info("author_area_str ---- %s", author_area_str.split("＝", 1))
                        author_area_splits = author_area_str.split("＝", 1)
                        if author_area_splits and len(author_area_splits) == 2:
                            reporterItem = ReporterItem()
                            reporterItem["reporter_id"] = author_area_str.split("＝", 1)[1]
                            reporterItem["reporter_name"] = author_area_str.split("＝", 1)[1]
                            reporterItem["reporter_intro"] = author_area_str.split("＝", 1)[0]
                            newItem["reporter_list"].append(reporterItem)
                            yield reporterItem
        news_url = response.meta.get('article').get("news_url")
        news_id = news_url.split("/")[-2]
        newItem["news_id"] = news_id
        newItem["news_title"] = response.meta.get('article').get("news_title")
        newItem["news_content"] = article_body
        newItem["news_publish_time"] = response.meta.get('article').get("released_time").replace('Z', '').replace('T', ' ')
        newItem["news_url"] = response.meta.get('article').get("news_url")
        newItem["news_pdf"] = self.name + "_" + news_id + ".pdf"
        newItem["news_pdf_cn"] = self.name + "_" + news_id + "_cn.pdf"
        yield newItem
