BOT_NAME = 'media'
SPIDER_MODULES = ['media.spiders']
NEWSPIDER_MODULE = 'media.spiders'

LOGGER_LEVEL = "INFO"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.1
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': '*',
}
DOWNLOADER_MIDDLEWARES = {
    'media.middlewares.MediaDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
    'media.pipelines.ImageSpiderPipeline': 1,
    'media.pipelines.MongoDBPipeline': 3,
}

# 保存图片配置
IMAGES_STORE = "./images/data/images/"
MEDIA_ALLOW_REDIRECTS = True

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:aini1314@39.107.26.235:27017'
MONGO_DB = 'media'
