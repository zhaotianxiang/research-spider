import scrapy
from scrapy.linkextractors import LinkExtractor

# 定义下载新闻分类的种子
def seed():
    return [
        'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=%25EC%259D%25B4%25EC%25B2%25A0%25ED%2598%25B8&result_filter=user&count=20&query_source=typed_query&cursor=DAAFCgABFNdHWgs__z8LAAIAAADwRW1QQzZ3QUFBZlEvZ0dKTjB2R3AvQUFBQUJRU1pJanYrdFdRQmdBQUFBQWhzUWo1QUFBQUFBa0paS29BQUFBQXB4dDV0UUFBQUFBR291VTRBQUFBQUFscFNVa0FBQUFBdzlrRk1Bd3AzZThmRmFBQUFBQUFBQWFsSXZZQUFBQUFDajE0T2dBQUFBREFldE1VQUFBQUFCVTZxaDRPZVZkRi9oUlFBQlJrQUpUQkdnQURBQUFBQUErczFtQUFBQUFBRWdmUi93QUFBQUFjVlVFY0VDcVhFYzdWQUFJQUFBQUFDYmFFYndBQUFBQURIVlo1AAA&pc=1&spelling_corrections=1&ext=mediaStats%252ChighlightedLabel%252ChasNftAvatar%252CvoiceInfo%252Cenrichments%252CsuperFollowMetadata',
    ]


class Voa(scrapy.Spider):
    name = 'twitter'
    start_urls = seed()

    def parse(self, response):
        self.logger.info("twitter url %s",response.url)
        self.logger.info("response", response.body)
