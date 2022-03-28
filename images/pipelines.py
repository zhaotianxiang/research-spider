# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo
import sys
# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

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
