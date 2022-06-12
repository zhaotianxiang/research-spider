import csv
import os

import pymongo

file_set = set()

client = pymongo.MongoClient('mongodb://root:841_sjzc@8.210.221.113:8410')
db = client['rocketreach']

def insert(people):
        db.people.update_one({
            "id": people["id"]},
            {"$set": dict(people)},
            upsert=True
        )


def init_downloaded_file_set(dir):
    file_set = set()
    list_dir = os.listdir(dir)
    for file in list_dir:
        if 'csv' in file:
            file_set.add(os.path.join(dir, file))
    return file_set


def read_data(file_name):
    ret = []
    with open(file_name) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            ret.append(row)
    return ret


if __name__ == '__main__':
    files = init_downloaded_file_set('/Users/zhaotianxiang/data/rocket')
    for file in files:
        data = read_data(file)
        for item in data:
            insert(item)
