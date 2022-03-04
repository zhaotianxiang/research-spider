# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import logging


class TransformDataPipeline:
    def process_item(self, item, spider):
        if item.get("reporter_name"):
            item["news_contents"] = item["news_contents"].replace("<br />", " ")
            return item
        else:
            raise DropItem(f"Missing report_name in {item}")


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, response):
        logging.info("ImageSpiderPipeline imageUrl ----------------- {} ".format(item.get('reporter_image_url')))
        if item.get('reporter_image_url') and type(item.get('reporter_image_url')) == str:
            yield Request(url=item['reporter_image_url'],
                          meta={"image_name": "%s-%s-%s" % (item.get("reporter_name"), item.get("reporter_id"),
                                                            item['reporter_image_url'].split("/")[-1])})

    def file_path(self, request, response=None, info=None):
        return request.meta["image_name"]
