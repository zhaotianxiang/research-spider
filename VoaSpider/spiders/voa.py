import scrapy
from scrapy.linkextractors import LinkExtractor

from ..items import VoaItem


def generateUrlList():
    return [
        'https://www.voanews.com/z/6715',
        'https://www.voanews.com/z/1755',
        'https://www.voanews.com/z/1757',
        'https://www.voanews.com/z/1769',
    ]


class Voa(scrapy.Spider):
    name = 'vha'
    start_urls = generateUrlList()

    def parse(self, response):
        le = LinkExtractor(restrict_css='ul#ordinaryItems li.fui-grid__inner')
        links = le.extract_links(response)

        # 详情页面
        for link in links:
            self.logger.info("VOA PARSE LIST ------------------- {} ".format(link.url))
            yield scrapy.Request(url=link.url, meta={"detail_url": link.url, "list_url": response.request.url},
                                 callback=self.parse_voa_detail)
        next_le = LinkExtractor(restrict_css='div.media-block-wrap > p > a')
        next_links = next_le.extract_links(response)

        # 下一列表页
        if next_links:
            next_url = next_links[0].url
            self.logger.info("VOA NEXT_PAGE IS ------------------ {} ".format(next_url))
            yield scrapy.Request(url=next_url, meta={"list_url": next_url})
        self.logger.info("VOA ALL Page Done! -------------------- {} ".format(next_url))

    def parse_voa_detail(self, response):
        meta = response.meta

        sel = response.css('#content > div:nth-child(1)')
        title = sel.xpath('./div/div/div[2]/h1/text()').extract_first()
        content = sel.xpath('//*[@id="article-content"]/div//p/text()').extract()
        self.logger.info("VOA PARSE DETAIL ------------------- {} {}".format([title], meta))

        le = LinkExtractor(restrict_css='div.links > ul > li')
        links = le.extract_links(response)
        # 详情页面
        if links:
            for link in links:
                self.logger.info("VOA PARSE LIST ------------------- {} ".format(link.url))
                yield scrapy.Request(url=link.url, meta={"title": title, "content": content, "reporter_url": link.url,
                                                         "detail_url": meta["detail_url"],
                                                         "list_url": meta["list_url"]},
                                     callback=self.parse_voa_reporter)

    def parse_voa_reporter(self, response):
        meta = response.meta
        self.logger.info("VOA PARSE REPORTER ------------------- meta {}".format(meta))
        sel = response.css('#content div.c-author')
        reporter_name = sel.xpath('./div/div[2]/h1/text()').extract_first()
        reporter_describe = sel.xpath('./div/div[2]/div/p/text()').extract_first()
        allow_domains = []
        mediaspiderItem = VoaItem()
        for img in response.css("div.c-author img.avatar"):
            link = img.css("::attr(src)").extract_first()
            if link:
                mediaspiderItem["reporter_image_url"] = link
                self.logger.info("VOA PARSE REPORTER LINK ------------------- link {}".format(link))
        mediaspiderItem["news_id"] = response.meta["detail_url"]
        mediaspiderItem["news_title"] = response.meta["title"]
        mediaspiderItem["news_contents"] = response.meta["content"]
        mediaspiderItem["reporter_id"] = response.meta["reporter_url"]
        mediaspiderItem["reporter_name"] = reporter_name
        mediaspiderItem["reporter_describe"] = reporter_describe
        yield mediaspiderItem
