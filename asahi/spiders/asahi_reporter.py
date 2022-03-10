import scrapy
from scrapy.http import Request
from mySpider.items import AsahiReporterItem


class AsahiReporterSpider(scrapy.Spider):
    name = 'asahi-reporter'
    allowed_domains = ['asahi.com']
    start_urls = ['https://www.asahi.com/sns/reporter/']        # 记者目录

    def parse(self, response):
        for idx, item in enumerate(response.xpath("//li[@class='Reporter']")):
            url = item.xpath("a/@href").extract()
            if len(url):
                reporter_url = response.urljoin(url[0])
                yield Request(url=reporter_url, callback=self.parse_reporter)
            else:
                continue

    def parse_reporter(self, response):
        """解析记者详情页面"""

        names = response.xpath("//div[@class='Title']/h2[@class='lh20']/text()").extract()
        name = names[0] if len(names) else ""
        departments = response.xpath("//div[@class='Title']/h2[@class='lh20']/span/text()").extract()
        department = departments[0] if len(departments) else ""
        department = department.replace("(", "").replace(")", "")
        twitters = response.xpath("//div[@class='Title']/a/@href").extract()
        twitter = twitters[0] if len(twitters) else ""
        introductions = response.xpath("//div[@class='PlainMod']/p//text()").extract()
        introduction = introductions[0] if len(introductions) else ""

        reporter = AsahiReporterItem()
        reporter["url"] = response.url
        reporter["department"] = department
        reporter["name"] = name
        reporter["twitter"] = twitter
        reporter["introduction"] = introduction
        reporter["facebook"] = ""

        yield reporter
