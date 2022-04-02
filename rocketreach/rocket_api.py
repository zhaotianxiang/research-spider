import os
import rocketreach
from tools.utils import download_img
"""
Rocket API:https://rocketreach.co/api?section=api_section_ov_gs
获取Your unique API key
"""


class RocketAPI(object):
    def __init__(self, key):
        self.key = key

    def search(self, query, start=1, page_size=20):
        """
        Rocket Reach官方API接口
        :param api_key: 参照 Rocket API:https://rocketreach.co/api?section=api_section_ov_gs，进行获取
        :param name: 待查询人名
        :param company: 待查询公司名
        :param start: 查询开始下标
        :param page_size: 返回结果数量
        :return:
        """
        try:
            rr = rocketreach.Gateway(rocketreach.GatewayConfig(self.key))
            print(query)
            s = rr.person.search().filter(**query)
            s = s.params(start=start, size=page_size)           # 设置查询数量
            peoples = s.execute().people
            return peoples
        except Exception as e:
            print("Rocket API ERROR:\n", e)
            return None


def get_info(peoples):
    res = [["用户id", "姓名", "公司", "职位", "码址", "社交账号", "位置", "图片url"]]
    for people in peoples:
        for key, value in people.__dict__.items():
            print(key, ":", value)

        userid = people.id
        name = people.name
        img_url = people.profile_pic        # 头像URL

        if not os.path.exists("img"):
            os.mkdir("img")

        if img_url:
            img_path = os.path.join("img", "{}.jpg".format(userid))
            if not os.path.isfile(img_path):
                download_img(url=img_url, img_filepath=img_path)

        if people.links:
            links = "\n".join(["{}:{}".format(key, value) for key, value in people.links.items()])  # 个人社交账号
        else:
            links = ""

        location = people.location          # 定位
        title = people.current_title        # 头衔
        company = people.current_employer.upper().replace("NONE", "").strip()   # 公司

        if people.teaser:
            teaser = people.teaser
            emails = "\n".join(teaser["emails"])
            phones = "\n".join([item.get("number") for item in teaser["phones"]])
        else:
            emails = ""
            phones = ""

        numbers = emails + "\n" + phones
        res.append([userid, name, company, title, numbers, links, location, img_url])
    return res


if __name__ == '__main__':

    # 基于rocketreach的API，可以实现全自动的结果获取任务
    rocket = RocketAPI(key="a4ddcakf04a765dec0f1ae54df8ae9197c32a47")

    query = {"name": ["mask"], "keyword": ["shanghai"], "current_employer": [""]}   # 查询条件

    peoples = rocket.search(query, page_size=5)
    if peoples is not None:
        res = get_info(peoples)
        for item in res:
            print(item)
