BOT_NAME = 'gdelt'
SPIDER_MODULES = ['gdelt.spiders']
NEWSPIDER_MODULE = 'gdelt.spiders'

LOG_LEVEL = "DEBUG"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 20
DOWNLOAD_DELAY = 0.1
DEPTH_LIMIT = 100
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
}

ITEM_PIPELINES = {
    'gdelt.pipelines.DownfilesPipeline': 1,
}

FILES_STORE = r"/Users/zhaotianxiang/data/zip"

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:841_sjzc@8.210.221.113:8410'
MONGO_DB = 'gdelt'
