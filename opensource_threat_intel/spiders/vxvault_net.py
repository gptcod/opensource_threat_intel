# -*- coding: utf-8 -*-
import time

from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem


class Spider(CrawlSpider):
    name = "vxvault.net"
    allowed_domains = ["vxvault.net"]
    start_urls = [
        'http://vxvault.net/URL_List.php',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 7
        data_type = 2
        lines = response.body.split('\n')
        for line in lines:
            if str.startswith(line, 'http'):
                if line:
                    item = OpensourceThreatIntelItem()
                    url = line.split(',')[0].strip()
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = url
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = False
                    item['description'] = 'none'
                    item['confidence'] = 10
                    item['source'] = 'phishtank.com'
                    item['updated_time'] = 'none'
                    item['created_time'] = now_time
                    yield item
