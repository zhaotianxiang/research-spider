import datetime
import json

import scrapy
import uuid
from scrapy.linkextractors import LinkExtractor
from ..items import Item


class Spider(scrapy.Spider):
    id = 4
    name = 'yidaiyilu'
    allowed_domains = ['www.yidaiyilu.gov.cn']
    start_urls = [
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=1',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=2',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=3',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=4',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=5',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=6',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=7',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=8',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=9',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=10',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=11',
        'https://www.yidaiyilu.gov.cn/list/w/xmzb?page=12',
    ]

    def parse(self, response):
        links = LinkExtractor(restrict_css='div.common-item-infos > ul > li',
                              allow=["https://www.yidaiyilu.gov.cn"]).extract_links(response)
        self.logger.info("成功搜索 %s 个链接", len(links))
        for link in links:
            self.logger.info("成功搜索到 %s", link)
            yield scrapy.Request(link.url, callback=self.detail)

    def detail(self, response):
        title = response.css('div.news-details-box > h1::text').extract_first().strip()
        stripped = [s.strip() for s in response.css("div.news-details-box *::text").extract()]
        text = "".join(stripped)
        data = {
            'id': str(uuid.uuid1()),
            "title": title,
            'content': text
        }
        yield data
