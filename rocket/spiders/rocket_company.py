# 程序目的： 根据公司名称获取所有员工信息
#
# 1. 修改 company_list 里面的值， 多个公司增加多个值：
#    如：   company_list = [
#            '"Bryant Christie Inc."',
#            '"KBS"',
#        ]
#
# 2. 确认项目根路径下 scrapy.cfg 文件内容为：
#    [settings]
#    default = rocket.settings
#
# 3. 进入 C:\Users\spider7\Downloads\research-spider-master 文件夹， 选中上方的文件夹地址栏， 输入 cmd 后回车
#
# 4. 在黑框中运行程序输入： python -m scrapy crawl rocket_company
#
# 5. 结果见： C:\Users\spider7\Downloads\research-spider-master\data\csv 文件夹
#    人员头像见： C:\Users\spider7\Downloads\research-spider-master\data\image 文件夹

import json
import logging
import re
import rocketreach
import scrapy
import logging
import pymongo
import rocketreach
import scrapy
import json

logger = logging.getLogger(__name__)

########################################################
# 运行程序前确认需要搜索的公司名称如下，双引号表示精确搜索：
########################################################
company_list = [
    '"Bryant Christie Inc."'
]


def parse_job_history(item):
    ret = ""
    if not item.get("start_date"):
        ret += "None" + "～"
    else:
        ret += item["start_date"] + "～"
    if not item.get("end_date"):
        ret += "None"
    else:
        ret += item["end_date"]
    ret += ":" + item["company_name"]
    return ret


def parse_education(item):
    ret = ""
    if not item.get("start"):
        ret += "None" + "～"
    else:
        ret += str(item["start"]) + "～"
    if not item.get("end"):
        ret += "None"
    else:
        ret += str(item["end"])
    school = " "
    if 'school' in item:
        school = item['school']
    ret += ":" + str(school)
    return ret


logger = logging.getLogger(__name__)


class Spider(scrapy.Spider):
    name = 'rocket_company'
    allowed_domains = []
    key = 'ab52edkd117f699da82a53926b1db64f8a215ed'

    def start_requests(self):
        for company in company_list:
            url = f"https://api.rocketreach.co/v2/api/search"
            data = {
                "company": company,
                "query": {"current_employer": [company]},
                "start": 1,
                "page_size": 100
            }
            yield scrapy.Request(url, body=json.dumps(data), method="POST", meta=data)

    def parse(self, response):
        company = response.meta["company"]
        start = response.meta["start"]
        page_size = response.meta["page_size"]

        result = json.loads(response.text)
        peoples = result['profiles']
        pagination = result['pagination']

        self.logger.info("URL: %-20s Company: %-50s PAGE: %-3s/%-3s GOT: %-3s people", response.url, company,
                         int(pagination['start'] / page_size) + 1,
                         int(pagination['total'] / page_size) + 1, len(peoples))

        for people in peoples:
            url = f"https://api.rocketreach.co/v2/api/lookupProfile?api_key={self.key}&id={people['id']}"
            # yield people
            # 花费会员点数开启此项，关闭上一项
            yield scrapy.Request(url, meta={'people': people}, callback=self.profile)
        if len(peoples) > 0:
            url = f"https://api.rocketreach.co/v2/api/search"
            data = {
                "company": company,
                "query": {"current_employer": [company]},
                "start": start + page_size,
                "page_size": page_size
            }
            yield scrapy.Request(url, body=json.dumps(data), meta=data, method="POST")

    def profile(self, response):
        people = response.meta["people"]
        profile = json.loads(response.text)
        people.update(profile)
        self.logger.info("cost one credit")
        item = {
            '人员编号': people['id'],
            '人员名称': people['name'],
            '地区': people['region'],
            '城市': people['city'],
            '城市代码': people['country_code'],
            '雇主信息': people['current_employer'],
            '当前职位': people['current_title'],
            '当前领英地址': people['linkedin_url'],
            '地理位置': people['location'],
            '正式职位': people['normalized_title'],
            '人员状态': people['status'],
            '附加信息': people['teaser'],
            '头像信息（源数据）': profile['profile_pic'],
            '社交账号（源数据）': profile['links'],
            '工作经历（源数据）': profile['job_history'],
            '教育经历（源数据）': profile['education'],
            '邮箱地址（源数据）': profile['emails'],
            '电话号码（源数据）': profile['phones']
        }
        if profile['emails'] is not None:
            item['邮箱列表'] = "\n".join(list(map(lambda e: e['email'], profile['emails'])))
        if profile['phones'] is not None:
            item['电话列表'] = "\n".join(list(map(lambda p: p['number'], profile['phones'])))
        if profile['job_history'] is not None:
            item['工作列表'] = "\n".join(list(map(parse_job_history, profile['job_history'])))
        if profile['education'] is not None:
            item['教育列表'] = "\n".join(list(map(parse_education, profile['education'])))
        if profile['links'] is not None:
            for link in profile['links']:
                item[link] = profile['links'][link]
        item['最原始详情数据'] = people
        item['profile_pic'] = people['profile_pic']
        item['name'] = people['name']
        yield item
