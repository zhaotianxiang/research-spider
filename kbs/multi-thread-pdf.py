import threading
import csv
import pdfkit


def download_pdf(url='http://google.com?xxx'):
    print(url)
    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
    }
    try:
        pdfkit.from_url(url, "./data/pdf/%s.pdf" % url.split("?")[-1], options=options)
    except:
        pass


def thread_func(tasks):  # 线程函数
    for url in tasks:
        download_pdf(url)


def multi_thread_run(thread_num):
    news_detail_url_list = []
    csv_reader = csv.reader(open("./data/csv/kbs.csv"))
    for line in csv_reader:
        news_detail_url_list.append(line[9])
    news_detail_url_list = news_detail_url_list[1:]
    n = thread_num
    num = len(news_detail_url_list) // n

    for i in range(n + 1):
        tasks = news_detail_url_list[i * num:(i + 1) * num]
        t = threading.Thread(target=thread_func, args=(tasks,))
        t.start()


if __name__ == '__main__':
    multi_thread_run(100)
