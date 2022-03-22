import scrapy
import datetime
import json
import sys

sys.path.append("../../")
from items.MongoDBItems import MediaItem
from items.MongoDBItems import ReporterItem
from items.MongoDBItems import NewsItem


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
    start_urls = list(map(generate_url_list, date_range("20220312", now)))

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
            newItem["news_title_cn"] = item["newsCode"]
            if item["newsContents"]:
                newItem["news_content"] = item["newsContents"].replace("<br /><br />", " ")
            newItem["news_content_cn"] = item["newsCode"]
            newItem["news_publish_time"] = item["broadDate"]
            newItem["news_url"] = news_detail_url
            newItem["news_pdf"] = self.name + "_" + item["newsCode"] + ".pdf"
            newItem["news_pdf_cn"] = self.name + "_" + item["newsCode"] + "_cn.pdf"
            newItem["reporter_list"] = []
            newItem["media_id"] = 1
            newItem["media_name"] = self.name

            if item['reporters']:
                for reporter in item['reporters']:
                    reporterItem = ReporterItem()
                    if reporter['imgUrl']:
                        reporterItem["reporter_image_url"] = response.urljoin(reporter['imgUrl'])
                        reporterItem["reporter_image"] = "%s_%s_%s.jpg" % (
                            self.name, reporter["reporterName"], reporter["reporterCode"])

                    reporterItem["reporter_id"] = reporter["reporterCode"]
                    reporterItem["reporter_name"] = reporter["reporterName"]
                    reporterItem["reporter_intro"] = reporter["jobName"]
                    reporterItem["reporter_url"] = 'https://news.kbs.co.kr/news/list.do?rcd='+reporterItem["reporter_id"]
                    if reporter["email"]:
                        reporterItem["reporter_code_list"] = [{"code_content": reporter["email"], "code_type": "email"}]
                    reporterItem["reporter_name"] = reporter["reporterName"]
                    reporterItem["media_id"] = 1
                    reporterItem["media_name"] = self.name
                    newItem["reporter_list"].append(reporterItem)
                    yield reporterItem

            yield newItem
