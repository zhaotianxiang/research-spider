import os, logging, json
import csv
from scrapy.utils.project import get_project_settings
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import logging

logger = logging.getLogger(__name__)
SETTINGS = get_project_settings()


def mkdirs(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


class SaveToFilePipeline:
    def __init__(self):
        self.savePostPath = SETTINGS['SAVE_POST_PATH']
        self.saveUserPath = SETTINGS['SAVE_USER_PATH']
        logger.info(self.saveUserPath)
        logger.info(self.savePostPath)
        mkdirs(self.savePostPath)  # ensure the path exists
        mkdirs(self.saveUserPath)

    def process_item(self, item, spider):
        self.save_to_file(item, self.saveUserPath + "twitter.user.csv")

    def save_to_file(self, item, filename):
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(dict(item), f, ensure_ascii=False)


class ImageSpiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, response):
        if item.get('profile_image_url') and type(item.get('profile_image_url')) == str:
            logging.info("ImageSpiderPipeline imageUrl ----------------- %s ",item.get('profile_image_url'))
            yield Request(url=item['profile_image_url'].replace("normal","400x400"),
                          meta={"image_name": "%s-%s-%s" % (item.get("search_reporter_name"),item.get("screen_name"),item['profile_image_url'].split("/")[-1].replace("normal","400x400"))})

    def file_path(self, request, response=None, info=None):
        return request.meta["image_name"]
