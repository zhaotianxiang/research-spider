import csv
import pymongo


def get_collection(
                    db_name="media", collection_name="reporter",
                    db_url='mongodb://root:aini1314@39.107.26.235:27017'
                   ):
    my_client = pymongo.MongoClient(db_url)
    my_db = my_client[db_name]                       # 选择数据库, media数据库
    my_collection = my_db[collection_name]
    return my_collection


def update_reporters(collection):
    """采用\t分隔，清除文本中的\r、\n等换行"""

    for idx, item in enumerate(collection.find()):

        if item.get("reporter_intro"):
            value = item.get("reporter_intro").replace("\r", "").replace("\n", "").replace("\t", "")
            collection.update_one({"_id": item.get("_id")}, {"$set": {"reporter_intro": value}})


def update_news(collection):
    """采用\t分隔，清除文本中的\r、\n等换行"""

    query = {"media_name": "npr"}
    for idx, item in enumerate(collection.find(query)):
        if item.get("news_content"):
            value = item.get("news_content").replace("\r", "").replace("\n", "").replace("\t", "")
            collection.update_one({"_id": item.get("_id")}, {"$set": {"news_content": value}})
        else:
            if not item.get("news_content") and not item.get("title"):
                collection.delete_one({"_id": item.get("_id")})


if __name__ == '__main__':
    reporter_collection = get_collection()
    # update_reporters(reporter_collection)
    update_news(reporter_collection)