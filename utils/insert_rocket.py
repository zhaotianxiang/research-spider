import csv
import os

import pymongo

file_set = set()

client = pymongo.MongoClient('mongodb://root:841_sjzc@8.210.221.113:8410')
db = client['media']


def insert(data):
    if 'reporter_id' in data:
        reporter = db.reporter.find_one({'reporter_id': data['reporter_id']})
    else:
        reporter = db.reporter.find_one({'reporter_name': data['name']})
    if reporter:

        if 'reporter_code_list' in reporter:
            reporter_code_list = reporter['reporter_code_list']
        else:
            reporter_code_list = []
        for phone in data['phones']:
            # 判断是否重复
            is_duplicate = False
            for code in reporter_code_list:
                if code['code_content'] == phone['number']:
                    is_duplicate = True

            if not is_duplicate:
                reporter_code_list.append({
                    'code_type': 'phone',
                    'code_content': phone['number']
                })
        for email in data['emails']:
            # 判断是否重复
            is_duplicate = False
            for code in reporter_code_list:
                if code['code_content'] == email['email']:
                    is_duplicate = True

            if not is_duplicate:
                reporter_code_list.append({
                    'code_type': 'email',
                    'code_content': email['email']
                })
        for link in data['links']:
            # 判断是否重复
            is_duplicate = False
            for code in reporter_code_list:
                if code['code_content'] == data['links'][link]:
                    is_duplicate = True

            if not is_duplicate:
                reporter_code_list.append({
                    'code_type': link,
                    'code_content': data['links'][link]
                })

        print("\n\n\n\n")
        reporter['reporter_code_list'] = reporter_code_list
        if 'job_history' in data:
            reporter['job_history'] = data['job_history']
        else:
            reporter['job_history'] = []

        if 'education' in data:
            reporter['education'] = data['education']
        else:
            reporter['education'] = []

        if 'location' in data:
            reporter['location'] = data['location']
        else:
            reporter['location'] = ''
        print(reporter)
        db.reporter.update_one({
            "reporter_id": reporter["reporter_id"],
            "media_id": reporter["media_id"]},
            {"$set": dict(reporter)},
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
            data = eval(row['最原始详情数据'])
            ret.append(data)
    return ret


if __name__ == '__main__':
    files = init_downloaded_file_set('/Users/zhaotianxiang/data/')
    for file in files:
        data = read_data(file)
        for item in data:
            insert(item)
