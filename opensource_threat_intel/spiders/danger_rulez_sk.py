#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/7/25
import time
from scrapy.spiders import CrawlSpider
from ..items import OpensourceThreatIntelItem
DPATH = '../data_bak/public_dns_info'
class Spider(CrawlSpider):
    name = 'danger.rulez.sk'
    start_urls = [
        'http://danger.rulez.sk/projects/bruteforceblocker/blist.php',
    ]
    # item数据格式规范
    @staticmethod
    def format_data(line):
        line2list = line.split('\t')
        update_time = line2list[2].split('#')[-1].strip().replace(' ','T')
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = line2list[0]
        item['data_type'] = 0
        item['tag'] = 5
        item['alive'] = True
        item['description'] = 'none'
        item['confidence'] = 9
        item['source'] = 'danger.rulez.sk'
        item['updated_time'] = update_time
        item['created_time'] = now_time
        return item

    def parse_start_url(self, response):
        lines = response.body.strip().split('\n')
        for line in lines:
            if not  line.startswith('#'):
                yield self.format_data(line)

