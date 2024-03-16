BOT_NAME = 'media'
SPIDER_MODULES = ['media.spiders']
NEWSPIDER_MODULE = 'media.spiders'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
DOWNLOAD_DELAY = 0
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 0
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
}
ITEM_PIPELINES = {
    'media.pipelines.JsonWriterPipeline': 545,
}

MEDIA_ALLOW_REDIRECTS = True
