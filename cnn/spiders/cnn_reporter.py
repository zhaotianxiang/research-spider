import scrapy
from scrapy import Request
from mySpider.items import CNNReporterItem
import time
import re


class CnnReporterSpider(scrapy.Spider):
    name = 'cnn-reporter'
    allowed_domains = ['us.cnn.com']
    start_urls = ['https://us.cnn.com/specials/profiles',
                  'https://us.cnn.com/specials/tv/anchors-and-reporters',
                  'https://us.cnn.com/specials/more/cnn-leadership']
    # start_urls = ['https://us.cnn.com/profiles/maribel-aber-profile']

    def parse(self, response):
        for item in response.xpath("//div[@class='media']"):
            url = item.xpath("a/@href").extract()
            # print(6666, url)
            if len(url):
                reporter_url = response.urljoin(url[0])
                yield Request(url=reporter_url, callback=self.parse_reporter)
            else:
                continue

    def parse_reporter(self, response):

        content = response.xpath("//div[@class='cd__content']")

        name = content.xpath("div[@class='cd_profile-headline']/div[@class='cd__profile-name']/text()").extract()
        name = name[0] if len(name) else ""

        introduction = content.xpath("div[3]/div/p/text()").extract()
        introduction = introduction[0] if len(introduction) else ""

        social_links = []
        for item in response.xpath("//div[@class='social-description__follow-links']/div"):
            social_link = item.xpath("a/@href").extract()
            social_links.append(social_link)
        social_links = ["https:"+item[0] for item in social_links if len(item)]

        img_url = response.xpath("//div[@class='pg__background__image_wrapper']/img/@data-src-small").extract()
        img_url = "https:" + img_url[0] if len(img_url) else ""

        def get_links(web):
            for link in social_links:
                if web in link:
                    return link
                else:
                    continue
            return ""

        reporter = CNNReporterItem()
        if not name:
            return

        reporter["id"] = "cnn_" + response.url.split('/')[-1]
        reporter["name"] = name
        reporter["url"] = response.url
        reporter["introduction"] = introduction

        code_list = []
        for item in social_links:
            code_type = re.match(r"https://(.*?).com", item)
            if code_type.group(1):
                new_dict = dict()
                new_dict["code_type"] = code_type.group(1)
                new_dict["code_content"] = item
                code_list.append(new_dict)

        reporter["code_list"] = str(code_list)
        reporter["img_url"] = img_url
        yield reporter


