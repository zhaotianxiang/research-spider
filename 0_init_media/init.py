import pymongo
import logging
import csv

import sys
sys.path.append("..")
from items.MongoDBItems import MediaItem

media_list = []
for line in csv.reader(open("./media.csv")):
    mediaItem = MediaItem()
    mediaItem["media_id"] = line[0]
    mediaItem["media_name_en"] = line[1]
    mediaItem["media_name_cn"] = line[2]
    mediaItem["media_content_type"] = line[3]
    mediaItem["media_official_website"] = line[4]
    media_list.append(mediaItem)


class MediaInit(object):
    def __init__(self):
        self.mongo_uri = 'mongodb://root:aini1314@39.107.26.235:27017',
        self.mongo_db = 'media'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process(self):
        self.db.media.drop()
        for item in media_list:
            if isinstance(item, MediaItem):
                self.db.media.update_one({"media_id": item["media_id"]}, {"$set": dict(item)}, upsert=True)
        print(f"init  {len(media_list)}  media")
        self.client.close()


MediaInit().process()
