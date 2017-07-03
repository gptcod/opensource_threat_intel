# -*- coding: utf-8 -*-
import os
import re
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/emergingthreat_net'


class Spider(CrawlSpider):
    name = 'emergingthreats.net'

    start_urls = [
        'https://rules.emergingthreats.net/blockrules',
    ]

    rules = (
        Rule(LinkExtractor(allow='/compromised-ips.txt'), callback='parse_line'),
        Rule(LinkExtractor(allow='/emerging-compromised.rules'), callback="parse_regex"),
        Rule(LinkExtractor(allow='/emerging-botcc.excluded'), callback="parse_line"),
        Rule(LinkExtractor(allow='/emerging-compromised.suricata.rules'), callback="parse_regex"),
        Rule(LinkExtractor(allow='/emerging-botcc.rules'), callback="parse_regex"),
        Rule(LinkExtractor(allow='/emerging-botcc.portgrouped.rules'), callback="parse_regex"),
        Rule(LinkExtractor(allow=(r'/emerging-botcc.portgrouped.suricata.rules')), callback="parse_regex"),
        Rule(LinkExtractor(allow=(r'/emerging-tor.rules')), callback="parse_regex"),
        Rule(LinkExtractor(allow=(r'/emerging-tor.suricata.rules')), callback="parse_regex"),
        Rule(LinkExtractor(allow=(r'/emerging-ciarmy.rules')), callback="parse_regex"),
        Rule(LinkExtractor(allow=(r'/emerging-ciarmy.suricata.rules')), callback="parse_regex"),
        Rule(LinkExtractor(allow=(r'/emerging-compromised-BLOCK.rules')), callback="parse_regex"),
    )
    def bak(self, response):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = response.url.split("/")[-1]
        bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        with open(bak_file, 'w') as f:
            f.write(response.body)

    # item数据格式规范
    @staticmethod
    def format_data(indicator, tag):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = indicator
        item['data_type'] = 0
        item['tag'] = tag
        item['alive'] = False
        item['confidence'] = 7
        item['source'] = 'emergingthreats.net'
        item['updated_time'] = 'none'
        item['created_time'] = now_time
        item['description'] = 'none'
        return item
    # 判断数据源的tag类型
    @staticmethod
    def get_tag(url):
        if url.find("compromised") >= 0:
            return  6
        elif url.find("botcc") >= 0:
            return  7
        elif url.find("tor") >= 0:
            return  9
        else:
            return 0

    # 单行IP feed格式解析
    def parse_line(self, response):
        tag = self.get_tag(response.url)
        self.bak(response)
        content = response.body.split('\n')
        content_data = []
        for i in content:
            if i :
                content_data.append(i)
        for indicator in content_data:
            item = self.format_data(indicator, tag)
            yield item
    # 正则匹配IP　feed 解析
    def parse_regex(self, response):
        tag = self.get_tag(response.url)
        self.bak(response)
        content_data = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response.body)
        for indicator in content_data:
            item = self.format_data(indicator,tag)
            yield item

