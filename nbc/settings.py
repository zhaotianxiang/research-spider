BOT_NAME = 'nbc'
SPIDER_MODULES = ['nbc.spiders']
NEWSPIDER_MODULE = 'nbc.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 1
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': '*',
}
DOWNLOADER_MIDDLEWARES = {
    'nbc.middlewares.MediaspiderDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
    'nbc.pipelines.TransformDataPipeline': 1,
    'nbc.pipelines.ImageSpiderPipeline': 2,
}

MEDIA_ALLOW_REDIRECTS = True

IMAGES_STORE = "./nbc/data/images/"
# 导出文件格式和文件名称
FEED_URI = './nbc/data/csv/%(name)s_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'
