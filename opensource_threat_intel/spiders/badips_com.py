# -*- coding: utf-8 -*-
import time

from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem


class Spider(CrawlSpider):
    name = "023_badips.com"
    allowed_domains = ["badips.com"]
    start_urls = [
        'https://www.badips.com/get/list/any/2?age=7d',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 0
        data_type = 0
        lines = response.body.split('\n')
        for line in lines:
            if line:
                item = OpensourceThreatIntelItem()
                ip = line.split(' ')[0].strip()
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = ip
                item['data_type'] = data_type
                item['tag'] = tag
                item['alive'] = False
                item['description'] = 'none'
                item['confidence'] = 5
                item['source'] = 'badips.com'
                item['updated_time'] = 'none'
                item['created_time'] = now_time
                yield item
