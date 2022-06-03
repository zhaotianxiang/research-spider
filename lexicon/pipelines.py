# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from urllib.parse import urlparse, parse_qs

from scrapy.pipelines.files import FilesPipeline


class DownfilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        parsed_url = urlparse(request.url)
        qs = parse_qs(parsed_url.query)
        cate_name = qs['name'][0].replace("/","")
        file_name = f"{cate_name}_cate_{qs['id'][0]}.scel"
        print("正在下载：", file_name)
        return file_name
