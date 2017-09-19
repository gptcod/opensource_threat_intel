# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy import Request
from ..items import OpensourceThreatIntelItem
#from django.conf.urls import url
#from scrapy.linkextractors import LinkExtractor
import time

class Spider(CrawlSpider):
    name = "sshpwauth"
    #allowed_domains = ["dragonresearchgroup.org"]
    start_urls = [
	    'http://dragonresearchgroup.org/insight/sshpwauth.txt',
	]
#    rules = (Rule(LinkExtractor(allow()),callback='parse_1',follow=True),)
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)
            
    def parse_1(self, response):
        tag = 5
        data_type = 0
       # self.bak(response)
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                if line:
                    item = OpensourceThreatIntelItem()
                    indicator = line.split('  |  ')[2]
                   # x=time.localtime()
                    alive_time = line.split('|')[3]
                   # alive_time = time.strftime('%Y-%m-%dT%H:%M:%S', x)
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = indicator
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = True
                    item['description'] = 'none'
                    item['confidence'] = 8
                    item['source'] = 'dragonresearchgroup.org'
                    item['updated_time'] = alive_time
                    item['created_time'] = now_time
                    yield item
