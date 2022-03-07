import csv
import pdfkit
import logging
import os

csv_reader = csv.reader(open("./data/csv/kbs.csv"))


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_pdf(url):
    logging.info("downloading %s" % url)
    pdfkit.from_url(url, "./data/pdf/%s.pdf" % url.split("/")[-1])


news_detail_url_list = []
for line in csv_reader:
    news_detail_url_list.append(line[9])

mkdir("./data/pdf")
for url in news_detail_url_list[1:]:
    print(url)
    try:
        download_pdf(url)
    except:
        print("failed download pdf %s"%url)
    else:
        print("success download pdf %s"%url)
