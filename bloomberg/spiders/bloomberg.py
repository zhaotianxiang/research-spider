import scrapy
import datetime
import json


def generate_url_list():
    return 'https://www.bloomberg.com/lineup/api/lazy_load_paginated_module?id=pagination_story_list&page=new-economy-forum&offset=60&zone=righty'


now = datetime.datetime.now().strftime('%Y%m%d')


class bloomberg(scrapy.Spider):
    name = 'bloomberg'
    start_urls = generate_url_list

    def parse(self, response):

        response_obj = json.loads(response.body)
        if not response_obj["success"]:
            self.logger.error(response_obj)
            yield None

        for item in response_obj["data"]:
            news_detail_url = 'https://news.bloomberg.co.kr/news/view.do?ncd=' + item["newsCode"]
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
