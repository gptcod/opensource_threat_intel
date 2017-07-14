#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/7/14
import os
import time
from scrapy.spiders import CrawlSpider, Rule
from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/alienvault_com'


class Spider(CrawlSpider):
    name = 'alienvault.com'

    start_urls = [
        'https://reputation.alienvault.com/reputation.data',
    ]


    # item数据格式规范
    @staticmethod
    def format_data(des,indicator, tag, data_type):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = indicator
        item['data_type'] = data_type
        item['tag'] = tag
        item['alive'] = True
        item['description'] = des
        item['confidence'] = 7
        item['source'] = 'alienvault.com'
        item['updated_time'] = now_time
        item['created_time'] = now_time
        return item

    # 判断数据源的tag类型
    @staticmethod
    def get_tag(tag):
        if tag.find('3')>=0:
            return 7
        elif tag.find('12') >=0:
            return 3
        else:
            return 0

    def bak(self, response):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = response.url.split("/")[-1]
        bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        with open(bak_file, 'w') as f:
            f.write(response.body)

    def parse_start_url(self, response):
        self.bak(response)
        for line in response.body.strip().split('\n'):
            indicator = line.split('#')[0]
            description =line.split('#')[3]
            tag = self.get_tag(line.split('#')[-1])
            data_type = 0
            yield self.format_data(description,indicator,tag,data_type)

