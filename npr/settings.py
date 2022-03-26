BOT_NAME = 'npr'
SPIDER_MODULES = ['npr.spiders']
NEWSPIDER_MODULE = 'npr.spiders'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'

LOG_LEVEL = "INFO"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.1
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': '*',
}
ITEM_PIPELINES = {
    'npr.pipelines.MongoDBPipeline': 523,
}
MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = "./npr/data/images/"

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:aini1314@39.107.26.235:27017'
MONGO_DB = 'media'
