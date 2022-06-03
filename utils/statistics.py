import pymongo

client = pymongo.MongoClient('mongodb://root:841_sjzc@8.210.221.113:8410')
db = client['media']

reporter_list = db.reporter.find({})
stastics = {}
for reporter in reporter_list:
    code_list = reporter['reporter_code_list']
    for code in code_list:
        code_type = code['code_type']
        code_content = code['code_content']
        if (stastics.get(code_type)):
            stastics[code_type] += 1
        else:
            stastics[code_type] = 1
print(stastics)
