import logging

import scrapy
from scrapy.pipelines.images import ImagesPipeline

logger = logging.getLogger(__name__)


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, response):
        if item.get('image_url'):
            logging.info("ImageSpiderPipeline imageUrl ----------------- %s ", item['image_url'])
            yield scrapy.Request(url=item['image_url'], media=item)

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta["name"]
