import scrapy
import json
import re


class PDFSpider(scrapy.Spider):
    name = 'aptnotes'

    def __init__(self):
        with open('./aptnotes.json') as f:
            self.apt_list = json.load(f)
        self.logger.info("init %s items", len(self.apt_list))

    def start_requests(self):
        for apt in self.apt_list:
            yield scrapy.Request(apt["Link"], meta=apt)

    def parse(self, response):
        file_id = re.findall(r'(?<=postStreamURLs = ).*?(?=;)', response.text)[0].split('_')[-1].replace('"]', '')
        url = 'https://app.box.com/index.php?rm=box_download_shared_file&shared_name={}&file_id=f_{}'. \
            format(response.url.split('/')[-1], file_id)
        yield scrapy.Request(url, meta=response.meta, callback=self.download_pdf)

    def download_pdf(self, response):
        meta = response.meta
        meta['pdf_url'] = response.url
        yield meta
