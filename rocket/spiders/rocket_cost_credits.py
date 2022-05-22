import json
import logging

import rocketreach
import scrapy
import logging
import pymongo
import rocketreach
import scrapy
import json

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
        ret += str(item["start"]) + "～"
    if not item.get("end"):
        ret += "None"
    else:
        ret += str(item["end"])
    ret += ":" + str(item["school"])
    return ret


class Spider(scrapy.Spider):
    name = 'rocket_cost_credits'

    allowed_domains = []
    # query = {"name":["Amit Shanbhag"],"keyword":["Founder"],"current_employer":["RocketReach.co"]}
    start = 0
    size = 5
    # youxiao
    key = 'ab52edkd117f699da82a53926b1db64f8a215ed'

    # tian
    # key = 'a4f232k9333d66b17f359eec8b1e4b89de31df6'

    def start_requests(self):
        self.client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
        self.db = self.client[self.settings.get('MONGO_DB')]
        result = self.db.reporter.find({"media_id": 8})

        reporter_list = []
        for reporter in result:
            reporter_list.append(reporter)

        self.logger.info("=================== %s ===============", len(reporter_list))

        for reporter in reporter_list:
            url = f"https://www.baidu.com/?q={reporter['reporter_name']}"
            query = {"name":[reporter['reporter_name']], "employer":'Associated Press'}
            # query = {"name":['Mariano Castillo'], "employer":['CNN']}
            yield scrapy.Request(url, meta={'query':  query, 'reporter_id': reporter['reporter_id']})


    def parse(self, response):
        query = response.meta["query"]
        reporter_id = response.meta["reporter_id"]
        rr = rocketreach.Gateway(rocketreach.GatewayConfig(self.key))
        self.logger.info("query %s", [query])
        self.logger.info("start %s", [self.start])
        self.logger.info("size %s", [self.size])
        self.logger.info("key %s", [self.key])
        s = rr.person.search().filter(**query)
        s = s.params(start=self.start, size=self.size)  # 设置查询数量
        results = s.execute()
        if isinstance(results, rocketreach.result.ErrorResult):
            self.logger.error("query error %s", results.message)
            self.logger.error("query error %s", results)
        if isinstance(results, rocketreach.result.SuccessfulResult):
            peoples = results.people
            self.logger.info("query success %s people", len(peoples))
            for people in peoples:
                print(people.current_employer, people.name)
                url = f"https://api.rocketreach.co/v2/api/lookupProfile?api_key={self.key}&id={people.id}"
                yield scrapy.Request(url, meta={'people': people, 'reporter_id':reporter_id}, callback=self.profile)
                break

    def profile(self, response):
        people = response.meta["people"]
        reporter_id = response.meta["reporter_id"]
        profile = json.loads(response.text)
        self.logger.info("people detail data %s", json.dumps(profile))
        item = {
            'reporter_id': reporter_id,
            '人员编号': people.id,
            '人员名称': people.name,
            '地区': people.region,
            '城市': people.city,
            '城市代码': people.country_code,
            '雇主信息': people.current_employer,
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
