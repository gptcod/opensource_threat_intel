#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/9/26
import os
import time
import json
from scrapy.spiders import CrawlSpider
from ..items import OpensourceThreatIntelItem
DPATH = '../data_bak/cisco_com'
class Spider(CrawlSpider):
    name = 'watchlab'
    start_urls = [
        'http://feed.watcherlab.com/',
    ]
    # item数据格式规范
    @staticmethod
    def format_data(line,data_type,tag):
        item = OpensourceThreatIntelItem()
        indicator = line['indicator']
        lasttime_list = indicator['lasttime'].split(' ')
        update_time = lasttime_list[0] + 'T' + lasttime_list[1]
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = indicator['indicator']
        item['data_type'] = data_type
        item['tag'] = tag
        item['alive'] = True
        item['description'] = 'none'
        item['confidence'] = 9
        item['source'] = 'csirtg.io'
        item['updated_time'] = update_time
        item['created_time'] = now_time
        return item

    def parse_start_url(self, response):
        url = "http://feed.watcherlab.com/watcherlab-2017-09-25.tgz"
        os.system("wget %s" % url)
        os.system("tar -zxf watcherlab-2017-09-25.tgz")


