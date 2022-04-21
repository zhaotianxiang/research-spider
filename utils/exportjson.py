import pymongo

client = pymongo.MongoClient('mongodb://root:841_sjzc@8.210.221.113:8410')
db = client["research"]

docs = list(db['reporters'].find())

