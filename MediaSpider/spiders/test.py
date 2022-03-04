import scrapy

class MySpider(scrapy.Spider):
    name = "test"

    start_urls = [
        "https://news.kbs.co.kr/news/view.do?ncd=5408951",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        yield {
            "url": "https://news.kbs.co.kr/news/view.do?ncd=5408951",
            "pdf_url": "https://news.kbs.co.kr/news/view.do?ncd=5408951.pdf",
        }