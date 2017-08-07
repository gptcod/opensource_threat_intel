#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/8/7
import os
import time

from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/openphish_com'


class Spider(CrawlSpider):
    name = "openphish.com"
    start_urls = [
        "https://openphish.com/feed.txt",
    ]
    # item数据格式规范
    @staticmethod
    def format_data(line):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = line.strip()
        item['data_type'] = 2
        item['tag'] = 8
        item['alive'] = False
        item['description'] = 'none'
        item['confidence'] = 9
        item['source'] = 'openphish.com'
        item['updated_time'] = "none"
        item['created_time'] = now_time
        return item

    def bak(self, response):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = response.url.split("/")[-1]
        bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        with open(bak_file, 'w') as f:
            f.write(response.body)
    def parse_start_url(self, response):
        self.bak(response)
        lines = response.body.strip().split('\n')
        for line in lines:
            if not line.startswith("#"):
                yield self.format_data(line)
