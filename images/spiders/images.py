import json
import re
import re
import scrapy
import sys
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import pymongo

sys.path.append("../../")
from items.MongoDBItems import MediaItem
from items.MongoDBItems import ReporterItem
from items.MongoDBItems import NewsItem


class YanSpider(scrapy.Spider):
    name = 'images'
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        reporterItem = ReporterItem()

        client = pymongo.MongoClient('mongodb://root:aini1314@39.107.26.235:27017')
        db = client['media']

        results = db.reporter.find({})
        for reporter in results:
            if reporter.get('reporter_image_url') and reporter.get('reporter_image'):
                reporterItem['reporter_image_url'] = reporter['reporter_image_url']
                reporterItem['reporter_image'] = reporter['reporter_image']
                if 'jpg' not in reporter['reporter_image']:
                    reporter['reporter_image'] = reporter['reporter_image'] + '.jpg'
                yield reporterItem
