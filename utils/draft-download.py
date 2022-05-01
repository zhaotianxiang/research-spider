# coding:utf-8
import json
import logging
import os
import time
from urllib.parse import urlparse

import pymongo
from selenium import webdriver

client = pymongo.MongoClient('mongodb://root:841_sjzc@8.210.221.113:8410')
db = client['media']
col = db['news']
downloaded_file_dir = '/Users/zhaotianxiang/data/pdf/'
file_set = set()


def google_download(url, filename):
    options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isHeaderFooterEnabled": False,
        "isLandscapeEnabled": True,  # landscape横向，portrait 纵向，若不设置该参数，默认纵向
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4 210 x 297 mm"
        },
    }
    options.add_argument('--enable-print-browser')
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': downloaded_file_dir  # 此处填写你希望文件保存的路径
    }
    options.add_argument('--kiosk-printing')
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.maximize_window()
    temp_height = 0
    while True:
        driver.execute_script("window.scrollBy(0,1000)")
        time.sleep(1)
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        if check_height == temp_height:
            break
        temp_height = check_height

    time.sleep(2)
    driver.execute_script('document.title="' + filename + '";window.print();')
    time.sleep(1)
    driver.close()


def convert_to_google_url(url):
    parsed_url = urlparse(url)
    return f"https://{'-'.join(parsed_url.hostname.split('.'))}.translate.goog/{parsed_url.path}?_x_tr_sl=auto&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp"


def init_downloaded_file_set(dir):
    list_dir = os.listdir(dir)
    for file in list_dir:
        file_set.add(file)


def read_draft_url_from_mongo():
    cursor = col.find().limit(10)
    for news in cursor:
        url_en = news["news_url"]
        url_cn = convert_to_google_url(url_en)
        filename_en = news["news_pdf"]
        filename_cn = news["news_pdf_cn"]
        # skip duplicated pdf file
        if filename_cn in file_set and filename_en in file_set:
            logging.info("%s %s downloaded", filename_cn, filename_en)
            continue
        else:
            try:
                logging.info("downloading %s %s", filename_cn, filename_en)
                # google_download(url_en, filename_en)
                google_download(url_cn, filename_cn)
            except:
                logging.error("Error download %s", filename_cn)


if __name__ == '__main__':
    init_downloaded_file_set(downloaded_file_dir)
    read_draft_url_from_mongo()
