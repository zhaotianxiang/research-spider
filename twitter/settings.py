BOT_NAME = 'twitter'
SPIDER_MODULES = ['twitter.spiders']
NEWSPIDER_MODULE = 'twitter.spiders'
LOG_LEVEL = 'INFO'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': '*',
}
ITEM_PIPELINES = {
    # 'twitter.pipelines.SaveToFilePipeline': 2,
}
COOKIES_DEBUG = True
MEDIA_ALLOW_REDIRECTS = True
# # 导出文件格式和文件名称
FEED_URI = './%(name)s/data/csv/%(name)s_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'