import json
import csv
from urllib.parse import quote

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy_selenium import SeleniumRequest, SeleniumMiddleware

import re


class Twitter(CrawlSpider):
    name = 'twitter'
    allowed_domains = ['twitter.com']
    x_guest_token = ""

    def __init__(self):
        self.url = (
            f'https://api.twitter.com/2/search/adaptive.json?'
            f'include_profile_interstitial_type=1'
            f'&include_blocking=1'
            f'&include_blocked_by=1'
            f'&include_followed_by=1'
            f'&include_want_retweets=1'
            f'&include_mute_edge=1'
            f'&include_can_dm=1'
            f'&include_can_media_tag=1'
            f'&skip_status=1'
            f'&cards_platform=Web-12'
            f'&include_cards=1'
            f'&include_ext_alt_text=true'
            f'&include_quote_count=true'
            f'&include_reply_count=1'
            f'&tweet_mode=extended'
            f'&include_entities=true'
            f'&include_user_entities=true'
            f'&include_ext_media_color=true'
            f'&include_ext_media_availability=true'
            f'&send_error_codes=true'
            f'&simple_quoted_tweet=true'
            f'&query_source=typed_query'
            f'&pc=1'
            f'&spelling_corrections=1'
            f'&ext=mediaStats%2ChighlightedLabel'
            f'&count=20'
            f'&tweet_search_mode=live'
            f'&result_filter=user'
        )
        self.url = self.url + '&q={query}'
        self.num_search_issued = 0
        self.cursor_re = re.compile('"(scroll:[^"]*)"')

        self.user_list = set()

        for line in csv.reader(open("./kbs/data/csv/kbs.csv")):
            self.user_list.add(line[5])
        self.user_list = list(self.user_list)
        self.user_list.sort()
        self.user_list = self.user_list[12:13]
        self.logger.info("INIT [ ---- %s ---- ] USERS", len(self.user_list))

    def start_requests(self):
        yield SeleniumRequest(url="https://twitter.com/explore", callback=self.add_cookie)

    def add_cookie(self, response):
        self.headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        }
        self.logger.info('Headers %s', self.headers)
        for r in self.start_query_request():
            yield r

    def start_query_request(self, cursor=None):
        for user_name in self.user_list:
            if cursor:
                url = self.url + '&cursor={cursor}'
                url = url.format(query=quote(user_name), cursor=quote(cursor))
            else:
                url = self.url.format(query=quote(user_name))
            yield scrapy.Request(url, meta={"userName": user_name}, callback=self.parse_user_list, headers=self.headers)

    def parse_user_list(self, response):
        data = json.loads(response.text)
        user_dict = data.get("globalObjects").get("users")
        self.logger.info("PARSE USER USER_NAME: %s ITEM: %s", response.meta.get("userName"), len(user_dict))

        for userId in user_dict:
            user = user_dict.get(userId)
            user["search_reporter_name"] = response.meta.get("userName")
            user_description = user.get("description") + user.get("name") + user.get("screen_name")
            if user_description:
                kbs = re.compile(r'kbs', re.I)
                if kbs.search(user_description):
                    self.logger.info("SUCCESS MATCH  %s ---- %s", response.meta.get("userName"), user_description)
                    yield user
                    url = 'https://twitter.com/' + user.get("screen_name")
                    yield scrapy.Request(url, meta={"userName": response.meta.get('userName')},
                                         callback=self.parse_user_post, headers=self.headers)

    def parse_user_post(self, response):
        self.logger.info(response.text)
        pass
