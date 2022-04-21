import json
import re

import pymongo
import scrapy
import whois
from scrapy.selector import Selector


def parse_domain(company):
    company["domain"] = \
        company["company_url"].replace("www.", "").replace("http://", "").replace("https://", "").split('/')[0]
    return company


def json_callback(text=None):
    return text


class Spider(scrapy.Spider):
    name = 'domainsearch'
    done_set = set()
    subnet = False
    port_type_map = {
        '21': 'ftp',
        '22': 'ssh',
        '23': 'telnet',
        '25': 'smtp',
        '53': 'dns',
        '79': '',
        '80': 'http',
        '110': 'pop3',
        '135': '',
        '137': '',
        '138': '',
        '139': '',
        '143': '',
        '443': 'https',
        '1109': '',
        '1521': '',
        '3306': 'mysql',
        '3311': '',
        '3312': '',
        '3389': 'rdp',
        '7000': '',
        '8000': '',
        '8080': 'tomcat',
        '8443': 'tomcats',
        '8888': '',
        '9000': '',
    }

    def start_requests(self):
        self.client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
        self.db = self.client[self.settings.get('MONGO_DB')]
        self.subdomain_list = self.db.subdomain.find_one()["subdomain"]

        for company in list(map(parse_domain, self.db.spider.find({'spider_name': self.name}))):
            url = f"https://micp.chinaz.com/Handle/AjaxHandler.ashx?action=GetBeiansl&callback=json_callback&query={company['domain']}&type=host"
            yield scrapy.Request(url, meta={'company': company}, callback=self.micp)

    def micp(self, response):
        company = response.meta['company']
        prefix = company["company_url"].split(":")[0] + "://"
        result = re.findall(r'(?<=json_callback\(){.*?}(?=\))', response.text)
        icmp_company_list = []
        icmp_company_first = {
            "domain_source": "程序初始化域名",
            "main_page": company['company_url'],
            "site_name": company['company_name'],
            "site_license": None,
            "verify_time": None,
        }
        icmp_company_first.update(company)
        icmp_company_list.append(icmp_company_first)
        if result and len(result) > 0:
            result = result[0]
            result = result.replace("results:", "'results':")
            result = result.replace("SiteLicense:", "'SiteLicense':")
            result = result.replace("SiteName:", "'SiteName':")
            result = result.replace("MainPage:", "'MainPage':")
            result = result.replace("VerifyTime:", "'VerifyTime':")
            if result and len(result) > 10:
                response_json = eval(result)
                self.logger.info("%s 的ICMP备案信息 %s 条", company["company_name"], len(response_json['results']))
                for com in response_json['results']:
                    if com['MainPage'] and len(com['MainPage'].split(';')) > 1:
                        for main_page in com['MainPage'].split(';'):
                            icmp_company = {
                                "domain_source": "icmp备案",
                                "domain_source_url": response.url,
                                "site_license": com['SiteLicense'],
                                "site_name": com['SiteName'],
                                "main_page": prefix + main_page,
                                "verify_time": com['VerifyTime'],
                            }
                            icmp_company.update(company)
                            icmp_company_list.append(icmp_company)
                    icmp_company = {
                        "domain_source": "icmp备案",
                        "domain_source_url": response.url,
                        "site_license": com['SiteLicense'],
                        "site_name": com['SiteName'],
                        "main_page": prefix + com['MainPage'],
                        "verify_time": com['VerifyTime'],
                    }
                    icmp_company.update(company)
                    icmp_company_list.append(icmp_company)
        self.logger.info("%s 根据备案号拓展出来 %s 站点", company["company_name"], len(icmp_company_list))

        for icmp_company in icmp_company_list:
            self.logger.info("站点：%s  待查询的子域名： %s  个", icmp_company["site_name"], len(self.subdomain_list))
            w = whois.whois(icmp_company['main_page'])
            icmp_company["whois"] = w
            icmp_company["whois_domain_name"] = w.domain_name
            icmp_company["whois_registrar"] = w.registrar
            icmp_company["whois_emails"] = w.emails
            icmp_company["whois_name"] = w.name
            if w.emails:
                url = f"https://www.cxw.com/rewhois?checkWhois={w.emails}&type=email"
                yield scrapy.Request(url, meta={
                    "icmp_company": icmp_company
                }, callback=self.rewhois)
            if w.registrar:
                url = f"https://www.cxw.com/rewhois?checkWhois={w.registrar}&type=register"
                yield scrapy.Request(url, meta={
                    "icmp_company": icmp_company
                }, callback=self.rewhois)

            for subdomain in self.subdomain_list:
                icmp_company = icmp_company.copy()
                url = f"https://phpinfo.me/domain/?domain={icmp_company['domain']}&q={subdomain}"
                icmp_company["subdomain_url"] = icmp_company['company_url'].split(':')[0] + "://" + subdomain + "." + \
                                                icmp_company['domain']
                yield scrapy.Request(url, meta={'icmp_company': icmp_company}, callback=self.ipaddress)

    def rewhois(self, response):
        icmp_company = response.meta["icmp_company"].copy()
        icmp_company["domain_source"] = "RE WHOIS"
        icmp_company["domain_source_url"] = response.url
        relist = response.css("body > div.lt-main > div.box > div.mod-table > table > tbody > tr").extract()
        relist_num = response.css("div.page > em::text").extract_first()
        if not relist_num:
            relist_num = len(relist)
            for data in relist:
                icmp_company = icmp_company.copy()
                domain = Selector(text=data).css("td:nth-child(2)::text").extract_first().strip()
                register_company_name = Selector(text=data).css("td:nth-child(3)::text").extract_first()
                register_user_name=  Selector(text=data).css("td:nth-child(4)::text").extract_first()
                register_user_phone=  Selector(text=data).css("td:nth-child(5) *::text").extract_first()

                icmp_company["domain"] = domain
                icmp_company["main_page"] = "https://www."+domain
                for subdomain in self.subdomain_list:
                    icmp_company = icmp_company.copy()
                    url = f"https://phpinfo.me/domain/?domain={icmp_company['domain']}&q={subdomain}"
                    icmp_company["subdomain_url"] = icmp_company['main_page'].split(':')[0] + "://" + subdomain + "." + \
                                                    icmp_company['domain']
                    yield scrapy.Request(url, meta={'icmp_company': icmp_company}, callback=self.ipaddress)
        self.logger.info("%s 域名反查询 %s", response.url, relist_num)

    def generate_subnet_ip(self, ip):
        return list(map(lambda i: '.'.join(ip.split('.')[0:3]) + '.' + str(i), range(1, 256)))

    def ipaddress(self, response):
        response_json = json.loads(response.text)
        meta = response.meta["icmp_company"].copy()
        self.logger.info('  网址域名    %-35s    IP地址    %s    %-5s   %s', meta['subdomain_url'], response_json['ip'],
                         response_json['status'], response.url)

        if response_json['status'] == 200:
            if self.subnet:
                self.logger.warn('是否扫描子网  %s', self.subnet)
                prefix_ip = '.'.join(response_json['ip'].split('.')[0:3])
                if not prefix_ip in self.done_set:
                    self.logger.warning("开始扫描子网扫 %s", response_json['ip'])
                    self.done_set.add(prefix_ip)
                    for ip in self.generate_subnet_ip(response_json['ip']):
                        meta = meta.copy()
                        meta['ip'] = ip
                        for port in self.port_type_map:
                            meta = meta.copy()
                            meta['port'] = port
                            url = f"https://api.yum6.cn/dk.php?ip={meta['ip']}&dk={port}"
                            yield scrapy.Request(url, meta={'gene': meta}, callback=self.ports)
                else:
                    self.logger.warning("子网已经扫描过 %s", response_json['ip'])
            else:
                meta['ip'] = response_json['ip']
                for port in self.port_type_map:
                    meta = meta.copy()
                    meta['port'] = port
                    url = f"https://api.yum6.cn/dk.php?ip={meta['ip']}&dk={port}"
                    yield scrapy.Request(url, meta={'gene': meta}, priority=5, callback=self.ports)
        else:
            pass

    def ports(self, response):
        meta = response.meta["gene"].copy()
        response_json = json.loads(response.text)
        meta['port'] = response_json['dk']
        meta['port_type'] = self.port_type_map[meta['port']]
        meta['is_port_open'] = response_json['state']
        meta['is_login_page'] = 0
        meta['title'] = ''
        self.logger.info('  扫描结果    %-35s   端口:  %-5s  开放:  %s ', meta['ip'], meta['port'], meta['is_port_open'])
        if meta['is_port_open'] == '1':
            yield meta
        if meta['is_port_open'] == '1' and (meta['port'] == '443' or meta['port'] == '80'):
            yield scrapy.Request(meta["subdomain_url"],
                                 meta={'gene': meta},
                                 priority=10,
                                 callback=self.is_login_page)

    def is_login_page(self, response):
        meta = response.meta["gene"].copy()
        meta['subdomain_url'] = response.url
        title = response.css('title::text').extract_first()
        if title and (
                '系统' in title or '登陆' in title or '平台' in title or '邮件' in title or 'Sign' in title or 'Login' in title):
            meta['is_login_page'] = 1
        content = "".join(response.css("*::text").extract())
        if "登陆" in content or 'Sign' in content or 'Login' in content:
            meta['is_login_page'] = 1
        self.logger.info('  判断:  %s  是否登陆页:  %2s   标题： %s', response.url, meta['is_login_page'], title)
        meta['title'] = title
        yield meta
