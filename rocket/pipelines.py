import logging

import scrapy
from scrapy.pipelines.images import ImagesPipeline

logger = logging.getLogger(__name__)


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, response):
        if item['profile_pic']:
            logging.info("ImageSpiderPipeline imageUrl ----------------- %s ", item['profile_pic'])
            yield scrapy.Request(url=item['profile_pic'], media=item)

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta["name"]
