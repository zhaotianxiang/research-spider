import scrapy
from scrapy.linkextractors import LinkExtractor

# 定义下载新闻分类的种子
def seed():
    return [
        'https://www.voanews.com/z/6715',
        'https://www.voanews.com/z/1757',
        'https://www.voanews.com/z/1757',
        'https://www.voanews.com/z/1769',
    ]


class Voa(scrapy.Spider):
    name = 'voa'
    start_urls = seed()

    def parse(self, response):
        links = LinkExtractor(restrict_css='div.media-block-wrap ul li').extract_links(response)
        self.logger.info("VOA PARSE LIST -------------- URL {} SIZE {} ".format(response.url, len(links)))

        # 详情页面
        for link in links:
            yield scrapy.Request(url=link.url, meta={"detail_url": link.url, "list_url": response.request.url},
                                 callback=self.parse_voa_detail)
        next_links = LinkExtractor(restrict_css='div.media-block-wrap > p > a').extract_links(response)

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
                yield scrapy.Request(url=link.url,
                                     meta={
                                         "title": title,
                                         "content": content,
                                         "reporter_url": link.url,
                                         "detail_url": meta["detail_url"],
                                         "list_url": meta["list_url"]
                                     },
                                     callback=self.parse_voa_reporter)

    def parse_voa_reporter(self, response):
        self.logger.info("VOA PARSE REPORTER ------------------- {} ".format(response.url))
        meta = {}
        meta["reporter_id"] = response.meta["reporter_url"]
        meta["reporter_name"] = response.css('#content div.c-author').xpath('./div/div[2]/h1/text()').extract_first()
        meta["reporter_describe"] = response.css('#content div.c-author').xpath(
            './div/div[2]/div/p/text()').extract_first()

        # 下载作者图片的链接
        for img in response.css("div.c-author img.avatar"):
            link = img.css("::attr(src)").extract_first()
            if link:
                meta["reporter_image_url"] = link
        link = response.css("div.c-author__btns > a::attr(href)").extract_first()
        author_api_link = response.urljoin(link)
        # 作者文章列表的链接
        if author_api_link:
            yield scrapy.Request(url=author_api_link, meta={"item": meta}, callback=self.parse_reporter_articles)

    def parse_reporter_articles(self, response):
        root = response.xpath('./channel/item')
        self.logger.info("REPORTER'S ARTICLE ------------------- API {} ITEM {}".format(response.url, len(root)))
        if root:
            for child in root:
                item = response.meta['item'].copy()
                item['news_title'] = child.xpath('./title/text()').extract_first()
                item['news_id'] = child.xpath('./link/text()').extract_first()
                item['news_contents'] = child.xpath('./description/text()').extract_first()
                item['publish_date'] = child.xpath('./pubDate/text()').extract_first()
                item['category'] = child.xpath('./category/text()').extract_first()
                item['author_api_link'] = response.url
                author_list = child.xpath('./author/text()').extract_first().split(" ")
                if author_list[0]:
                    item['email'] = author_list[0]
                yield item
