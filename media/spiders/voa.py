import datetime
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor

from ..items import NewsItem
from ..items import ReporterItem


# 定义下载新闻分类的种子
def seed():
    return [
        # 中国新闻
        'https://www.voanews.com/z/6715',
        # 新闻自由
        'https://www.voanews.com/z/5818'
    ]


class Spider(scrapy.Spider):
    id = 2
    name = 'voa'
    start_urls = seed()

    def parse(self, response):
        links = LinkExtractor(restrict_css='div.media-block-wrap ul li').extract_links(response)
        self.logger.info("VOA PARSE LIST -------------- URL {} SIZE {} ".format(response.url, len(links)))

        # 详情页面
        for link in links:
            yield scrapy.Request(url=link.url, meta={"detail_url": link.url, "list_url": response.request.url},
                                 callback=self.parse_voa_detail, priority=2)
        next_links = LinkExtractor(restrict_css='div.media-block-wrap > p > a').extract_links(response)

        # 下一列表页
        if next_links:
            next_url = next_links[0].url
            yield scrapy.Request(url=next_url, meta={"list_url": next_url}, priority=1)
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
                                         "list_url": meta["list_url"]
                                     },
                                     callback=self.parse_voa_reporter
                                     , priority=3)

    def parse_voa_reporter(self, response):
        self.logger.info("VOA PARSE REPORTER ------------------- {} ".format(response.url))
        meta = {
            "reporter_id": response.url.split('/')[-2],
            "reporter_name": response.css('#content div.c-author').xpath('./div/div[2]/h1/text()').extract_first(),
            "reporter_describe": response.css('#content div.c-author').xpath(
                './div/div[2]/div/p/text()').extract_first()
        }

        # 下载作者图片的链接
        for img in response.css("div.c-author img.avatar"):
            link = img.css("::attr(src)").extract_first()
            if link:
                meta["reporter_image_url"] = link
        link = response.css("div.c-author__btns > a.btn.btn-rss.btn--social::attr(href)").extract_first()
        author_api_link = response.urljoin(link)
        twitter_link = response.css("div.c-author__btns > a.btn.btn-twitter.btn--social::attr(href)").extract_first()

        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = meta["reporter_id"]
        reporterItem['reporter_name'] = meta["reporter_name"]
        reporterItem[
            'reporter_image'] = f'{self.name}_{reporterItem["reporter_id"]}.jpg'  # (媒体名称_人员内部编号.[jpg|png|jpeg])
        reporterItem['reporter_image_url'] = meta["reporter_image_url"].replace("w144", "w400").replace("w100", "w400")
        reporterItem['reporter_intro'] = ""
        intro_list = response.css('div.c-author__content > div.wsw > p::text').extract()
        for intro in intro_list:
            reporterItem['reporter_intro'] += intro + "\n"
        if response.css('div.c-author__content > div.wsw::text').extract_first():
            reporterItem['reporter_intro'] += response.css('div.c-author__content > div.wsw::text').extract_first()
        reporterItem['reporter_url'] = response.url
        reporterItem['reporter_code_list'] = []
        if twitter_link:
            reporterItem['reporter_code_list'] = [{'code_type': 'twitter', 'code_content': twitter_link}]
        # 第二中码址形式，藏在内容里
        links = LinkExtractor(restrict_css='div.c-author__content > div.wsw a').extract_links(response)
        if links and len(links):
            for link in links:
                if 'twitter' in link.url:
                    if not len(reporterItem['reporter_code_list']):
                        reporterItem['reporter_code_list'].append({'code_type': 'twitter', 'code_content': link.url})
        yield reporterItem
        # 作者文章列表的链接
        if author_api_link:
            meta["reporterItem"] = reporterItem
            yield scrapy.Request(url=author_api_link, meta=meta, callback=self.parse_reporter_articles, priority=0)

    def parse_reporter_articles(self, response):
        root = response.xpath('./channel/item')
        self.logger.info("REPORTER'S ARTICLE ---- API %s ITEM %s", response.url, len(root))
        if root:
            for child in root:
                newsItem = NewsItem()
                link = child.xpath('./link/text()').extract_first()
                newsItem['news_id'] = link.split("/")[-1].replace('.html', '')
                newsItem['news_title'] = child.xpath('./title/text()').extract_first()
                newsItem['news_keywords'] = response.css("meta[name=keywords]::attr(content)").extract_first()
                newsItem['news_title_cn'] = ""
                newsItem['news_content'] = child.xpath('./description/text()').extract_first()
                newsItem['news_content_cn'] = ""
                newsItem['news_publish_time'] = datetime.datetime.strptime(
                    child.xpath('./pubDate/text()').extract_first(), "%a, %d %b %Y %X %z").strftime('%Y-%m-%d %H:%M:%S')
                newsItem['news_url'] = link
                newsItem['news_pdf'] = f"{self.name}_{newsItem['news_id']}.pdf"
                newsItem['news_pdf_cn'] = f"{self.name}_{newsItem['news_id']}_cn.pdf"
                newsItem['reporter_list'] = [response.meta["reporterItem"]]
                yield newsItem
