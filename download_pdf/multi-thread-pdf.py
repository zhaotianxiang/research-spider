import threading
import csv
import pdfkit

read_file_path = "./kbs/data/csv/kbs.csv"
write_file_path = "./kbs/data/pdf/%s.pdf"


def download_pdf(url, write_filepath=None):
    print(url)
    options = {
        'page-size': 'A4',
        'margin-top': '5mm',
        'margin-right': '5mm',
        'margin-bottom': '5mm',
        'margin-left': '5mm',
        'encoding': "UTF-8",
    }
    try:
        pdfkit.from_url(url, write_file_path % url.split("?")[-1], options=options)
        # pdfkit.from_url(url, write_filepath, options=options)
    except:
        pass


def thread_func(tasks):  # 线程函数
    for url in tasks:
        download_pdf(url)


def multi_thread_run(thread_num):
    news_detail_url_list = []
    csv_reader = csv.reader(open(read_file_path))
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