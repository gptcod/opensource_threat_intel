# -*- coding: utf-8 -*-
import os
import time

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/osint_bambenekconsulting_com'


class Spider(CrawlSpider):
    name = 'osint_bambenekconsulting_com'

    start_urls = [
        'http://osint.bambenekconsulting.com/feeds/',
    ]

    rules = (
        Rule(LinkExtractor(allow='/c2-dommasterlist.txt'), callback='parse_indicator'),
        Rule(LinkExtractor(allow='/c2-ipmasterlist.txt'), callback='parse_indicator'),
        Rule(LinkExtractor(allow='/dga-feed.txt'), callback='parse_dga'),
    )

    def bak(self, response):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = response.url.split("/")[-1]
        bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        with open(bak_file, 'w') as f:
            f.write(response.body)

    # item数据格式规范
    @staticmethod
    def format_data(line, tag, data_type):
        item = OpensourceThreatIntelItem()
        if line:
            indicator = line.split(',')[0]
            alive_time = line.split(',')[2].replace(' ', 'T') + ':00'
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = indicator
            item['data_type'] = data_type
            item['tag'] = tag
            item['alive'] = True
            # 类型为C&C的描述设置为cc的类型
            item['description'] = line.split(',')[1]
            item['confidence'] = 9
            item['source'] = 'osint.bambenekconsulting.com'
            item['updated_time'] = alive_time
            item['created_time'] = now_time
            return item

    @staticmethod
    def get_data_type(url):
        if url.find('ip') >= 0:
            return 0
        else:
            return 1

    # url ip  c&c feed 解析
    def parse_indicator(self, response):
        tag = 7
        data_type = self.get_data_type(response.url)
        self.bak(response)
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                item = self.format_data(line, tag, data_type)
                yield item
    # dga feed 解析
    def parse_dga(self, response):
        tag = 13
        data_type = 1
        self.bak(response)
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                if line :
                    item = OpensourceThreatIntelItem()
                    indicator = line.split(',')[0]
                    alive_time = line.split(',')[2]+ 'T00:00:00'
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = indicator
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = True
                    #dga 类型
                    item['description'] = line.split(',')[1]
                    item['confidence'] = 9
                    item['source'] = 'osint.bambenekcoGnsulting.com'
                    item['updated_time'] = alive_time
                    item['created_time'] = now_time
                    yield item
