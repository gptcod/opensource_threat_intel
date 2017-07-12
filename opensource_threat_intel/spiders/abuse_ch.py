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
        'https://sslbl.abuse.ch/blacklist/dyre_sslblacklist.csv',
        'https://sslbl.abuse.ch/blacklist/sslblacklist.csv',
        'https://sslbl.abuse.ch/blacklist/sslipblacklist.csv',
        'https://sslbl.abuse.ch/blacklist/sslipblacklist_aggressive.csv',
        'https://sslbl.abuse.ch/blacklist/dyre_sslipblacklist.csv',
        # zeustracker.abuse.ch
        'https://zeustracker.abuse.ch/blocklist.php?download=baddomains',
        'https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist',
        'https://zeustracker.abuse.ch/blocklist.php?download=badips',
        'http://zeustracker.abuse.ch/blocklist.php?download=ipblocklist',
        # feodotracker.abuse.ch
        'https://feodotracker.abuse.ch/blocklist/?download=ipblocklist',
        'https://feodotracker.abuse.ch/blocklist/?download=domainblocklist',
        #ransomware.abuse.ch
        'http://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt',
        'http://ransomwaretracker.abuse.ch/downloads/RW_URLBL.txt',
        'http://ransomwaretracker.abuse.ch/downloads/RW_IPBL.txt',

    ]

    def start_requests(self):
        for url in self.start_urls:
            if url.find('sslbl') >= 0:
                yield Request(url, callback=self.reduce_sslbl)
            elif url.find('zeustracker') >= 0:
                yield Request(url, callback=self.reduce_zeustracker)
            elif url.find('feodotracker')>=0:
                yield Request(url, callback=self.reduce_feodotracker)
            elif url.find('ransomwaretracker')>=0:
                yield Request(url, callback=self.reduce_ransomwaretracker)
            else:
                pass


    def sslbl_bak(self, url, site):
        if not os.path.exists(DPATH):
            os.system('mkdir -p %s ' % DPATH)
        filename = url.split("/")[-1]
        bak_file = '%s/%s%s%s' % (DPATH, site, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        cmd = " wget  -c '%s'  -O %s" % (url, bak_file)
        os.system(cmd)
        return bak_file

    # sslbl feed 解析
    def reduce_sslbl(self, response):
        file_path = self.sslbl_bak(response.url, 'sslbl')
        if response.url.find('sslblacklist') >= 0:
            with open(file_path, 'r') as f:
                for line in f:
                    if not line.startswith('#'):
                        yield self.parse_sha1(line.strip())
        elif response.url.find('sslipblacklist') >=0:
            with open(file_path,'r') as f:
                for line in f:
                    if not line.startswith('#'):
                        yield self.parse_ip(line.strip())


    # feed 解析
    def reduce_zeustracker(self, response):
        url = response.url
        if url.find('domain')>=0 :
            data_type = 1
            tags = 10
        elif url.find('ip')>=0 :
            data_type = 0
            tags = 10
        elif url.find('compromised')>=0 :
            data_type = 2
            tags = 6
        for line in response.body.strip().split('\n'):
            if not line.startswith('#'):
                item = OpensourceThreatIntelItem()
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = line
                item['data_type'] = data_type
                item['tag'] = tags
                item['alive'] = False
                item['description'] = 'ZeuS'
                item['confidence'] = 9
                item['source'] = 'zeustracker.abuse.ch'
                item['updated_time'] = 'none'
                item['created_time'] = now_time
                yield item

    # feed 解析
    def reduce_feodotracker(self, response):
        url = response.url
        if url.find('domain')>=0 :
            data_type = 1
            tags = 10
        elif url.find('ip')>=0 :
            data_type = 0
            tags = 10
        for line in response.body.strip().split('\n'):
            if not line.startswith('#'):
                item = OpensourceThreatIntelItem()
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = line
                item['data_type'] = data_type
                item['tag'] = tags
                item['alive'] = True
                item['description'] = 'feodotracker'
                item['confidence'] = 8
                item['source'] = 'feodotracker.abuse.ch'
                item['updated_time'] = now_time
                item['created_time'] = now_time
                yield item


    # feed 解析
    def reduce_ransomwaretracker(self, response):
        url = response.url
        if url.find('DOM')>=0 :
            data_type = 1
            tags = 10
        elif url.find('IP')>=0 :
            data_type = 0
            tags = 10
        elif url.find('URL')>=0 :
            data_type = 2
            tags = 10
        for line in response.body.strip().split('\n'):
            if not line.startswith('#'):
                item = OpensourceThreatIntelItem()
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = line
                item['data_type'] = data_type
                item['tag'] = tags
                item['alive'] = True
                item['description'] = 'ransomware'
                item['confidence'] = 8
                item['source'] = 'ransomware.abuse.ch'
                item['updated_time'] = now_time
                item['created_time'] = now_time
                yield item
    def parse_ip(self, line):
        tag = 10
        data_type = 0
        item = OpensourceThreatIntelItem()
        indicator = line.split(',')[0]
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = indicator
        item['data_type'] = data_type
        item['tag'] = tag
        item['alive'] = True
        item['description'] = line.split(',')[2]
        item['confidence'] = 9
        item['source'] = 'sslbl.abuse.ch'
        item['updated_time'] = now_time
        item['created_time'] = now_time
        return item

    def parse_sha1(self, line):
        tag = 10
        data_type = 5
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
        return item
