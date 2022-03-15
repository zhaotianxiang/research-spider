import json
import csv
from urllib.parse import quote
from urllib.parse import urlencode

import scrapy

import re


class MobileTwitter(scrapy.Spider):
    name = 'twitter_mobile_posts'

    def start_requests(self):
        query_params = '{"userId": "1324626960434147328",\
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
                f"https://mobile.twitter.com/i/api/graphql/4yLxhZ2dQm5lsjAOKydYsA/UserMedia?"
                f"variables=" + query_params
        )

        headers = {
            'x-guest-token': '1503364727572901888',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        }
        yield scrapy.Request(url=url, headers=headers)

    def parse(self, response):
        try:
            response_data = json.loads(response.body)
            posts = response_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][0]["entries"]
            self.logger.info(" 第 %s 页共有 ----  %s 动态", response.meta["depth"], len(posts))
            for entry in posts:
                if entry.get("content"):
                    yield entry
            # 下一页
            try:
                if posts[101]:
                    next_page_hash = posts[101]["content"]["value"]
                    query_params = '{"userId": "1324626960434147328",\
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
                            f"https://mobile.twitter.com/i/api/graphql/4yLxhZ2dQm5lsjAOKydYsA/UserMedia?"
                            f"variables=" + query_params
                    )
                    headers = {
                        'x-guest-token': '1503364727572901888',
                        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                    }
                    yield scrapy.Request(url=url, headers=headers)
            except:
                self.logger.info(" 第 %s 页结束 ---- 翻页结束 ！", response.meta["depth"])
        except (Exception, err):
            self.logger.info(" --------------------  TOKEN 失效 ------------------- %s", err)

###### 翻页分析 ----------------
# {"userId": "1324626960434147328",
#  "count": 40,
#  "cursor": "HBaAgLOh16D1vCkAAA==",
#  "includePromotedContent": true,
#  "withQuickPromoteEligibilityTweetFields": true,
#  "withSuperFollowsUserFields": true,
#  "withDownvotePerspective": false,
#  "withReactionsMetadata": false,
#  "withReactionsPerspective": false,
#  "withSuperFollowsTweetFields": true,
#  "withVoice": true,
#  "withV2Timeline": true,
#  "__fs_dont_mention_me_view_api_enabled": false,
#  "__fs_interactive_text_enabled": true,
#  "__fs_responsive_web_uc_gql_enabled": false
#  }

## Twitter 将返回的列表翻页数值放在了数据中，最后两个 entries 中分别存放了上一页和下一页 cursor 的 hash 值
