import os
import threading

import pdfkit

output_path = "/Volumes/data/pdfcn/"
file_set = set()


def init_downloaded_file_set(dir):
    list_dir = os.listdir(dir)
    for file in list_dir:
        file_set.add(file)


init_downloaded_file_set(output_path)

if not os.path.exists(output_path):
    os.mkdir(output_path)


def mongo_datas():
    import pymongo

    MONGO_URI = 'mongodb://root:841_sjzc@8.210.221.113:8410'
    myclient = pymongo.MongoClient(MONGO_URI)

    mydb = myclient['media']  # 选择media数据库
    mycollection = mydb["news"]  # 选择news数据表

    # query = {"media_name": media_name}  # 查询条件
    query = {}  # 查询条件
    res = mycollection.find(query)

    result = [(item["news_url"], item["news_pdf"]) for item in res]
    myclient.close()
    print("mongo数据获取完成， 共{}条".format(str(len(result))))
    return result


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
        pdfkit.from_url(url, write_filepath, options=options)
        print("success!")
    except:
        print("wrong")
        pass


def thread_func(tasks):  # 线程函数
    for (url, pdf_filename) in tasks:
        if pdf_filename in file_set:
            print(pdf_filename, "is downloaded")
            continue
        filepath = os.path.join(output_path, pdf_filename)
        if os.path.isfile(filepath):
            continue
        download_pdf(url, write_filepath=filepath)


def multi_thread_run(thread_num):
    news_detail_url_list = mongo_datas()

    n = thread_num
    num = len(news_detail_url_list) // n

    for i in range(n + 1):
        tasks = news_detail_url_list[i * num:(i + 1) * num]
        t = threading.Thread(target=thread_func, args=(tasks,))
        t.start()


if __name__ == '__main__':
    multi_thread_run(10)
