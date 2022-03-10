import re
import time
import scrapy
import datetime
from scrapy.http import Request
from mySpider.items import AsahiItem


def string_to_datetime(st):
    """
    :param st:2022年3月4日 12時57分
    :return:
    """
    st = st.replace("年", "-").replace("月", "-").replace("日", "")
    st = st.replace("時", ":").replace("分", "")
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M")


def datetime_to_string(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class AsahiSpider(scrapy.Spider):
    name = 'asahi'
    allowed_domains = ['asahi.com']
    start_urls = ['https://www.asahi.com/national/list/', 'https://www.asahi.com/business/list/', 'https://www.asahi.com/politics/list/',
                  'https://www.asahi.com/international/list/', 'https://www.asahi.com/tech_science/list/',
                  'https://www.asahi.com/culture/list/', 'https://www.asahi.com/life/list/']

    def parse(self, response):
        for idx, url in enumerate(response.xpath("//*[@id='MainInner']/div[2]/ul/li")):

            article_url = url.xpath("a/@href").extract()
            if len(article_url):
                article_url = response.urljoin(article_url[0])
                yield Request(url=article_url, callback=self.parse_article)
            else:
                continue

    def parse_article(self, response):
        time.sleep(0.01)
        title = response.xpath("//*[@id='main']/div[@class='y_Qv3']/h1/text()").extract()
        tag = response.xpath("//*[@id='main']/div[@class='y_Qv3']/div/p/span[@class='ek8Dn']/a/text()").extract()
        reporter = response.xpath("//*[@id='main']/div[@class='y_Qv3']/div/span[@class='H8KYB']//text()").extract()
        broad_time = response.xpath("//*[@id='main']/div[@class='y_Qv3']/div/span[@class='UDj4P']/time/text()").extract()
        content = response.xpath("//*[@id='main']/div[@class='nfyQp']/p//text()").extract()
        relation_urls = response.xpath("//div[@class='_yMWq']/div[@class='B5yP3']/ul//li/a/@href").extract()

        if not title and not content and not relation_urls:
            title, tag, reporter, broad_time, content, relation_urls = self.parse_article2(response)

        broad_datetime_str = ""
        if len(broad_time):
            broad_datetime = string_to_datetime(broad_time[0])         # 用于结束递归的条件
            edg_datetime = datetime.datetime.strptime("2021-01-01 00:00", "%Y-%m-%d %H:%M")
            if edg_datetime >= broad_datetime:      # 如果新闻时间早于2021年，则跳过
                return
            broad_datetime_str = datetime_to_string(broad_datetime)    # 用于存储的日期字符串

        content = "".join(content).replace("\u3000", "")

        item = AsahiItem()
        item["url"] = response.url
        item["title"] = title
        item["reporter"] = reporter
        item["tag"] = tag
        item["broad_datetime"] = broad_datetime_str
        item["content"] = content
        yield item

        # 解析相关文章，以此向历史数据不断拓展
        for url in relation_urls:

            if not url:                                     # 广告
                continue
            relate_url = re.sub("\?iref=.*", "", url)
            yield Request(url=relate_url, callback=self.parse_article)

    def parse_article2(self, response):
        """
        部分文章，无法被parse_article解析
        :param response:
        :return:
        """
        title = response.xpath("//div[@class='ArticleTitle']/div[@class='Title']/h1/text()").extract()
        reporter = response.xpath("//div[@class='Title']/div[@class='TagUnderTitle']/p[@class='Sub']/text()").extract()
        tag = response.xpath("//span[@class='TagMatome']//text()").extract()
        broad_time = response.xpath("//span[@class='UpdateDate']/time/text()").extract()

        content = response.xpath("//div[@class='ArticleText']//p//text()").extract()
        content = "".join(content).replace("\u3000", "")

        relation_url = response.xpath("//ul[@class='InnerArticleList']//li/a/@href").extract()

        return title, tag, reporter, broad_time, content, relation_url

