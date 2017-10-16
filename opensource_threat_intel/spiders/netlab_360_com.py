# -*- coding: utf-8 -*-
import os
import time

from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/netlab_360_com'


class Spider(CrawlSpider):
    name = '014_netlab_360_com'

    allowed_domains = [
        "netlab.360.com"
    ]
    start_urls = [
        # ek
        'http://data.netlab.360.com/feeds/ek/magnitude.txt',
        # dga
        'http://data.netlab.360.com/feeds/dga/proslikefan.txt',
        'http://data.netlab.360.com/feeds/dga/gameover.txt',
        'http://data.netlab.360.com/feeds/dga/fobber.txt',
        'http://data.netlab.360.com/feeds/dga/gspy.txt',
        'http://data.netlab.360.com/feeds/dga/locky.txt',
        'http://data.netlab.360.com/feeds/dga/madmax.txt',
        'http://data.netlab.360.com/feeds/dga/mirai.txt',
        'http://data.netlab.360.com/feeds/dga/murofet.txt',
        'http://data.netlab.360.com/feeds/dga/necurs.txt',
        'http://data.netlab.360.com/feeds/dga/nymaim.txt',
        'http://data.netlab.360.com/feeds/dga/pykspa.txt',
        'http://data.netlab.360.com/feeds/dga/qadars.txt',
        'http://data.netlab.360.com/feeds/dga/ranbyus.txt',
        'http://data.netlab.360.com/feeds/dga/rovnix.txt',
        'http://data.netlab.360.com/feeds/dga/shifu.txt',
        'http://data.netlab.360.com/feeds/dga/simda.txt',
        'http://data.netlab.360.com/feeds/dga/suppobox.txt',
        'http://data.netlab.360.com/feeds/dga/symmi.txt',
        'http://data.netlab.360.com/feeds/dga/tempedreve.txt',
        'http://data.netlab.360.com/feeds/dga/tinba.txt',
        'http://data.netlab.360.com/feeds/dga/tofsee.txt',
        'http://data.netlab.360.com/feeds/dga/vawtrak.txt',
        'http://data.netlab.360.com/feeds/dga/vidro.txt',
    ]

    def start_requests(self):
        for url in self.start_urls:
            if url.find('ek') >=0:
                yield Request(url, callback=self.parse_ek)

            else:
                yield Request(url, callback=self.parse_dga)

    def bak(self, response):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = response.url.split("/")[-1]
        bak_file = '%s/%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        with open(bak_file, 'w') as f:
            f.write(response.body)

    # ek feed 解析
    def parse_ek(self, response):
        tag = 3
        data_type = 0
        self.bak(response)
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                if line:
                    item = OpensourceThreatIntelItem()
                    indicator = line.split('\t')[2]
                    alive_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(int(line.split('\t')[1])))
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = indicator
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = True
                    item['description'] = 'none'
                    item['confidence'] = 10
                    item['source'] = 'netlab.360.com'
                    item['updated_time'] = alive_time
                    item['created_time'] = now_time
                    yield item

    # dga feed 解析
    def parse_dga(self, response):
        tag = 13
        data_type = 1
        self.bak(response)
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                if line:
                    item = OpensourceThreatIntelItem()
                    indicator = line.split('\t')[0]
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = indicator
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = False
                    item['description'] = 'none'
                    item['confidence'] = 10
                    item['source'] = 'netlab.360.com'
                    item['updated_time'] = 'none'
                    item['created_time'] = now_time
                    yield item
