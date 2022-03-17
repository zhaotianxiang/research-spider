import json
import scrapy
import re
import csv


class MobileTwitter(scrapy.Spider):
    name = 'twitter_tweets'
    start_urls = ['https://abs.twimg.com/responsive-web/client-web/main.e8e94c25.js']

    def __init__(self):
        self.headers = {}
        self.user_list = []

        for line in csv.reader(open("./twitter/data/csv/twitter_kbs_user.csv")):
            self.user_list.append({
                "user_id": line[0],
                "user_name": line[2],
                "screen_name": line[3],
                "twitter_tweets_url": "https://twitter.com/" + line[3],
            })

        for line in csv.reader(open("./twitter/data/csv/twitter_asahi_user_2022-03-14T03-24-14.csv")):
            self.user_list.append({
                "user_id": line[0],
                "user_name": line[2],
                "screen_name": line[3],
                "twitter_tweets_url": "https://twitter.com/" + line[3],
            })

        for line in csv.reader(open("./twitter/data/csv/twitter_youmiuri_user_2022-03-14T02-48-52.csv")):
            self.user_list.append({
                "user_id": line[0],
                "user_name": line[2],
                "screen_name": line[3],
                "twitter_tweets_url": "https://twitter.com/" + line[3],
            })
        self.logger.info("初始化待爬取用户数量： %s 个", len(self.user_list))

    def parse(self, response):
        revert_text = response.text[::-1]
        query = re.findall(r'(?<="steewTresU":emaNnoitarepo,").*?(?=":dIyreuq{)', revert_text)
        authorization = re.findall(r'AAAAAAAAAAAAAAAA.*?(?=")', response.text)
        query_path = ""
        auth_str = ""
        if query and len(query) > 0:
            query_path = query[0][::-1]
            self.logger.info("获取用户动态页HASH路径 ---- %s", query_path)
        if authorization and len(authorization):
            auth_str = 'Bearer ' + authorization[0]
            self.headers['authorization'] = auth_str
            self.headers['content-type'] = 'application/x-www-form-urlencoded'
        self.logger.info("设置请求头加密字段 ---- %s", self.headers)

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
        if response_json.get("guest_token"):
            response.meta['guest_token'] = response_json["guest_token"]
            for user in self.user_list:
                query_params = '{"userId": "' + user['user_id'] + '",\
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
                    callback=self.parse_list)

    def parse_list(self, response):
        try:
            response_data = json.loads(response.body)
            posts = []
            for data in response_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]:
                if data["type"] == "TimelineAddEntries":
                    posts = data['entries']

            self.logger.info("用户：%s  第 %s 层共有 ----  %s 动态", response.meta["user"]["user_name"],
                             response.meta["depth"] - 2, len(posts))

            for entry in posts:
                if entry.get("content"):
                    entry["user_name"] = response.meta["user"]["user_name"]
                    entry["user_id"] = response.meta["user"]["user_id"]
                    entry["screen_name"] = response.meta["user"]["screen_name"]
                    entry["twitter_tweets_url"] = response.meta["user"]["twitter_tweets_url"]
                    if entry["content"]["entryType"] == "TimelineTimelineItem":
                        yield entry
            # 下一页
            try:
                if posts[101]:
                    next_page_hash = posts[101]["content"]["value"]
                    query_params = '{"userId": "' + response.meta["user"]["user_id"] + '",\
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
                                         }, callback=self.parse_list)
            except:
                self.logger.info(" 第 %s 页结束 ---- 翻页结束 ！", response.meta["depth"])
        except:
            self.logger.info(" --------------------  TOKEN 失效 ------------------- %s")
