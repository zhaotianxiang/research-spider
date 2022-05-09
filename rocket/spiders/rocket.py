import logging

import rocketreach
import scrapy

logger = logging.getLogger(__name__)


class Spider(scrapy.Spider):
    name = 'rocket'

    allowed_domains = []
    query = None
    start = 0
    size = 1
    key = "a4f232k9333d66b17f359eec8b1e4b89de31df6"
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
            self.logger.error("result error %s", results.message)
        if isinstance(results, rocketreach.result.SuccessfulResult):
            peoples = results.people
            self.logger.info("success get %s people", len(peoples))
            for people in peoples:
                yield {
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
                    '社交信息（源数据）': people.links,
                    '头像信息（源数据）': people.profile_pic
                }
