import scrapy
from scrapy.linkextractors import LinkExtractor
import json
import csv


class Voa(scrapy.Spider):
    name = 'india'

    def start_requests(self):
        seed = 'https://capi.tianyancha.com/cloud-tempest/search/suggest/v2'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Accept': '*/*'
        }
        done_list = []
        for line in csv.reader(open("./india/data/csv/india.csv")):
            done_list.append(line[0])
        self.logger.info("done %s", len(done_list))
        for line in csv.reader(open("./india/spiders/company.csv")):
            company_name = line[0]
            if company_name in done_list:
                continue
            body = {"keyword": company_name, "pageSize": 5}
            yield scrapy.Request(url=seed, method="POST",
                                 body=json.dumps(body, ensure_ascii=False),
                                 meta={'keyword': body["keyword"]},
                                 headers=headers)

    def parse(self, response):
        response_json = json.loads(response.text)
        keyword = response.meta["keyword"]
        if response_json["errorCode"]:
            self.logger.error("根据公司名称查询公司编号失败！ %s %s", keyword, response_json)

        if response_json["data"] and len(response_json["data"]):
            company_name = response_json["data"][0]["comName"]
            company_id = response_json["data"][0]["graphId"]
            match_type = response_json["data"][0]["matchType"]
            if match_type == "公司名称匹配":
                url = 'https://www.tianyancha.com/company/' + company_id
                self.logger.info("成功搜索到 %s %s", keyword, company_name)
                yield scrapy.Request(
                    url,
                    meta={
                        "company_name": company_name,
                        "company_id": company_id,
                        "keyword": keyword
                    },
                    callback=self.parse_company_detail
                )
                return
            self.logger.error("不能搜索到公司名：%s", keyword)

    def parse_company_detail(self, response):
        meta = response.meta
        item = {}
        item["企查查搜索关键字"] = meta["keyword"]
        item["公司在企查查编号"] = meta["company_id"]
        item["公司在企查查地址"] = response.url
        item["公司名称"] = meta["company_name"]
        tags = response.css("div.tag-list-content > div > div.tag-common::text").extract()
        tag_str = ""
        for tag in tags:
            tag_str += tag + " "
        item["公司标签"] = tag_str

        detail = response.css("#company_web_top > div.box.-company-box > div.content > div.detail")
        item["法定代表人"] = detail.css("div.f0.boss > div > span:nth-child(2) > a::text").extract_first()
        item["法定代表人拥有企业数量"] = detail.css(
            "div.f0.boss > div > span:nth-child(2) > a:nth-child(2) > span::text").extract_first()
        item["公司地址"] = detail.css(
            "div.f0.clearfix.mb0.address > div.in-block.sup-ie-company-header-child-2.copy-component-box > span > div > div > div::text").extract_first()
        item["公司电话"] = detail.css(
            "div:nth-child(2) > div.in-block.sup-ie-company-header-child-1.copy-info-box > span > span.copy-it.info-need-copy._phone::text").extract_first()
        item["公司邮箱-单个"] = detail.css(
            "div.in-block.sup-ie-company-header-child-2.copy-info-box > span > span.email.copy-it.info-need-copy._email::text").extract_first()
        item["公司邮箱-多个"] = detail.css(
            "div.in-block.sup-ie-company-header-child-2.copy-info-box > span > span:nth-child(5) > script::text").extract()
        item["公司网址"] = detail.css(
            "div.f0.clearfix.mb0.address > div.in-block.sup-ie-company-header-child-1::text").extract()
        item["公司邮箱"] = detail.css(
            "div.in-block.sup-ie-company-header-child-2.copy-info-box > span > span:nth-child(5) > script::text").extract()
        item["公司简介"] = ""
        company_intro_list = detail.css("div.summary.mt8 > div > div::text").extract()
        for company_intro in company_intro_list:
            item["公司简介"] += company_intro

        item["企业类型"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(7) > td:nth-child(2)::text").extract_first()
        item["经营状态"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(1) > td:nth-child(4)::text").extract_first()
        item["成立日期"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(2) > td:nth-child(2)::text").extract_first()
        item["注册资本"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(3) > td:nth-child(2) > div::text").extract_first()
        item["实缴资本"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(4) > td:nth-child(2)::text").extract_first()
        item["工商注册号"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(4) > td:nth-child(4)::text").extract_first()
        item["统一社会信用代码"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(5) > td:nth-child(2) > span > span::text").extract_first()
        item["营业期限"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(6) > td:nth-child(2) > span::text").extract_first()
        item["经营状态"] = response.css("tbody > tr:nth-child(1) > td:nth-child(4)::text").extract_first()
        item["参保人数"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(8) > td:nth-child(2)::text").extract_first()
        item["曾用名"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(9) > td:nth-child(2) > span > span::text").extract_first()
        item["注册地址"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(10) > td:nth-child(2) > span > span > span::text").extract_first()
        item["经营范围"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(11) > td:nth-child(2) > span::text").extract_first()
        item["纳税人识别号"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(5) > td:nth-child(4) > span > span::text").extract_first()
        item["纳税人资质"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(6) > td:nth-child(4)::text").extract_first()
        item["行业"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(7) > td:nth-child(4)::text").extract_first()
        item["登记机关"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(8) > td:nth-child(4)::text").extract_first()
        item["英文名称"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(9) > td:nth-child(4) > span > span::text").extract_first()
        item["组织机构代码"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(5) > td:nth-child(6) > span > span::text").extract_first()
        item["核准日期"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(6) > td:nth-child(6)::text").extract_first()
        item["人员规模"] = response.css(
            "#_container_baseInfo > table > tbody > tr:nth-child(7) > td:nth-child(6)::text").extract_first()
        item["评分"] = ""
        if response.css("#sort-chart-score-img::attr(alt)").extract_first():
            item["评分"] = response.css("#sort-chart-score-img::attr(alt)").extract_first().replace("评分", "")
        yield item

    def parse_stock_right(self, response):
        # https://capi.tianyancha.com/cloud-equity-provider/v4/equity/indexnode.json?id=2315095069
        pass
