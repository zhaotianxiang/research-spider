# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

class MediaspiderPipeline:
    def process_item(self, item, spider):
        return item

class ImgspiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(url=item['reporter_image_url'], meta={"image_name": "voa/"+item['reporter_image_url'].split("/")[-1]})

    def file_path(self, request, response=None, info=None):
        return request.meta["image_name"]