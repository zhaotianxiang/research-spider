# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
import scrapy


class AptnotesPipeline:
    def process_item(self, item, spider):
        return item


class DownLoadPdfPipeline(FilesPipeline):
    def get_media_requests(self, item, spider):
        yield scrapy.Request(item['pdf_url'], meta=item)

    def file_path(self, request, response=None, info=None):
        return request.meta.get('Year') + '/' + request.meta.get('Filename') + '.pdf'
