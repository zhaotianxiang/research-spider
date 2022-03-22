BOT_NAME = 'upi'
SPIDER_MODULES = ['upi.spiders']
NEWSPIDER_MODULE = 'upi.spiders'

LOG_LEVEL = "WARN"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.3
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*'
}
SPIDER_MIDDLEWARES = {
    'upi.middlewares.MediaspiderSpiderMiddleware': 543,
}
DOWNLOADER_MIDDLEWARES = {
    'upi.middlewares.MediaspiderDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
    'upi.pipelines.ImageSpiderPipeline': 1,
    'upi.pipelines.MongoDBPipeline': 3,
}

# 保存图片配置
IMAGES_STORE = "./upi/data/images/"
MEDIA_ALLOW_REDIRECTS = True

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:aini1314@39.107.26.235:27017'
MONGO_DB = 'media'
