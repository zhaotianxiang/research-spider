BOT_NAME = 'kbs'
SPIDER_MODULES = ['kbs.spiders']
NEWSPIDER_MODULE = 'kbs.spiders'

LOGGER_LEVEL = "INFO"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
# CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 5
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': '*',
}
DOWNLOADER_MIDDLEWARES = {
    'kbs.middlewares.MediaspiderDownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'kbs.pipelines.TransformDataPipeline': 1,
    'kbs.pipelines.MongoDBPipeline': 3,
}

IMAGES_STORE = "./kbs/data/images/"
MEDIA_ALLOW_REDIRECTS = True

# 数据库配置
HOST = "39.107.26.235"
PORT = 27017
USER = "root"
PASS = "aini1314"
