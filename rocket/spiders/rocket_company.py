import json
import logging
import re

import scrapy

logger = logging.getLogger(__name__)

class Spider(scrapy.Spider):
    name = 'rocket_company'
    allowed_domains = []
    key = 'ab52edkd117f699da82a53926b1db64f8a215ed'
    # test account
    # key = 'a4f232k9333d66b17f359eec8b1e4b89de31df6'

    def start_requests(self):
        company_list = [
            '"KBS (Korean Broadcasting System)"',
            '"Voice of America"',
            '"Thomson Reuters"',
            '"Associated Press"',
            'Youmiuri',
            '"Asahi Shinbun"',
            '"Financial Times"',
            '"United Press International"',
            '"Associated Press"',
            '"Bloomberg Lp"',
            '"Nhk, Japan Broadcasting Corporation"',
            '"NHK World Japan"',
            '"The Washington Post"',
            '"WSJ Magazine"',
            '"WSJ the Wall Street Journal Magazine"',
            '"The Wall Street Journal"'
            '"Nbcuniversal Media, LLC"',
            '"The Times"',
            '"Time Magazine"',
            '"NTD Television"',
            '"CNN"',
            '"The Globe and Mail"',
            '"Mirror"',
            '"Epoch Times"',
            '"Kyodo News"',
            '"Chinaaid Association"',
            '"NPR"'
        ]
        for company in company_list:
            url = f"https://api.rocketreach.co/v2/api/search"
            data = {
                "company": company,
                "query":{"current_employer":[company]},
                "start": 1,
                "page_size": 100
            }
            yield scrapy.Request(url, body=json.dumps(data), method="POST", meta=data)


    def parse(self, response):
        company = response.meta["company"]
        start = response.meta["start"]
        page_size = response.meta["page_size"]

        result = json.loads(response.text)
        peoples = result['profiles']
        pagination = result['pagination']

        self.logger.info("URL: %-20s Company: %-50s PAGE: %-3s/%-3s GOT: %-3s people", response.url,  company, int(pagination['start']/page_size)+1,
            int(pagination['total']/page_size), len(peoples))

        for people in peoples:
            # judgement this people is reporter
            current_title = people['current_title']
            if current_title:
                reporter_keywords = re.compile(r'news|writer|reporter|publisher|journalist|photographer|cameraman|correspondent|corresponsal|analyst|producer|Television|Commentator|기자', re.I)
                if reporter_keywords.search(current_title):
                    # self.logger.info("Company: %-40s Title: %-80s PeopleName: %-50s IS Reporter !!", people['current_employer'], people['current_title'], people['name'])
                    url = f"https://api.rocketreach.co/v2/api/lookupProfile?api_key={self.key}&id={people['id']}"
                    yield people
                    # yield scrapy.Request(url, meta={'people': people}, callback=self.profile)
                else:
                    pass
                    # self.logger.info("Company: %-40s Title: %-80s PeopleName: %-50s NOT Reporter ", people['current_employer'], people['current_title'], people['name'])

        if len(peoples) > 0:
            url = f"https://api.rocketreach.co/v2/api/search"
            data = {
                "company": company,
                "query":{"current_employer":[company]},
                "start": start+page_size,
                "page_size": page_size
            }
            yield scrapy.Request(url, body=json.dumps(data),meta=data, method="POST")

    def profile(self, response):
        people = response.meta["people"]
        profile = json.loads(response.text)
        people.update(profile)
        yield people
