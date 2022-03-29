import pymongo
import datetime
import time

from datetime import date


class NewsPostProgress:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:aini1314@39.107.26.235:27017')
        self.db = self.client['media']

    def close(self):
        if self.client:
            self.client.close()

    def read_news_from_mongo(self):
        result = self.db.news.find()
        for row in result:
            if len(row['news_publish_time']) <4:
                continue
            if row['media_name'] == 'kbs':
                try:
                    publish_time = row['news_publish_time']
                    time = datetime.datetime(int(publish_time[0:4]), int(publish_time[4:6]), int(publish_time[6:8]))
                    row['news_publish_time'] = time.isoformat()
                except:
                    pass
            elif row['media_name'] == 'voa':
                try:
                    publish_time = row['news_publish_time']
                    time = datetime.datetime.strptime(publish_time, "%a, %d %b %Y %X %z")
                    row['news_publish_time'] = time.isoformat()
                except:
                    pass
            elif row['media_name'] == 'reuters' or row['media_name'] == 'apnews':
                print(row['news_publish_time'])
                publish_time = row['news_publish_time']
                time = datetime.datetime.fromisoformat(publish_time.replace('Z',''))
                row['news_publish_time'] = time.isoformat()
                print(row['media_name'], row['news_publish_time'])
            elif row['media_name'] == 'youmiuri':
                try:
                    print(row['news_publish_time'])
                    publish_time = row['news_publish_time']
                    time = datetime.datetime.fromisoformat(publish_time.replace('Z',''))
                    row['news_publish_time'] = time.isoformat()
                    print(row['media_name'], row['news_publish_time'])
                except:
                    pass
            elif row['media_name'] == 'upi':
                try:
                    print(row['news_publish_time'])
                    publish_time = row['news_publish_time']
                    # March 24, 2022 / 7:54 PM
                    time = datetime.datetime.strptime(publish_time, "%B %d, %Y / %I:%M %p")
                    row['news_publish_time'] = time.isoformat()
                    print(row['media_name'], row['news_publish_time'])
                except:
                    pass
            else:
                pass
                # time = datetime.fromisoformat(row['news_publish_time'])
                # row['news_publish_time'] = time.isoformat()
            self.db.news.update_one({"news_id": row["news_id"], "media_id": row["media_id"]},
                                    {"$set": dict(row)},
                                    upsert=True)


newsPostProgress = NewsPostProgress()
newsPostProgress.read_news_from_mongo()
newsPostProgress.close()
