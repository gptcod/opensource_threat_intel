# -*- coding: utf-8 -*-
# from first.items import FirstItem
import time

from IPy import IP
from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem


class Spider(CrawlSpider):
    name = "020_spamhaus.org"
    allowed_domains = ["spamhaus.org"]
    start_urls = [
        'http://www.spamhaus.org/drop/drop.txt',
        'http://www.spamhaus.org/drop/edrop.txt',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 3
        data_type = 0
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, ';'):
                if line:
                    network = line.split(' ; ')[0]
                    ipList = IP(network)
                    for ip in ipList:
                        item = OpensourceThreatIntelItem()
                        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                        item['indicator'] = str(ip)
                        item['data_type'] = data_type
                        item['tag'] = tag
                        item['alive'] = False
                        item['description'] = 'none'
                        item['confidence'] = 9
                        item['source'] = 'www.spamhaus.org'
                        item['updated_time'] = 'none'
                        item['created_time'] = now_time
                        yield item
