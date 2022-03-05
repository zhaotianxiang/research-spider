# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import logging


class TransformDataPipeline:
    def process_item(self, item, spider):
        item['news_title'] = item['news_title'].replace('\n','')
        item['news_contents'] = item['news_contents'].replace('\n','')
        return item


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, response):
        logging.info("ImageSpiderPipeline imageUrl ----------------- {} ".format(item.get('reporter_image_url')))
        if item.get('reporter_image_url') and type(item.get('reporter_image_url')) == str:
            yield Request(url=item['reporter_image_url'],
                          meta={"image_name": "%s_%s" % (item['reporter_name'],item['reporter_image_url'].split("/")[-1])})

    def file_path(self, request, response=None, info=None):
        return request.meta["image_name"]
