import os, logging, json
import csv
import pymongo
from scrapy.utils.project import get_project_settings
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import logging
import sys

sys.path.append("..")
from items.MongoDBItems import SocialDynamicsItem

logger = logging.getLogger(__name__)
SETTINGS = get_project_settings()


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, response):
        if isinstance(item, SocialDynamicsItem):
            if item.get('dynamics_media_list') and len(item.get('dynamics_media_list')) > 0:
                for media in item.get('dynamics_media_list'):
                    if media['type'] == 'photo':
                        logging.info("ImageSpiderPipeline imageUrl ----------------- %s ", media['media_url'])
                        yield Request(url=media['media_url'], meta=media)

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta["media_name"]


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

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if item.get('screen_name'):
            self.db.twitter_account.update_one({"reporter_id": item["reporter_id"], "media_id": item["media_id"]},
                                               {"$set": dict(item)},
                                               upsert=True)
        if isinstance(item, SocialDynamicsItem):
            self.db.social_dynamic.update_one(
                {
                    "media_id": item["media_id"],
                    "reporter_id": item["reporter_id"],
                    "dynamics_id": item["dynamics_id"],
                    "account_type": item["account_type"],
                },
                {"$set": dict(item)},
                upsert=True)
        return item
