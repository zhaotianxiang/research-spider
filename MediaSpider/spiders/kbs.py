import scrapy
import datetime
import json
from ..items import MediaspiderItem


def date_range(start, end, step=1, format="%Y%m%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def generate_url_list(date_str):
    return 'https://news.kbs.co.kr/api/getNewsList?currentPageNo=1&rowsPerPage=500&exceptPhotoYn=Y&broadCode=0001' \
           '&broadDate={}&needReporterInfo=Y&orderBy=broadDate_desc%2CbroadOrder_asc'.format(date_str)


class KBS(scrapy.Spider):
    name = 'kbs'
    start_urls = list(map(generate_url_list, date_range("20210101", "20220301")))

    def parse(self, response):
        response_obj = json.loads(response.body)
        if not response_obj["success"]:
            self.logger.error(response_obj)
            yield None

        for item in response_obj["data"]:
            detail_url = 'https://news.kbs.co.kr/mobile/news/view.do?ncd='+item["newsCode"]

            if item['reporters']:
                for reporter in item['reporters']:
                    media_spider_item = MediaspiderItem()
                    media_spider_item["news_id"] = item["newsCode"]
                    media_spider_item["news_title"] = item["newsTitle"]
                    media_spider_item["news_contents"] = item["newsContents"]
                    media_spider_item["broad_time"] = item["broadDate"]
                    media_spider_item["reporter_id"] = reporter["reporterCode"]
                    media_spider_item["reporter_name"] = reporter["reporterName"]
                    media_spider_item["reporter_email"] = reporter["email"]
                    media_spider_item["reporter_twitter"] = reporter["twitter"]
                    media_spider_item["reporter_facebook"] = reporter["facebook"]
                    media_spider_item["reporter_job_name"] = reporter["jobName"]
                    media_spider_item["reporter_image_url"] = response.urljoin(reporter['imgUrl'])
                    yield media_spider_item
                yield scrapy.Request(url=detail_url, callback=self.download_full_html)

    def download_full_html(self, response):
        filename = './data/kbs/html/'+response.url.split("?")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        yield None
