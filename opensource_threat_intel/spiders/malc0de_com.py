#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/8/7
import os
import re

from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem
DPATH = '../data_bak/malc0de_com'


class Spider(CrawlSpider):
    name = '013_malc0de.com'
    allowed_domains = [
        "malc0de.com"
    ]
    start_urls = [
        "http://malc0de.com/rss/",
    ]


    # item数据格式规范
    @staticmethod
    def format_data(ip):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = ip
        item['data_type'] = 0
        item['tag'] = 7
        item['alive'] = False
        item['description'] = 'none'
        item['confidence'] = 9
        item['source'] = 'malc0de.com'
        item['updated_time'] = 'none'
        item['created_time'] = now_time
        return item
    @staticmethod
    def bak(response):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = response.url.split("/")[-1]
        bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        with open(bak_file, 'w') as f:
            f.write(response.body)

    def parse_start_url(self, response):
        self.bak(response)
        content_data = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response.body)
        for ip in content_data:
                yield self.format_data(ip)

