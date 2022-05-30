import json
import re
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import NewsItem
from ..items import ReporterItem


class Spider(CrawlSpider):
    name = 'bbc'
    media_name = 'BBC'
    id = 25
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/zhongwen/', 'https://www.bbc.com/']
    rules = (
        # Rule(LinkExtractor(allow=r'https://www.bbc.com/news/.*?\d{2}$'), callback='news_en', follow=True),
        Rule(LinkExtractor(allow=r'https://www.bbc.com/zhongwen/simp/.*?\d{2}$'), callback='news', follow=True),
    )

    def news_en(self, response):
        pass

    def news(self, response):
        # 解析详情页

        response_json = json.loads(re.findall(r'(?<=SIMORGH_DATA=){.*?}(?=</script>)', response.text)[0]);
        # metadata = response_json['pageData']['metadata']
        # content = response_json['pageData']['content']
        promo = response_json['pageData']['promo']
        # relatedContent = response_json['pageData']['relatedContent']

        newsItem = NewsItem()
        newsItem['reporter_list'] = []
        print(promo)
        for key in promo:
            print(key)
        for person in promo['byline']['persons']:
            reporter = ReporterItem()
            reporter['reporter_id'] = '-'.join(person['name'].split(" "))
            reporter['reporter_name'] = person['name']
            reporter['reporter_intro'] = person['function']
            newsItem['reporter_list'].append(reporter)
            yield reporter

        newsItem['news_id'] = response.url.split('/')[-1]
        newsItem['news_title'] = promo['headlines']['headline']
        newsItem['news_title_cn'] = ''
        newsItem['news_content'] = promo['summary']
        newsItem['news_content_cn'] = ''
        published_time = response_json['pageData']['metadata']['lastPublished']
        newsItem['news_publish_time'] = datetime.fromtimestamp(published_time/1000).strftime('%Y-%m-%d %H:%M:%S')
        self.logger.warn("保存新闻信息 %s", response.url)
        yield newsItem
