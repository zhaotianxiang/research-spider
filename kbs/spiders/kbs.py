import scrapy
import datetime
import json


def date_range(start, end, step=1, format="%Y%m%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def generate_url_list(date_str):
    return 'https://news.kbs.co.kr/api/getNewsList?currentPageNo=1&rowsPerPage=500&exceptPhotoYn=Y&broadCode=0001' \
           '&broadDate={}&needReporterInfo=Y&orderBy=broadDate_desc%2CbroadOrder_asc'.format(date_str)


now = datetime.datetime.now().strftime('%Y%m%d')


class KBS(scrapy.Spider):
    name = 'kbs'
    start_urls = list(map(generate_url_list, date_range("20210101", now)))

    def parse(self, response):

        response_obj = json.loads(response.body)
        if not response_obj["success"]:
            self.logger.error(response_obj)
            yield None

        for item in response_obj["data"]:
            news_detail_url = 'https://news.kbs.co.kr/news/view.do?ncd=' + item["newsCode"]
            if item['reporters']:
                for reporter in item['reporters']:
                    reporter_image_url = None
                    if reporter['imgUrl']:
                        reporter_image_url = response.urljoin(reporter['imgUrl'])
                    yield {
                        "broad_time": item["broadDate"],
                        "news_id": item["newsCode"],
                        "news_title": item["newsTitle"],
                        "news_contents": item["newsContents"],
                        "reporter_id": reporter["reporterCode"],
                        "reporter_name": reporter["reporterName"],
                        "reporter_email": reporter["email"],
                        "reporter_job_name": reporter["jobName"],
                        "reporter_image_url": reporter_image_url,
                        "news_detail_url": news_detail_url,
                        "news_list_api": response.url,
                        "reporter_twitter": reporter["twitter"],
                        "reporter_facebook": reporter["facebook"],
                    }
