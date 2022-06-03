from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import DownfilesItem


class Spider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['shurufa.baidu.com']
    start_urls = ['https://shurufa.baidu.com/dict']
    rules = (
        Rule(LinkExtractor(allow=r'https://shurufa.baidu.com/dict_list.*?$'), follow=True),
        Rule(LinkExtractor(allow=r'https://shurufa.baidu.com/dict_innerid_download?innerid=2020208?.*?$'), callback='download', follow=True),
    )

    def download(self, response):
        file_url = response.url
        file_url = response.urljoin(file_url)
        item = DownfilesItem()
        item['file_urls'] = [file_url]
        yield item
