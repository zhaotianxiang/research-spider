import csv
import pymongo
import sys

sys.path.append("..")

media_list = []
for line in csv.reader(open("./media.csv")):
    mediaItem = {}
    print(line)
    mediaItem["media_id"] = line[0]
    mediaItem["media_name_en"] = line[1]
    mediaItem["media_name_cn"] = line[2]
    media_list.append(mediaItem)


class MediaInit(object):
    def __init__(self):
        self.mongo_uri = 'mongodb://root:841_sjzc@8.210.221.113:8410',
        self.mongo_db = 'media'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process(self):
        self.db.media.drop()
        for item in media_list:
            self.db.media.update_one({"media_id": item["media_id"]}, {"$set": dict(item)}, upsert=True)
        print(f"init  {len(media_list)}  media")
        self.client.close()


MediaInit().process()
