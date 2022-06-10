from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import DownfilesItem


class Spider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['shurufa.baidu.com']
    start_urls = ['https://shurufa.baidu.com/dict']
    rules = [
        Rule(LinkExtractor(
            allow=('https://shurufa.baidu.com/dict_list.*?$',
                   'https://shurufa.baidu.com/dict_innerid_download?innerid=.*?$'),
            deny=('orderby')),
            callback='download',
            follow=True)
    ]

    def download(self, response):
        dict_id_list = response.css('a.dict-down')
        for dict in dict_id_list:
            dict_name = dict.css("::attr(dict-name)").extract_first()
            dict_name = dict_name.replace("/", "-")
            dict_innerid = dict.css("::attr(dict-innerid)").extract_first()
            url = f"https://shurufa.baidu.com/dict_innerid_download?innerid={dict_innerid}"
            item = DownfilesItem()
            item['file_urls'] = [url]
            item['file_name'] = f"{dict_name}.bdict"

            yield item
