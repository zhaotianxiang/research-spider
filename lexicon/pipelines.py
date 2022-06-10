# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse, parse_qs

import scrapy
from scrapy.pipelines.files import FilesPipeline

from lexicon.items import DownfilesItem


class DownfilesPipeline(FilesPipeline):
    def get_media_requests(self, item, response):
        if isinstance(item, DownfilesItem):
            for url in item['file_urls']:
                yield scrapy.Request(url, meta={"item": item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']

        if item["file_name"]:
            print("正在下载：", item['file_name'])
            return item['file_name']
