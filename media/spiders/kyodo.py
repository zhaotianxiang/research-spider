import json
import re
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse

sys.path.append("../../")
from items.MongoDBItems import MediaItem
from items.MongoDBItems import ReporterItem
from items.MongoDBItems import NewsItem


class YanSpider(scrapy.Spider):
    name = 'kyodo'
    id = 22
    allowed_domains = ['english.kyodonews.net', 'china.kyodonews.net', 'www.47news.jp'][0:2]
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
        # response_json = None
        # if re.search('47news', response.url):
        #     print(re.findall(r'(?<=ld\+json">).*?(?=</script>)', response.text))
        #     self.logger.warn("================= %s", response.url)
        #     return None
        # else:
        response_json = json.loads(re.findall(r'(?<=ld\+json">)\[.*?\](?=</script)', response.text)[0])[0]

        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('/')[-1].split('.html')[0]
        newsItem['news_title'] = response_json['headline']
        newsItem['news_content'] = "".join(response.css("div.article-body p::text").extract())
        if re.search("china.kyodonews.net", response.url):
            newsItem['news_title_cn'] = newsItem['news_title']
            newsItem['news_content_cn'] = newsItem['news_content']

        newsItem['news_publish_time'] = response_json["datePublished"]
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
        newsItem['media_id'] = self.id
        newsItem['media_name'] = self.name
        newsItem['reporter_list'] = []
        reporter_name = response_json["author"]["name"].strip()
        reporter_id = reporter_name
        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = reporter_id
        reporterItem['reporter_name'] = reporter_name
        reporterItem['media_id'] = self.id
        reporterItem['media_name'] = self.name
        newsItem['reporter_list'].append(reporterItem)
        yield reporterItem
        self.logger.warn("保存新闻和记者信息 %s", response.url)
        if len(newsItem['reporter_list']) == 0:
            yield None
        yield newsItem

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
