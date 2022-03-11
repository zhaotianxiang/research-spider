import os, logging, json
import csv
from scrapy.utils.project import get_project_settings

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
