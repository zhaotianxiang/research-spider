import csv
import datetime
import json
import pymongo
import re
import scrapy
import sys

sys.path.append("../../")
from items.MongoDBItems import SocialDynamicsItem


class MobileTwitter(scrapy.Spider):
    name = 'twitter_tweets'
    start_urls = ['https://abs.twimg.com/responsive-web/client-web/main.114ab985.js']

    def __init__(self):
        self.headers = {}
        self.user_list = []
        self.client = pymongo.MongoClient('mongodb://root:aini1314@39.107.26.235:27017')
        self.db = self.client['media']
        self.mongo_user_accounts = self.db.twitter_account.find({})
        for user in self.mongo_user_accounts:
            self.user_list.append(user)
        self.logger.warn("初始化待爬取用户数量： %s 个", len(self.user_list))

    def parse(self, response):
        revert_text = response.text[::-1]
        query = re.findall(r'(?<="steewTresU":emaNnoitarepo,").*?(?=":dIyreuq{)', revert_text)
        authorization = re.findall(r'AAAAAAAAAAAAAAAA.*?(?=")', response.text)
        query_path = ""
        auth_str = ""
        if query and len(query) > 0:
            query_path = query[0][::-1]
            self.logger.warn("获取用户动态页HASH路径 ---- %s", query_path)
        if authorization and len(authorization):
            auth_str = 'Bearer ' + authorization[0]
            self.headers['authorization'] = auth_str
            self.headers['content-type'] = 'application/x-www-form-urlencoded'
        self.logger.warn("设置请求头加密字段 ---- %s", self.headers)

        yield scrapy.Request(
            url='https://api.twitter.com/1.1/guest/activate.json',
            method='POST',
            headers=self.headers,
            callback=self.active,
            meta={
                "query_path": query_path,
                "auth_str": auth_str
            }
        )

    def active(self, response):
        response_json = json.loads(response.text)
        self.logger.warn('激活游客Token ！！ ----  %s', response_json)
        if response_json.get("guest_token"):
            response.meta['guest_token'] = response_json["guest_token"]
            for user in self.user_list:
                query_params = '{"userId": "' + str(user['id']) + '",\
                "count": 100,\
                "includePromotedContent": false,\
                "withSuperFollowsUserFields": true,\
                "withDownvotePerspective": false,\
                "withReactionsMetadata": false,\
                "withReactionsPerspective": false,\
                "withSuperFollowsTweetFields": true,\
                "withClientEventToken": false,\
                "withBirdwatchNotes": false,\
                "withVoice": true,\
                "withV2Timeline": true,\
                "__fs_dont_mention_me_view_api_enabled": false,\
                "__fs_interactive_text_enabled": true,\
                "__fs_responsive_web_uc_gql_enabled": false\
                }'
                url = (
                        f"https://mobile.twitter.com/i/api/graphql/" +
                        response.meta['query_path'] + "/UserTweets?"
                                                      f"variables=" + query_params
                )
                headers = {
                    'x-guest-token': response.meta['guest_token'],
                    'authorization': response.meta['auth_str']
                }
                yield scrapy.Request(
                    url=url,
                    headers=headers,
                    meta={
                        "user": user,
                        "query_path": response.meta['query_path']
                    },
                    callback=self.parse_tweets)

    def parse_tweets(self, response):
        response_data = json.loads(response.body)
        posts = []
        if 'timeline_v2' in response_data["data"]["user"]["result"]:
            for data in response_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]:
                if data["type"] == "TimelineAddEntries":
                    posts = data['entries']

        self.logger.warn("用户：%-10s  %s 层共有 %-5s 动态", response.meta["user"]["name"],
                         response.meta["depth"] - 2, len(posts))

        self.logger.warn("%s 解析动态 %s 条", response.meta["user"]["name"], len(posts))
        for entry in posts:
            if entry.get("content"):
                twitter_user = response.meta["user"]
                entry["user_name"] = twitter_user["reporter_name"]
                entry["user_id"] = twitter_user["id"]
                entry["screen_name"] = twitter_user["screen_name"]
                entry["twitter_tweets_url"] = "https://twitter.com/" + twitter_user["screen_name"]
                if entry["content"]["entryType"] == "TimelineTimelineItem":
                    item = SocialDynamicsItem()

                    item['account_type'] = 'twitter'
                    result = entry['content']['itemContent']['tweet_results']['result']

                    if 'legacy' in result:
                        legacy = result['legacy']
                        item['dynamics_id'] = legacy['conversation_id_str']
                        item['account_name'] = twitter_user['name']
                        item['account_id'] = twitter_user['id']
                        item['dynamics_content'] = legacy['full_text']
                        item['dynamics_content_cn'] = ''
                        item['dynamics_favorite_count'] = legacy['favorite_count']
                        item['dynamics_media_list'] = []
                        item['dynamics_url'] = \
                            f"https://twitter.com/{twitter_user['screen_name']}/status/{item['dynamics_id']}"
                        if 'media' in legacy['entities']:
                            item['dynamics_media_list'] = list(map(
                                lambda media: {'type': 'photo', 'media_url': media['media_url_https']},
                                list(legacy['entities']['media'])))
                        item['media_id'] = twitter_user['media_id']
                        item['media_name'] = twitter_user['media_name']
                        item['reporter_id'] = twitter_user['reporter_id']
                        item['reporter_name'] = twitter_user['reporter_name']
                        item['dynamics_publish_time'] = datetime.datetime. \
                            strptime(legacy['created_at'], "%a %b %d %X %z %Y").isoformat()
                        yield item
        # 下一页
        if len(posts) == 102:
            next_page_hash = posts[101]["content"]["value"]
            query_params = '{"userId": "' + str(response.meta["user"]["id"]) + '",\
                    "count": 100,\
                    "cursor": "%s",\
                    "includePromotedContent": false,\
                    "withSuperFollowsUserFields": true,\
                    "withDownvotePerspective": false,\
                    "withReactionsMetadata": false,\
                    "withReactionsPerspective": false,\
                    "withSuperFollowsTweetFields": true,\
                    "withClientEventToken": false,\
                    "withBirdwatchNotes": false,\
                    "withVoice": true,\
                    "withV2Timeline": true,\
                    "__fs_dont_mention_me_view_api_enabled": false,\
                    "__fs_interactive_text_enabled": true,\
                    "__fs_responsive_web_uc_gql_enabled": false\
                }' % (next_page_hash)
            url = (
                    f"https://mobile.twitter.com/i/api/graphql/" + response.meta['query_path'] + "/UserTweets?"
                                                                                                 f"variables=" + query_params
            )
            yield scrapy.Request(url=url, headers=response.request.headers,
                                 meta={
                                     "user": response.meta["user"],
                                     "query_path": response.meta["query_path"]
                                 }, callback=self.parse_tweets)
        else:
            self.logger.warn("第 %s 页结束 ---- 翻页结束 ！", response.meta["depth"])
