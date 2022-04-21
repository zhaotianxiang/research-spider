# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

# useful for handling different item types with a single interface
from .items import ResearchItem
from .items import CodeAddressItem


class ResearchPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ResearchItem):
            for key in item:
                if isinstance(item[key], list):
                    item[key] = "\n".join(list(set(item[key])))
        return item


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
        if isinstance(item, ResearchItem):
            self.db[spider.name].update_one({"联系页面": item["联系页面"]},
                                            {"$set": dict(item)},
                                            upsert=True)
            spider.logger.info("成功保存媒体信息 %s", item)
        if isinstance(item, CodeAddressItem):
            self.db[spider.name].update_one({"联系页面": item["联系页面"]},
                                            {"$set": dict(item)},
                                            upsert=True)
            spider.logger.info("成功保存媒体信息 %s", item)
        return item
