# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging


class FilterPipeline:
    def process_item(self, item, spider):
        if not item['注册资本']:
            raise DropItem(f"Missing report_name in {item}")
        return item
