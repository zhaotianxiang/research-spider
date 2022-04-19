BOT_NAME = 'twitter'
SPIDER_MODULES = ['twitter.spiders']
NEWSPIDER_MODULE = 'twitter.spiders'
LOG_LEVEL = 'INFO'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2
DEFAULT_REQUEST_HEADERS = {
    'content-type': 'application/json',
    'accept': '*/*'
}

COOKIES_ENABLED = False

SPIDER_MIDDLEWARES = {
    'twitter.middlewares.MediaspiderSpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
    'twitter.middlewares.MediaspiderDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'twitter.pipelines.MongoDBPipeline': 3,
    'twitter.pipelines.ImageSpiderPipeline': 4,
}
COOKIES_DEBUG = True
MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = "./images/data/images/"

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:841_sjzc@8.210.221.113:8410'
MONGO_DB = 'media'