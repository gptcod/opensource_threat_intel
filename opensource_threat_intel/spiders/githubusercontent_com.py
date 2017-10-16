# -*- coding: utf-8 -*-
# from first.items import FirstItem
import time
from scrapy import Request
from scrapy.spiders import CrawlSpider
from ..items import OpensourceThreatIntelItem

'''
1. 调研不够 https://iplists.firehol.org/
    https://github.com/firehol
    https://github.com/firehol/blocklist-ipsets

'''
class Spider(CrawlSpider):
    name = "TODOgithubusercontent.com"
    allowed_domains = ["githubusercontent.com"]
    start_urls = [
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/botscout_1d.ipset',
        'https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/cruzit_web_attacks.ipset',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 5
        data_type = 0
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                item = OpensourceThreatIntelItem()
                ip = line.split(' ')[0].strip()
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = ip
                item['data_type'] = data_type
                item['tag'] = tag
                item['alive'] = False
                item['description'] = 'none'
                item['confidence'] = 5
                item['source'] = 'githubusercontent.com'
                item['updated_time'] = 'none'
                item['created_time'] = now_time
                yield item

