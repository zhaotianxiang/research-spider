import json
import csv
from urllib.parse import quote

import scrapy
from scrapy.spiders import CrawlSpider
from scrapy_selenium import SeleniumRequest, SeleniumMiddleware

import re


class Post(CrawlSpider):
    name = 'posts'
    allowed_domains = ['twitter.com']
    x_guest_token = ""

    def __init__(self):
        self.url = f'https://twitter.com/i/api/graphql/CDDPst9A-AHg6Q0k9-wo7w/UserTweets?variables=%257B%2522userId%2522%253A%2522164509454%2522%252C%2522count%2522%253A40%252C%2522includePromotedContent%2522%253Atrue%252C%2522withQuickPromoteEligibilityTweetFields%2522%253Atrue%252C%2522withSuperFollowsUserFields%2522%253Atrue%252C%2522withDownvotePerspective%2522%253Afalse%252C%2522withReactionsMetadata%2522%253Afalse%252C%2522withReactionsPerspective%2522%253Afalse%252C%2522withSuperFollowsTweetFields%2522%253Atrue%252C%2522withVoice%2522%253Atrue%252C%2522withV2Timeline%2522%253Atrue%252C%2522__fs_dont_mention_me_view_api_enabled%2522%253Afalse%252C%2522__fs_interactive_text_enabled%2522%253Atrue%252C%2522__fs_responsive_web_uc_gql_enabled%2522%253Afalse%257D'

        # self.url = self.url + '&q={query}'
        # self.num_search_issued = 0
        # self.cursor_re = re.compile('"(scroll:[^"]*)"')
        #
        # self.user_list = set()
        #
        # for line in csv.reader(open("./kbs/data/csv/kbs.csv")):
        #     self.user_list.add(line[5])
        # self.user_list = list(self.user_list)
        # self.user_list.sort()
        # self.user_list = self.user_list[12:13]
        # self.logger.info("INIT [ ---- %s ---- ] USERS", len(self.user_list))

    def start_requests(self):
        yield SeleniumRequest(url=self.url)

    def add_cookie(self, response):
        self.headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        }
        self.logger.info('Headers %s', self.headers)
        for r in self.start_query_request():
            yield r

    def parse(self, response):
        print(response.body)