BOT_NAME = 'rocket'
SPIDER_MODULES = ['rocket.spiders']
NEWSPIDER_MODULE = 'rocket.spiders'

LOG_LEVEL = "DEBUG"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 5

DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
}

ITEM_PIPELINES = {
    'rocket.pipelines.ImageSpiderPipeline': 1,
}

# 保存图片配置
IMAGES_STORE = "/data/ftp/image/"
MEDIA_ALLOW_REDIRECTS = True

# 导出文件格式和文件名称
FEED_URI = '/data/ftp/csv/%(name)s_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'
