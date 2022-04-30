import re
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor

from ..items import NewsItem
from ..items import ReporterItem


class Spider(scrapy.Spider):
    name = 'nbcnews'
    id = 13
    allowed_domains = ['www.nbcnews.com']
    start_urls = ['https://www.nbcnews.com/']

    def parse(self, response):
        links = LinkExtractor(restrict_css='body').extract_links(response)
        self.logger.warn("泛查询 %s --- %s 个子页面", response.url, len(links))
        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url.replace('featureFlag=false', '')
            if re.search('\d{4}$', url) and re.search('n', url.split('/')[-1].split('-')[-1]) and not re.search(
                    'author', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def news(self, response):
        # 解析详情页
        newsItem = NewsItem()
        newsItem['news_id'] = response.url.split('-')[-1].split("?")[0]
        newsItem['news_title'] = response.css("div.article-hero-headline h1::text").extract_first()
        newsItem['news_title_cn'] = None
        newsItem['news_content'] = "".join(response.css("div.article-body__content > p::text").extract())
        newsItem['news_content_cn'] = None
        published_time = response.css("div.article-body__date-source > time::text").extract_first()
        newsItem['news_publish_time'] = datetime.datetime \
            .strptime(published_time, "%B %d, %Y, %I:%M %p %Z") \
            .strftime('%Y-%m-%d %H:%M:%S')
        newsItem['news_url'] = response.url
        newsItem['news_pdf'] = f"{self.name}_{self.id}.pdf"
        newsItem['news_pdf_cn'] = f"{self.name}_{self.id}_cn.pdf"

        reporter_name = response.css('div.article-inline-byline > span.byline-name::text').extract_first()
        reporter_id = reporter_name

        reporter_links = LinkExtractor(restrict_css='div.article-inline-byline > span.byline-name').extract_links(
            response)
        if reporter_links and len(reporter_links) > 0:
            for reporter_link in reporter_links:
                if 'author' in reporter_link.url:
                    reporter_id = reporter_link.url.split('-')[-1]
                    reporter_name = reporter_link.text
                    yield scrapy.Request(url=reporter_link.url,
                                         meta={
                                             'reporter_id': reporter_id, 'reporter_name': reporter_name
                                         },
                                         callback=self.reporter,
                                         priority=10)
        if reporter_id:
            newsItem['reporter_list'] = [{'reporter_id': reporter_id, 'reporter_name': reporter_name}]
        self.logger.warn("保存新闻信息 %s", response.url)
        yield newsItem

        # 泛查询
        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            url = link.url
            if re.search('\d{4}$', url) and re.search('n', url.split('/')[-1].split('-')[-1]) and not re.search(
                    'author', url):
                yield scrapy.Request(url, callback=self.news)
            else:
                yield scrapy.Request(url)

    def reporter(self, response):

        reporterItem = ReporterItem()
        reporterItem['reporter_id'] = response.meta["reporter_id"]
        reporterItem['reporter_name'] = response.meta["reporter_name"]

        reporterItem['reporter_intro'] = response.css('div.person-lead__bio > p::text').extract_first()
        reporterItem['reporter_url'] = response.url

        image_link = response.css('div.person-lead__image > picture > img::attr(src)').extract_first()

        if image_link and re.search(r"nbcnews.com/image/", image_link):
            reporterItem['reporter_image_url'] = response.urljoin(image_link)
            reporterItem['reporter_image'] = f"{self.name}_{reporterItem['reporter_id']}.jpg"
        reporterItem['reporter_code_list'] = []
        email_list = response.css('ul.social-profile-list > li > a::attr(href)').extract()
        for email in email_list:
            if "mailto" in email:
                reporterItem['reporter_code_list'].append(
                    {'code_content': email.replace("mailto:", "").strip(), 'code_type': 'email'})

        social_account_list = LinkExtractor(restrict_css='div.person-lead__item').extract_links(response)
        for link in social_account_list:
            social_account = link.url
            if "twitter" in social_account:
                reporterItem['reporter_code_list'].append(
                    {'code_content': social_account, 'code_type': 'twitter'})
            elif "facebook" in social_account:
                reporterItem['reporter_code_list'].append(
                    {'code_content': social_account, 'code_type': 'facebook'})
            elif "instagram" in social_account:
                reporterItem['reporter_code_list'].append(
                    {'code_content': social_account, 'code_type': 'instagram'})
            else:
                reporterItem['reporter_code_list'].append(
                    {'code_content': social_account, 'code_type': 'account'})
        self.logger.warn("保存记者信息 %s", response.url)
        yield reporterItem
