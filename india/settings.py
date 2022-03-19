# Scrapy settings for india project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'india'

SPIDER_MODULES = ['india.spiders']
NEWSPIDER_MODULE = 'india.spiders'
TELNETCONSOLE_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# CONCURRENT_REQUESTS = 100
DOWNLOAD_DELAY = 10
DEFAULT_REQUEST_HEADERS = {
    'Accept': '*/*'
}
DOWNLOADER_MIDDLEWARES = {
    'india.middlewares.MediaspiderDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
}

MEDIA_ALLOW_REDIRECTS = True

# 导出文件格式和文件名称
FEED_URI = './india/data/csv/%(name)s.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'
