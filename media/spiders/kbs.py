import datetime
import json

import scrapy

from ..items import NewsItem
from ..items import ReporterItem


def date_range(start, end, step=1, format="%Y%m%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]


def generate_url_list(date_str):
    return 'https://news.kbs.co.kr/api/getNewsList?currentPageNo=1&rowsPerPage=500&exceptPhotoYn=Y&broadCode=0001' \
           '&broadDate={}&needReporterInfo=Y&orderBy=broadDate_desc%2CbroadOrder_asc'.format(date_str)


now = datetime.datetime.now().strftime('%Y%m%d')


class Spider(scrapy.Spider):
    id = 1
    name = 'kbs'
    media_name = 'KBS'
    start_urls = list(map(generate_url_list, date_range("20180101", now)))

    def parse(self, response):

        response_obj = json.loads(response.body)
        if not response_obj["success"]:
            self.logger.error(response_obj)
            return None

        for item in response_obj["data"]:
            news_detail_url = 'https://news.kbs.co.kr/news/view.do?ncd=' + item["newsCode"]

            newItem = NewsItem()
            newItem["news_id"] = item["newsCode"]
            newItem["news_title"] = item["newsTitle"]
            newItem['news_keywords'] = response.css("meta[name=keywords]::attr(content)").extract_first()
            newItem["news_title_cn"] = None
            if item["newsContents"]:
                newItem["news_content"] = item["newsContents"].replace("<br /><br />", " ")
            newItem["news_content_cn"] = None
            newItem["news_publish_time"] = item["broadDate"]
            newItem["news_publish_time"] = datetime.datetime(int(item["broadDate"][0:4]), int(item["broadDate"][4:6]),
                                                             int(item["broadDate"][6:8])).strftime('%Y-%m-%d %H:%M:%S')
            newItem["news_url"] = news_detail_url
            newItem["news_pdf"] = self.name + "_" + item["newsCode"] + ".pdf"
            newItem["news_pdf_cn"] = self.name + "_" + item["newsCode"] + "_cn.pdf"
            newItem["reporter_list"] = []

            if item['reporters']:
                for reporter in item['reporters']:
                    reporterItem = ReporterItem()
                    if reporter['imgUrl']:
                        reporterItem["reporter_image_url"] = response.urljoin(reporter['imgUrl'])
                        reporterItem["reporter_image"] = "%s_%s.jpg" % (self.name, reporter["reporterCode"])

                    reporterItem["reporter_id"] = reporter["reporterCode"]
                    reporterItem["reporter_name"] = reporter["reporterName"]
                    reporterItem["reporter_intro"] = reporter["jobName"]
                    reporterItem["reporter_url"] = 'https://news.kbs.co.kr/news/list.do?rcd=' + reporterItem[
                        "reporter_id"]
                    if reporter["email"]:
                        reporterItem["reporter_code_list"] = [{"code_content": reporter["email"], "code_type": "email"}]
                    reporterItem["reporter_name"] = reporter["reporterName"]
                    newItem["reporter_list"].append(reporterItem)
                    yield reporterItem
            yield newItem
