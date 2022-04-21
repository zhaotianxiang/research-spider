BOT_NAME = 'domainsearch'
LOG_LEVEL = 'INFO'
SPIDER_MODULES = ['domainsearch.spiders']
NEWSPIDER_MODULE = 'domainsearch.spiders'
ROBOTSTXT_OBEY = False
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'
CONCURRENT_REQUESTS = 64
DOWNLOAD_DELAY = 0.1
# DomainsearchDownloaderMiddleware
SPIDER_MIDDLEWARES = {
    'domainsearch.middlewares.DomainsearchSpiderMiddleware': 542,
}
DOWNLOADER_MIDDLEWARES = {
    'domainsearch.middlewares.DomainsearchDownloaderMiddleware': 543,
}
DEFAULT_REQUEST_HEADERS = {
    'accept': '*/*'
}
COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'domainsearch.pipelines.DomainsearchPipeline': 2,
    'domainsearch.pipelines.MongoDBPipeline': 200,
}

# MongoDB 数据库配置
MONGO_URI = 'mongodb://root:841_sjzc@8.210.221.113:8410'
MONGO_DB = 'research'