import csv
import pdfkit
import logging
import os

csv_reader = csv.reader(open("./data/csv/kbs.csv"))

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_pdf(url='http://google.com?xxx'):
    print(url)
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        # 'orientation':'Landscape',#横向
        'encoding': "UTF-8",
        'no-outline': None,
        # 'footer-right':'[page]' 设置页码
    }
    logging.info("downloading %s" % url)
    pdfkit.from_url(url, "./data/pdf/%s.pdf" % url.split("?")[-1], options=options)


news_detail_url_list = []
for line in csv_reader:
    news_detail_url_list.append(line[9])

mkdir("./data/pdf")
for url in news_detail_url_list[1:]:
    try:
        download_pdf(url)
    except:
        pass
