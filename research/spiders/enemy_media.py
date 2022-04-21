import re
from urllib import parse

import phonenumbers
import pymongo
import scrapy
from phonenumbers import timezone
from scrapy.linkextractors import LinkExtractor

from ..items import ResearchItem


class Spider(scrapy.Spider):
    name = 'enemy_media'
    allowed_domains = []

    def start_requests(self):
        self.client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
        self.db = self.client[self.settings.get('MONGO_DB')]
        config = self.db.spider.find_one({"spider_name": self.name})
        for search_key in config["arguments"]:
            url = f'https://www.google.com/search?q={search_key}&source=lnms&tbm=nws&start=0'
            yield scrapy.Request(url, meta={'item': {'搜索关键字': search_key}})

    def parse(self, response):
        item = response.meta['item']
        card = response.css("div#main > div > div")[2:]
        current_page = int(parse.parse_qs(response.url)['start'][0]) // 10 + 1
        self.logger.info("搜索关键字 %-10s 第 %-2s 页, 共有 %-2s 新闻 %s", item['搜索关键字'], current_page, len(card),
                         response.url)
        for news in card:
            url = news.css("div:nth-child(1) > a::attr(href)").extract_first()
            if url:
                researchItem = ResearchItem()
                researchItem["搜索关键字"] = item['搜索关键字']
                researchItem["机构名称"] = news.css("div:nth-child(1) > a > div::text").extract_first()
                researchItem["官网"] = re.findall("https?://.*?/", url)[0]
                # yield scrapy.Request("https://www.hk01.com", meta={"item": researchItem}, callback=self.news_web_site)
                yield scrapy.Request(researchItem["官网"], meta={"item": researchItem}, callback=self.news_web_site)

        # 下一页
        for link in scrapy.linkextractors.LinkExtractor(restrict_css='footer').extract_links(response):
            if '>' in link.text:
                yield scrapy.Request(link.url, meta={"item": item})

    def news_web_site(self, response):
        self.logger.info("抓取新闻页面信息 %s", response.url)
        item = response.meta['item'].copy()

        for link in LinkExtractor(
                restrict_css='body',
                allow_domains=self.allowed_domains,
                canonicalize=True).extract_links(response):
            if re.compile(r'contact', re.I).search(link.url):
                self.logger.info("找到了联系的页面 %s", link.url)
                item = response.meta['item'].copy()
                yield scrapy.Request(link.url, meta={'item': item}, callback=self.contact)
            #
            # 找到了关于xx的页面
            if re.compile(r'about', re.I).search(link.url):
                self.logger.info("找到了关于的的页面 %s", link.url)
                item = response.meta['item'].copy()
                yield scrapy.Request(link.url, meta={'item': item}, callback=self.contact)
        yield scrapy.Request(response.url+'?a=b', meta={'item': item.copy()}, callback=self.contact)

    def contact(self, response):
        self.logger.info("联系页面 %s", response)
        item = response.meta['item']
        item['联系页面'] = response.url
        item['邮箱'] = []
        item['电话'] = []
        item['传真'] = []
        item['微信公众号'] = []
        item['地址'] = []
        item['银行账号'] = []
        item['twitter'] = []
        item['facebook'] = []
        item['instagram'] = []
        item['telegram'] = []
        item['youtube'] = []
        item['linkedin'] = []

        removed_all_space_text = " ".join(response.css("*::text").extract())
        # 地址不太重要
        # address_list = re.findall(r"[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}", removed_all_space_text)
        # for address in address_list:
        #     item['地址'].append(address)

        # 邮箱
        email_list = re.findall('[\w\-]+@[\w]+\.[a-z]{2,4}.*?(?=[\"\\\<;\s\?])', response.text)
        for email in email_list:
            if re.search('@sentry.io', email):
                continue
            item['邮箱'].append(email)

        for country_str in ["HK", "CH", "US", "TW", "MO", "DE", "GB", "FR", "JP", "KR", "SG", "CA"]:
            for text in response.css("body *::text").extract():
                for phone_number in phonenumbers.PhoneNumberMatcher(text, country_str):
                    country = " ".join(timezone.time_zones_for_number(phone_number.number))
                    phone_number = phonenumbers.format_number(phone_number.number,
                                                              phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                    self.logger.info("找到了电话号码 %s %s", country, phone_number)
                    item['电话'].append(country + ":" + phone_number)

        # 传真
        fax_list = re.findall(r"(?<=Fax:).*?(?=^\w)", removed_all_space_text)
        for fax in fax_list:
            fax = fax.strip().replace(" ", "")
            item["传真"].append(fax)

        # 银行账号
        bank_card_list = re.findall(r'([1-9]{1})(\d{14} | \d{18})', removed_all_space_text)
        for bank_card in bank_card_list:
            self.logger.info("找到了 bank_card %s", bank_card)
            bank_card = bank_card.strip().replace("\"", "")
            item['银行账号'].append(bank_card)

        twitter_list = re.findall(r'https://.{0,4}twitter.com/.*?(?=[",])', response.text)
        for twitter in twitter_list:
            if re.search('share', twitter):
                continue
            self.logger.info("找到了 twitter %s", twitter)
            twitter = twitter.replace("\"", "").replace(";", "").replace("'", "").strip()
            item['twitter'].append(twitter)

        facebook_list = re.findall(r'https://www.facebook.com/.*?(?=[",])', response.text)
        for facebook in facebook_list:
            if re.search('share', facebook):
                continue
            self.logger.info("找到了 facebook %s", facebook)
            facebook = facebook.replace("\"", "").replace(";", "").replace("'", "").strip()
            item['facebook'].append(facebook)

        instagram_list = re.findall(r'https://www.instagram.com/.*?(?=[",])', response.text)
        for instagram in instagram_list:
            if re.search('share', instagram):
                continue
            self.logger.info("找到了 instagram %s", instagram)
            instagram = instagram.replace("\"", "").replace(";", "").replace("'", "").strip()
            item['instagram'].append(instagram)

        telegram_list = re.findall(r'https://www.telegram.com/.*?(?=[",])', response.text)
        for telegram in telegram_list:
            if re.search('share', telegram):
                continue
            self.logger.info("找到了telegram %s", telegram)
            telegram = telegram.replace("\"", "").replace(";", "").replace("'", "").strip()
            item['telegram'].append(telegram)

        youtube_list = re.findall(r'https://www.youtube.com/.*?(?=["\',>])', response.text)
        for youtube in youtube_list:
            if re.search('share', youtube):
                continue
            youtube = youtube.replace("\"", "").replace(";", "").replace("'", "").strip()
            item['youtube'].append(youtube)

        linkedin_list = re.findall(r'https://www.linkedin.com/.*?(?=["\',>])', response.text)
        for linkedin in linkedin_list:
            linkedin = linkedin.replace("\"", "").replace(";", "").replace("'", "").strip()
            item['linkedin'].append(linkedin)

        item['备注'] = ""

        yield item
