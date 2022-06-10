from urllib.parse import urlparse, parse_qs

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import DownfilesItem


class Spider(CrawlSpider):
    name = 'sougou'
    allowed_domains = ['pinyin.sogou.com']
    start_urls = ['https://pinyin.sogou.com/dict/']
    rules = (
        Rule(LinkExtractor(allow=r'https://pinyin.sogou.com/dict/cate/index/.*?$'), follow=True),
        Rule(LinkExtractor(allow=r'https://pinyin.sogou.com/dict/download_cell.php?.*?$'), callback='download',
             follow=True),
    )

    def download(self, response):
        file_url = response.url
        file_url = response.urljoin(file_url)
        item = DownfilesItem()
        item['file_urls'] = [file_url]

        parsed_url = urlparse(response.url)
        qs = parse_qs(parsed_url.query)
        cate_name = qs['name'][0].replace("/", "")
        file_name = f"{cate_name}.scel"
        item['file_name'] = file_name
        yield item
