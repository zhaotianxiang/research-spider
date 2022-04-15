import json
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

from ..items import ReporterItem
from ..items import NewsItem

# 定义下载新闻分类的种子

def get_query(offect, size):
    query = '{"arc-site": "reuters",\
        "called_from_a_component": true,\
        "fetch_type": "sophi_or_collection_or_section",\
        "offset": ' + str(offect) + ',\
        "section_id": "/world",\
        "size": ' + str(size) + ',\
        "sophi_page": "word",\
        "sophi_widget": "topic",\
        "website": "reuters"\
    }'
    url = (
            f"https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?" +
            f"query=" + query
    )
    return url


class Spider(scrapy.Spider):
    id = 6
    name = 'reuters_en'

    def start_requests(self):
        meta = {
            "offset": 0,
            "size": 100
        }
        url = get_query(meta["offset"], meta["size"])
        yield scrapy.Request(url, meta=meta)

    def parse(self, response):
        response_json = json.loads(response.text)
        articles = response_json["result"]["articles"]
        if articles and len(articles) > 0:
            self.logger.warn("%s %s", response.url, len(articles))
            self.logger.warn("第 %s 页 %s 新闻", response.meta["offset"] / response.meta["size"], len(articles))
            for article in articles:
                newsItem = NewsItem()
                newsItem['news_id'] = article["id"]
                newsItem['news_title'] = article["title"]
                newsItem['news_title_cn'] = None
                newsItem['news_content'] = article["description"]
                newsItem['news_content_cn'] = None
                newsItem['news_publish_time'] = article["published_time"].replace('Z', '')
                newsItem['news_url'] = response.urljoin(article['canonical_url'])
                newsItem['news_pdf'] = f"reuters_{newsItem['news_id']}.pdf"
                newsItem['news_pdf_cn'] = f"reuters_{newsItem['news_id']}_cn.pdf"
                newsItem['reporter_list'] = []
                newsItem['media_id'] = self.id
                newsItem['media_name'] = 'reuters'

                for author in article["authors"]:
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
                                "code_content": social["url"].replace('mailto:','')
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
                # 进入新闻详情页面
                yield scrapy.Request(url=newsItem['news_url'],
                                     meta={"newsItem": newsItem},
                                     callback=self.news)
            # 下一页
            meta = {
                "offset": response.meta['offset'] + response.meta['size'],
                "size": response.meta['size']
            }
            yield scrapy.Request(get_query(meta["offset"], meta["size"]), meta=meta)

    def reporter(self, response):
        # 能补充获取头像 作者简介
        reporterItem = response.meta["reporterItem"]
        news_url = response.meta["news_url"]
        print("====================", news_url)
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

    def news(self, response):
        # 补充内容详情
        newsItem = response.meta["newsItem"]
        response_json = None
        try:
            response_json = json.loads(re.findall(r'(?<=globalContent=){.*?}(?=;)', response.text)[0])
        except:
            pass
        if response_json:
            content_elements = response_json['result']['content_elements']
            for content in content_elements:
                newsItem['news_content'] += content['content'] + '\n'
        self.logger.info("详情页面，%s %s", response.url, newsItem)
        yield newsItem
