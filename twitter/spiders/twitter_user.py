import json
import pymongo
from urllib.parse import quote

import scrapy
from scrapy.spiders import CrawlSpider
import re


class Twitter(CrawlSpider):
    name = 'twitter_user'
    allowed_domains = ['twitter.com']
    x_guest_token = ""

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:aini1314@39.107.26.235:27017')
        self.db = self.client['media']
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

        self.user_list = []
        database_data = self.db.reporter.find({'media_name': 'youmiuri'})
        for reporter in database_data:
            self.user_list.append(reporter)
        self.logger.info("INIT [ ---- %s ---- ] USERS", len(self.user_list))

    def start_requests(self):
        yield scrapy.Request(url="https://twitter.com/explore", callback=self.add_cookie)

    def add_cookie(self, response):
        self.headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        }
        self.logger.info('Headers %s', self.headers)
        for r in self.start_query_request():
            yield r

    def start_query_request(self, cursor=None):
        for user in self.user_list:
            if cursor:
                url = self.url + '&cursor={cursor}'
                url = url.format(query=quote(user['reporter_name']), cursor=quote(cursor))
            else:
                url = self.url.format(query=quote(user['reporter_name']))
            yield scrapy.Request(url, meta={"userName": user['reporter_name'], 'user': user},
                                 callback=self.parse_user_list, headers=self.headers)

    def parse_user_list(self, response):
        data = json.loads(response.text)
        user_dict = data.get("globalObjects").get("users")
        self.logger.info("PARSE USER USER_NAME: %s ITEM: %s", response.meta.get("userName"), len(user_dict))

        for userId in user_dict:
            user = user_dict.get(userId)
            user["search_reporter_name"] = response.meta.get("userName")
            user_description = user.get("description") + user.get("name") + user.get("screen_name")
            if user_description:
                kbs = re.compile(r'kbs|朝日新聞|読売新聞|voa|npr|yna', re.I)
                if kbs.search(user_description):
                    self.logger.info("SUCCESS MATCH  %s ---- %s", response.meta.get("userName"), user_description)
                    if user.get('profile_image_url'):
                        item = response.meta['user'].copy()
                        if not item.get("reporter_image_url"):
                            item['reporter_image_url'] = user.get('profile_image_url')
                            self.db.reporter.update_one({"reporter_id": item["reporter_id"], "media_id": item["media_id"]},
                                                                        {"$set": dict(item)},
                                                                        upsert=True)
                    user.update(response.meta['user'])
                    yield user