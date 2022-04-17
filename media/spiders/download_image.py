import pymongo
import scrapy
from scrapy.utils.project import get_project_settings

from ..items import ImageItem

SETTINGS = get_project_settings()


class Spider(scrapy.Spider):
    id = 100
    name = 'download_image'
    start_urls = ["https://www.baidu.com"]

    def __init__(self, **kwargs):
        kwargs.pop('_job')
        self.client = pymongo.MongoClient(get_project_settings().get('MONGO_URI'))
        self.db = self.client[get_project_settings().get('MONGO_DB')]

    def parse(self, response):
        reporter_list = self.db.reporter.find()
        for reporter in reporter_list:
            image = ImageItem()
            if "reporter_image_url" in reporter and reporter["reporter_image_url"]:
                image['reporter_image_url'] = reporter["reporter_image_url"]
                image['reporter_image'] = reporter["reporter_image"]
                yield image
        self.client.close()
