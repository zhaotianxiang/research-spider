import json
import scrapy
import re


class MobileTwitter(scrapy.Spider):
    name = 'twitter_mobile_posts'
    start_urls = ['https://abs.twimg.com/responsive-web/client-web/main.e8e94c25.js']

    def __init__(self):
        self.headers = {
            'authorization': ''
        }

        self.user_id = "533784838"

    def parse(self, response):
        revert_text = response.text[::-1]
        # "steewTresU":emaNnoitarepo,"w7ow-9k0Q6gHA-A9tsPDDC":dIyreuq{
        query = re.findall(r'(?<="steewTresU":emaNnoitarepo,").*?(?=":dIyreuq{)', revert_text)
        # s="AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        authorization = re.findall(r'AAAAAAAAAAAAAAAA.*?(?=")', response.text)
        query_path = ""
        auth_str = ""
        if query and len(query) > 0:
            query_path = query[0][::-1]
            self.logger.info("GOT QUERY_PATH ------------ %s", query_path)
        if authorization and len(authorization):
            auth_str = 'Bearer ' + authorization[0]
            self.headers['authorization'] = auth_str
            self.headers['content-type'] = 'application/x-www-form-urlencoded'
        self.logger.info("HEADERS ------------ %s", self.headers)

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
            query_params = '{"userId": "' + self.user_id + '",\
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
                    f"https://mobile.twitter.com/i/api/graphql/" + response.meta['query_path'] + "/UserTweets?"
                                                                                                 f"variables=" + query_params
            )
            headers = {
                'x-guest-token': response.meta['guest_token'],
                'authorization': response.meta['auth_str']
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_list)

    def parse_list(self, response):
        try:
            response_data = json.loads(response.body)
            posts = []
            for data in response_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]:
                if data["type"] == "TimelineAddEntries":
                    posts = data['entries']
            self.logger.info(" 第 %s 页共有 ----  %s 动态", response.meta["depth"] - 2, len(posts))
            for entry in posts:
                if entry.get("content"):
                    yield entry
            # 下一页
            try:
                if posts[101]:
                    next_page_hash = posts[101]["content"]["value"]
                    query_params = '{"userId": "' + self.user_id + '",\
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

                    headers = {
                        'x-guest-token': response.meta['guest_token'],
                        'authorization': response.meta['auth_str']
                    }
                    yield scrapy.Request(url=url, headers=headers, callback=self.parse_list)
            except:
                self.logger.info(" 第 %s 页结束 ---- 翻页结束 ！", response.meta["depth"])
        except:
            self.logger.info(" --------------------  TOKEN 失效 ------------------- %s")
