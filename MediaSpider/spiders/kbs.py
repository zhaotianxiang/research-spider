import scrapy
import logging
import datetime
import json

logger = logging.getLogger()

def dateRange(start, end, step=1, format="%Y%m%d"):
    print(start,end)
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]

def generateUrlList(dateStr):
    return 'https://news.kbs.co.kr/api/getNewsList?currentPageNo=1&rowsPerPage=500&exceptPhotoYn=Y&broadCode=0001&broadDate={}&needReporterInfo=Y&orderBy=broadDate_desc%2CbroadOrder_asc'.format(dateStr)

def loadResponseData(item):
    mediaspiderItem=MediaspiderItem()
    mediaspiderItem=item
    return mediaspiderItem


class KBS(scrapy.Spider):
    name = 'kbs'

    allowed_domain=["news.kbs.co.kr"]
    start_urls = list(map(generateUrlList, dateRange("20210101","20220302")))

    def parse(self, response):
        responseObj=json.loads(response.body)
        if not responseObj["success"]:
            self.logger.error(responseObj)
            yield None

        for item in responseObj["data"]:
            item['image_urls']=[]
            if item['reporters']:
                for reporter in item['reporters']:
                    item['image_urls'].append(response.urljoin(reporter['imgUrl']))
            yield item