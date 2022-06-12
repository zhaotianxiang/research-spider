BOT_NAME = 'rocket'
SPIDER_MODULES = ['rocket.spiders']
NEWSPIDER_MODULE = 'rocket.spiders'

LOG_LEVEL = "INFO"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 2

DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
    'Api-Key': 'ab52edkd117f699da82a53926b1db64f8a215ed',
    'Content-Type': 'application/json'
}

ITEM_PIPELINES = {
    'rocket.pipelines.ImageSpiderPipeline': 1,
}

# 保存图片配置
IMAGES_STORE = "./data/image/"
MEDIA_ALLOW_REDIRECTS = True

# 导出文件格式和文件名称
FEED_URI = './data/csv/%(name)s_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:841_sjzc@8.210.221.113:8410'
MONGO_DB = 'media'

