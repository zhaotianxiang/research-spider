import scrapy

from gdelt.items import DownfilesItem


class Spider(scrapy.Spider):
    name = 'gdelt'
    allowed_domains = []

    with open('./gdelt/masterfilelist-translation.txt') as file:
        urls = []
        for line in file:
            line_splits = line.split(" ")
            if len(line_splits) == 3:
                urls.append(line_splits[2].strip())
        start_urls = list(filter(lambda x: '/2022' in x, urls))

    def parse(self, response):
        file_url = response.url
        file_url = response.urljoin(file_url)
        item = DownfilesItem()
        item['file_urls'] = [file_url]
        yield item
