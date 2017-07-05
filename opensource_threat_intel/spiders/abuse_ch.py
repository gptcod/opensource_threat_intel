# -*- coding: utf-8 -*-
import os
import time

from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/abuse_sh'


class Spider(CrawlSpider):
    name = 'abuse.sh'

    allowed_domains = [
        "abuse.sh"
    ]
    start_urls = [
        # sslbl.abuse.ch
        'https://sslbl.abuse.ch/blacklist/sslblacklist.csv',
    ]

    def start_requests(self):
        for url in self.start_urls:
            if url.find('sslbl') >= 0:
                yield Request(url, callback=self.reduce_sslbl)

    def bak(self, url, site):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = url.split("/")[-1]
        bak_file = '%s/%s%s%s' % (DPATH, site, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        cmd = " wget  -c '%s'  -O %s" % (url, bak_file)
        print cmd
        os.system(cmd)
        return bak_file

    # sslbl feed 解析
    def reduce_sslbl(self, response):
        file_path = self.bak(response.url, 'sslbl')
        if response.url.find('sslblacklist') >= 0:
            self.parse_sha1(file_path)

    @staticmethod
    def parse_sha1(file_path):
        print  file_path
        tag = 7
        data_type = 5
        with open(file_path, 'r') as f:
            for line in f:
                print line
                if not line.startswith('#'):
                    item = OpensourceThreatIntelItem()
                    indicator = line.split(',')[1]
                    alive_time = line.split(',')[0].replace(' ', 'T')
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = indicator
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = True
                    item['description'] = line.split(',')[2]
                    item['confidence'] = 9
                    item['source'] = 'sslbl.abuse.ch'
                    item['updated_time'] = alive_time
                    item['created_time'] = now_time
                    yield item
