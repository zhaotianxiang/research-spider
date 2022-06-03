# Scrapy settings for lexicon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'lexicon'

SPIDER_MODULES = ['lexicon.spiders']
NEWSPIDER_MODULE = 'lexicon.spiders'
TELNETCONSOLE_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 20
DOWNLOAD_DELAY = 0.1
DEPTH_LIMIT = 100
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*',
}

ITEM_PIPELINES = {
    'lexicon.pipelines.DownfilesPipeline': 1,
}

FILES_STORE = r"./lexicon/data/"
