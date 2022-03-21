# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class MyspiderPipeline:
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return '%s' % image_guid

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['img_url'])

    def item_completed(self, results, item, info):
        return item