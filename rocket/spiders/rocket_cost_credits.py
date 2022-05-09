import json
import logging

import rocketreach
import scrapy

logger = logging.getLogger(__name__)


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
        ret += item["start"] + "～"
    if not item.get("end"):
        ret += "None"
    else:
        ret += item["end"]
    ret += ":" + item["school"]
    return ret


class Spider(scrapy.Spider):
    name = 'rocket_cost_credits'

    allowed_domains = []
    query = None
    start = 0
    size = 1
    key = None
    start_urls = ['https://www.baidu.com']

    def parse(self, response):
        rr = rocketreach.Gateway(rocketreach.GatewayConfig(self.key))
        self.logger.info("query %s", [self.query])
        self.logger.info("start %s", [self.start])
        self.logger.info("size %s", [self.size])
        self.logger.info("key %s", [self.key])
        s = rr.person.search().filter(**eval(self.query))
        s = s.params(start=self.start, size=self.size)  # 设置查询数量
        results = s.execute()
        if isinstance(results, rocketreach.result.ErrorResult):
            self.logger.error("查询结果错误 %s", results.message)
        if isinstance(results, rocketreach.result.SuccessfulResult):
            peoples = results.people
            self.logger.info("成功查询到 %s 个人的信息", len(peoples))
            for people in peoples:
                url = f"https://api.rocketreach.co/v2/api/lookupProfile?api_key={self.key}&id={people.id}"
                yield scrapy.Request(url, meta={'people': people}, callback=self.profile)

    def profile(self, response):
        people = response.meta["people"]
        profile = json.loads(response.text)
        self.logger.info("个人联系信息详情 %s", json.dumps(profile))
        item = {
            '人员编号': people.id,
            '人员名称': people.name,
            '地区': people.region,
            '城市': people.city,
            '城市代码': people.country_code,
            '雇员信息': people.name,
            '当前职位': people.current_title,
            '当前领英地址': people.linkedin_url,
            '地理位置': people.location,
            '正式职位': people.normalized_title,
            '人员状态': people.status,
            '附加信息': people.teaser,
            '头像信息（源数据）': profile['profile_pic'],
            '社交账号（源数据）': profile['links'],
            '工作经历（源数据）': profile['job_history'],
            '教育经历（源数据）': profile['education'],
            '邮箱地址（源数据）': profile['emails'],
            '电话号码（源数据）': profile['phones']
        }
        # profile info
        self.logger.info("people : %s \n\n", people)
        # added
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
                print("link", link)
                item[link] = profile['links'][link]
        item['最原始详情数据'] = profile
        yield item
