#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/8/7
import time

from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/nothink_org'


class Spider(CrawlSpider):
    name = 'nothink.org'
    start_urls = [
        "http://www.nothink.org/blacklist/blacklist_ssh_day.txt",
    ]
    # item数据格式规范
    @staticmethod
    def format_data(line):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = line.strip()
        item['data_type'] = 0
        item['tag'] = 5
        item['alive'] = False
        item['description'] ='none'
        item['confidence'] = 7
        item['source'] = 'nothink.org'
        item['updated_time'] = 'none'
        item['created_time'] = now_time
        return item

    def parse_start_url(self, response):
        lines = response.body.strip().split('\n')
        for line in lines:
            if not line.startswith("#"):
                yield self.format_data(line)
