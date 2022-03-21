import csv
import pickle
import requests


def download_img(url, img_filepath):
    res = requests.get(url)
    if res.status_code != 200:
        print("图片下载失败：", url)

    with open(img_filepath, "wb") as fwb:
        fwb.write(res.content)
    print("图片下载完成")


def read_csv(filepath):
    with open(filepath, "r", encoding="utf8") as fr:
        csv_reader = csv.reader(fr)
        for line in csv_reader:
            yield line


def pickle_dump(obj, filepath):
    with open(filepath, "wb") as fw:
        pickle.dump(obj, fw)
        print("文件保存成功")


def pickle_load(filepath):
    with open(filepath, "rb") as fr:
        obj = pickle.load(fr)
    return obj

