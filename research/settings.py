BOT_NAME = 'research'
SPIDER_MODULES = ['research.spiders']
NEWSPIDER_MODULE = 'research.spiders'

LOG_LEVEL = "INFO"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 10
DEPTH_LIMIT = 100
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
}

ITEM_PIPELINES = {
    'research.pipelines.ResearchPipeline': 2,
    'research.pipelines.MongoDBPipeline': 200,
}

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:841_sjzc@8.210.221.113:8410'
MONGO_DB = 'research'
