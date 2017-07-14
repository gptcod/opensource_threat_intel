#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/7/14
import os
import time
import urllib
import zipfile

from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/alexa_com'


class Spider(CrawlSpider):
    name = 'alexa.com'

    start_urls = [
        'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip',
    ]

    # item数据格式规范
    @staticmethod
    def format_data(des, indicator, tag, data_type):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = indicator
        item['data_type'] = data_type
        item['tag'] = tag
        item['alive'] = True
        item['description'] = des
        item['confidence'] = 7
        item['source'] = 'alexa.com'
        item['updated_time'] = now_time
        item['created_time'] = now_time
        return item

    # 判断数据源的tag类型
    @staticmethod
    def get_tag(tag):
        if tag.find('3') >= 0:
            return 7
        elif tag.find('12') >= 0:
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

    def start_requests(self):
        for url  in self.start_urls:
            if not os.path.exists(DPATH):
                os.system('mkdir -p %s ' % DPATH)
            filename = url.split("/")[-1]
            bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
            if not os.path.exists(bak_file):
                urllib.urlretrieve (url, bak_file)
            else:
                pass
            print bak_file
            with zipfile.ZipFile(bak_file,"r") as zip_ref:
                bak_dir = '%s/%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())))
                zip_ref.extractall(bak_dir)
                print  bak_dir
                print zip_ref



