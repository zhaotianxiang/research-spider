import pymongo
import logging

init_media_list = [{
    "meida_id": "01",
    "media_name_en": "kbs",
    "media_name_cn": "kbs",
    "media_content_type": "ka"
}, {
    "meida_id": "02",
    "media_name_en": "voa",
    "media_name_cn": "kbs",
    "media_content_type": "en"
}]


class MediaInit(object):
    def __init__(self):
        self.mongo_uri = 'mongodb://root:aini1314@39.107.26.235:27017',
        self.mongo_db = 'media'
        self.collection_name = "media"
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process(self):
        for item in init_media_list:
            self.db[self.collection_name].insert_one(dict(item))
        logging.info("init %s media", len(init_media_list))
        self.client.close()

MediaInit().process()
