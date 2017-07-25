#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/7/25
import time
import json
from scrapy.spiders import CrawlSpider
from ..items import OpensourceThreatIntelItem
DPATH = '../data_bak/csirtg_io'
class Spider(CrawlSpider):
    name = 'csirtg.io'
    start_urls = [
        'https://csirtg.io/api/users/csirtgadgets/feeds/uce-ip',
        'https://csirtg.io/api/users/csirtgadgets/feeds/uce-urls',
        'https://csirtg.io/api/users/wes/feeds/darknet',
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
        url = response.url
        if 'darknet' in url:
            body_dict = json.loads(response.body)
            indicators = body_dict['feed']['indicators']
            data_type = 0
            tag = 9
            for indicator in indicators:
                yield self.format_data(indicator,data_type,tag)
        elif 'ip' in url:
            body_dict = json.loads(response.body)
            indicators = body_dict['feed']['indicators']
            data_type = 0
            tag = 3
            for indicator in indicators:
                yield self.format_data(indicator,data_type,tag)
        else:
            body_dict = json.loads(response.body)
            indicators = body_dict['feed']['indicators']
            data_type = 2
            tag = 3
            for indicator in indicators:
                yield self.format_data(indicator,data_type,tag)
