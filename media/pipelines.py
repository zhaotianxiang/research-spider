# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging
import pymongo
import sys

sys.path.append("..")
from items.MongoDBItems import ReporterItem
from items.MongoDBItems import NewsItem


class ImageSpiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, response):
        if isinstance(item, ReporterItem):
            if item.get('reporter_image_url') and type(item.get('reporter_image_url')) == str:
                logging.info("reporter_image_url ---- {} ".format(item.get('reporter_image_url')))
                yield Request(url=item['reporter_image_url'], meta=item)

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta["reporter_image"]


class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        logging.warn("正在清空媒体数据库中 %s 的所有数据", spider.name)
        self.db.news.remove({'media_name': spider.name})
        self.db.reporter.remove({'media_name': spider.name})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ReporterItem):
            self.db.reporter.update_one({"reporter_id": item["reporter_id"], "media_id": item["media_id"]},
                                        {"$set": dict(item)},
                                        upsert=True)
        if isinstance(item, NewsItem):
            self.db.news.update_one({"news_id": item["news_id"], "media_id": item["media_id"]},
                                    {"$set": dict(item)},
                                    upsert=True)
        return item
