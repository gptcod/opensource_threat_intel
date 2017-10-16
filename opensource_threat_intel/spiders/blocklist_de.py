# -*- coding: utf-8 -*-
import os
import re
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/blocklist_de'


class Spider(CrawlSpider):
    name = '005_blocklist.de'

    start_urls = [
        'https://lists.blocklist.de/lists/',
    ]

    rules = (
        Rule(LinkExtractor(allow='/\w+.txt$'), callback='parse_regex'),
        Rule(LinkExtractor(allow='/dnsbl/\w+.list$'), callback='parse_regex'),
        Rule(LinkExtractor(allow=r'/dnsbl'),follow=True),

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
    def format_data(indicator, tag, data_type):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = indicator
        item['data_type'] = data_type
        item['tag'] = tag
        item['alive'] = True
        item['description'] = 'none'
        item['confidence'] = 10
        item['source'] = 'blocklist.de'
        item['updated_time'] = now_time
        item['created_time'] = now_time
        return item

    # 判断数据源的tag类型
    @staticmethod
    def get_tag(url):
        if url.find("email") >= 0 \
                or url.find("mail") >= 0 \
                or url.find("imap") >= 0 \
                or url.find("pop") >= 0:
            return 3
        elif url.find("bot") >= 0:
            return 6
        else:
            return 5


    # 正则匹配IP　feed 解析
    def parse_regex(self, response):
        tag = self.get_tag(response.url)
        self.bak(response)
        ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response.body)
        if ips:
            for indicator in ips:
                if not indicator.startswith('127'):
                    item = self.format_data(indicator, tag, 0)
                    yield item
