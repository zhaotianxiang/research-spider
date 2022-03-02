# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MediaspiderPipeline:
    def process_item(self, item, spider):
    	# 修改最终结果，中间件处理程序
        item["exporter_image_url"] = "这是个增加item的测试"
        return item
