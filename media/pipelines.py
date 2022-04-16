# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo
import sys
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from .items import NewsItem
from .items import ReporterItem


class FilterPipeline(ImagesPipeline):

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            if len(item.get('news_content')) < 3:
                raise DropItem("news content is empty")
        if isinstance(item, ReporterItem):
            if not item.get('reporter_name') or len(item["reporter_name"]) < 1:
                raise DropItem("reporter_name is empty")
        if isinstance(item, ReporterItem):
            if not item.get('reporter_name'):
                raise DropItem("reporter_name is empty")
        return item


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
        spider.logger.info("正在清空数据库数据...")
        reporter_result = self.db.reporter.remove({'media_id': spider.id})
        news_result = self.db.news.remove({'media_id': spider.id})
        spider.logger.info("清空数据执行结果:\n reporter_result:\n %s\b news_result:\n %s", reporter_result, news_result)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ReporterItem):
            if not item.get('media_id'):
                item['media_id'] = spider.id
                item['media_name'] = spider.name

            if 'reporter_code_list' in item:
                reporter_code_list = []
                code_content_set = set()
                for code in item['reporter_code_list']:
                    if not code["code_content"] in code_content_set:
                        code_content_set.add(code["code_content"])
                        reporter_code_list.append(code)
                item["reporter_code_list"] = reporter_code_list
            else:
                item["reporter_code_list"] = []

            # 数据库中防止无码址的作者覆盖有码址的作者
            old_item = self.db.reporter.find_one({"reporter_id": item["reporter_id"], "media_id": item["media_id"]})
            if old_item and len(old_item['reporter_code_list']) >= len(item['reporter_code_list']):
                raise DropItem("reporter_code_list keep old")

            self.db.reporter.update_one({"reporter_id": item["reporter_id"], "media_id": item["media_id"]},
                                        {"$set": dict(item)},
                                        upsert=True)
            spider.logger.info("成功保存记者信息 %s", item)

        if isinstance(item, NewsItem):
            if not item.get('media_id'):
                item['media_id'] = spider.id
                item['media_name'] = spider.name
            if 'news_reporter_list' in item:
                if len(item['news_reporter_list']) == 0:
                    raise DropItem("news_reporter_list is empty")
                news_reporter_list = []
                for reporter in item['news_reporter_list']:
                    reporter['media_id'] = spider.id
                    reporter['media_name'] = spider.name
                    news_reporter_list.append(reporter)
                item['news_reporter_list'] = news_reporter_list

            self.db.news.update_one({"news_id": item["news_id"], "media_id": item["media_id"]},
                                    {"$set": dict(item)},
                                    upsert=True)
            spider.logger.info("成功保存新闻信息 %s", item)
        return item
