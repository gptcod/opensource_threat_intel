#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/7/19
import time
from scrapy.spiders import CrawlSpider
from ..items import OpensourceThreatIntelItem
DPATH = '../data_bak/public_dns_info'
class Spider(CrawlSpider):
    name = '019_public-dns.info'
    start_urls = [
        'https://public-dns.info/nameservers-all.txt',
    ]

    # item数据格式规范
    @staticmethod
    def format_data(line):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = line[0]
        item['data_type'] = 0
        item['tag'] = 11
        item['alive'] = True
        item['description'] = '10000'
        item['confidence'] = 5
        item['source'] = 'public-dns.info'
        item['updated_time'] = now_time
        item['created_time'] = now_time
        return item

    def parse_start_url(self, response):
        lines = response.body.strip().split('\n')
        for line in lines:
            print line
            yield self.format_data(line)
