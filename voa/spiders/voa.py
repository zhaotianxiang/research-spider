import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import XMLFeedSpider
from scrapy.selector import Selector
from scrapy.http import XmlResponse


def seed():
    return [
        'https://www.voanews.com/z/6715',
        'https://www.voanews.com/z/1755',
        'https://www.voanews.com/z/1757',
        'https://www.voanews.com/z/1769',
    ]


class Voa(scrapy.Spider):
    name = 'voa'
    start_urls = seed()

    def parse(self, response):
        le = LinkExtractor(restrict_css='div.media-block-wrap ul li')
        links = le.extract_links(response)
        self.logger.info("VOA PARSE LIST -------------- URL {} SIZE {} ".format(response.url, len(links)))
        # 详情页面
        for link in links:
            yield scrapy.Request(url=link.url, meta={"detail_url": link.url, "list_url": response.request.url},
                                 callback=self.parse_voa_detail)
        next_le = LinkExtractor(restrict_css='div.media-block-wrap > p > a')
        next_links = next_le.extract_links(response)

        # 下一列表页
        if next_links:
            next_url = next_links[0].url
            yield scrapy.Request(url=next_url, meta={"list_url": next_url})
        else:
            self.logger.info("VOA ALL Page Done! -------------------- {} ")

    def parse_voa_detail(self, response):
        self.logger.info("VOA PARSE DETAIL ------------------- {} ".format(response.url))
        meta = response.meta

        sel = response.css('#content > div:nth-child(1)')
        title = sel.xpath('./div/div/div[2]/h1/text()').extract_first()
        content = sel.xpath('//*[@id="article-content"]/div//p/text()').extract()
        le = LinkExtractor(restrict_css='div.links > ul > li')
        links = le.extract_links(response)
        # 详情页面
        if links:
            for link in links:
                yield scrapy.Request(url=link.url, meta={"title": title, "content": content, "reporter_url": link.url,
                                                         "detail_url": meta["detail_url"],
                                                         "list_url": meta["list_url"]},
                                     callback=self.parse_voa_reporter)

    def parse_voa_reporter(self, response):
        self.logger.info("VOA PARSE REPORTER ------------------- {} ".format(response.url))
        meta = response.meta
        sel = response.css('#content div.c-author')
        reporter_name = sel.xpath('./div/div[2]/h1/text()').extract_first()
        reporter_describe = sel.xpath('./div/div[2]/div/p/text()').extract_first()
        allow_domains = []
        mediaspiderItem = {}
        mediaspiderItem["reporter_id"] = response.meta["reporter_url"]
        mediaspiderItem["reporter_name"] = reporter_name
        mediaspiderItem["reporter_describe"] = reporter_describe
        for img in response.css("div.c-author img.avatar"):
            link = img.css("::attr(src)").extract_first()
            if link:
                mediaspiderItem["reporter_image_url"] = link
                self.logger.info("VOA PARSE REPORTER LINK ------------------- link {}".format(link))

        link = response.css("div.c-author__btns > a::attr(href)").extract_first()
        author_api_link = response.urljoin(link)
        self.logger.info("AUTHOR LINK ----------------------- %s" % (author_api_link))
        response = XmlResponse(url='author_api_link')
        self.logger.info("%s" % (response.body));
        xxs = Selector(response)
        if author_api_link:
            yield scrapy.Request(url=author_api_link, meta={"item": mediaspiderItem},
                                 callback=self.reporter_all_article)

    def reporter_all_article(self, response):
        root = response.xpath('./channel/item')
        self.logger.info("REPORTER ALL ARTICLE ------------------- meta {}".format(root))
        if root:
            for child in root:
                item = {}
                item = response.meta['item'].copy()
                item['news_title'] = child.xpath('./title/text()').extract_first()
                item['news_id'] = child.xpath('./link/text()').extract_first()
                item['news_contents'] = child.xpath('./description/text()').extract_first()
                item['publish_date'] = child.xpath('./pubDate/text()').extract_first()
                item['category'] = child.xpath('./category/text()').extract_first()
                author = child.xpath('./author/text()').extract_first()
                author_list = author.split(" ")
                if author_list[0]:
                    item['email'] = author_list[0]
                yield item
