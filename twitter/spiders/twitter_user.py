# 程序作用：
# 从记者数据库中读取所有记者数据，
# 1. 如果记者的麻汁列表有twitter账号，根据记者的账号获取记者在twitter的用户数据
# 2. 如果记者的麻汁列表没有twitter数据则根据记者名称检索可能存在的账号，并保存用户数据
# 程序幂等，即多次执行本程序不会对原有的数据库造成影响，只更新不删除，不会入重复数据

import json
import pymongo
import re
import scrapy
from scrapy.spiders import CrawlSpider
from urllib.parse import quote
from scrapy.utils.project import get_project_settings
SETTINGS = get_project_settings()


class Twitter(CrawlSpider):
    name = 'twitter_user'
    allowed_domains = ['twitter.com']
    x_guest_token = ""

    def __init__(self):
        self.client = pymongo.MongoClient(get_project_settings().get('MONGO_URI'))
        self.db = self.client[get_project_settings().get('MONGO_DB')]
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
        database_data = self.db.reporter.find()
        for reporter in database_data:
            is_has_twitter_account = False
            if reporter.get("reporter_code_list"):
                reporter_code_list = reporter['reporter_code_list']
                try:
                    reporter_code_list = json.loads(reporter['reporter_code_list'])
                except:
                    pass
                if isinstance(reporter_code_list, str):
                    self.logger.warn("数据的麻汁列别格式有问题 %s", reporter)
                    continue
                for reporter_code in reporter_code_list:
                    if reporter_code['code_type'] == 'twitter':
                        is_has_twitter_account = True
                        reporter['screen_name'] = reporter_code['code_content'].split('/')[-1]

            if is_has_twitter_account:
                reporter['search_by'] = 'account'
                self.user_list.append(reporter)
            else:
                reporter['search_by'] = 'reporter_name'
                self.user_list.append(reporter)

        self.logger.info("INIT [ ---- %s ---- ] USERS", len(self.user_list))

    def start_requests(self):
        yield scrapy.Request(url="https://twitter.com/explore", callback=self.add_header)

    def add_header(self, response):
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
            yield scrapy.Request(url, meta={
                'user': user
            }, callback=self.user, headers=self.headers)

    def user(self, response):
        data = json.loads(response.text)
        meta_user = response.meta['user']
        user_dict = data.get("globalObjects").get("users")

        #  根据twitter账号搜索
        if meta_user['search_by'] == 'account':
            for userId in user_dict:
                user = user_dict.get(userId)
                if user['screen_name'] != meta_user.get("screen_name"):
                    continue
                self.logger.info("根据后缀 %s 找到了记者用户", meta_user['search_by'])
                user["search_reporter_name"] = meta_user['reporter_name']
                user_description = user.get("description") + user.get("name") + user.get("screen_name")
                self.logger.info("找到用户  %-20s %s", meta_user['reporter_name'], user_description)
                if user.get('profile_image_url'):
                    item = meta_user.copy()
                    if not item.get("reporter_image_url"):
                        item['reporter_image_url'] = user.get('profile_image_url')
                        self.db.reporter.update_one(
                            {"reporter_id": item["reporter_id"], "media_id": item["media_id"]},
                            {"$set": dict(item)},
                            upsert=True)
                user.update(meta_user)
                yield user
        else:
            for userId in user_dict:
                user = user_dict.get(userId)
                user["search_reporter_name"] = meta_user['reporter_name']
                user_description = user.get("description") + user.get("name") + user.get("screen_name")
                if user_description:
                    kbs = re.compile(r'kbs|朝日新聞|読売新聞|voa|npr|yna｜'
                                     r'upi｜apnews', re.I)
                    if kbs.search(user_description):
                        self.logger.info("根据后缀 %s 找到了记者用户", meta_user['search_by'])

                        # 找到了记者的Twitter账号，反向更新记者数据库
                        if user.get('profile_image_url'):
                            item = meta_user.copy()
                            if not item.get("reporter_image_url"):
                                item['reporter_image_url'] = user.get('profile_image_url')
                                self.db.reporter.update_one(
                                    {"reporter_id": item["reporter_id"], "media_id": item["media_id"]},
                                    {"$set": dict(item)},
                                    upsert=True)
                        user.update(meta_user)
                        yield user
