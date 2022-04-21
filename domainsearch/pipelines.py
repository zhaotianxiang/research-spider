# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from scrapy.exceptions import DropItem


class DomainsearchPipeline:
    def process_item(self, item, spider):
        if not item.get("port"):
            raise DropItem("port is empty")
        if not item.get("ip"):
            raise DropItem("ip is empty")
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
        spider.logger.info("数据结果见 MongoDB research.domainsearch 表")
        self.client.close()

    def process_item(self, item, spider):
        del item["_id"]
        self.db[spider.name].update_one({"ip": item["ip"], "port": item["port"]},
                                        {"$set": dict(item)},
                                        upsert=True)
        spider.logger.info("成功保存机构信息 %s", item)
        return item
