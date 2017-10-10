# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy import Request
from ..items import OpensourceThreatIntelItem
#from django.conf.urls import url
from scrapy.linkextractors import LinkExtractor
import time
from IPy import IP

class Spider(CrawlSpider):
    name = "dragonresearchgroup.org"
    #allowed_domains = ["dragonresearchgroup.org"]
    start_urls = [
	    'http://dragonresearchgroup.org/insight',
	]
    rules = (
        Rule(LinkExtractor(allow='/sshpwauth.txt'),callback='parse_1',follow=True),
        Rule(LinkExtractor(allow='/http-report.txt'), callback='parse_2', follow=True),
    )
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)
            
    def parse_1(self, response):
        tag = 5
        data_type = 0
        lines = response.body.split('\n')
        for line in lines:
            if not str.startswith(line, '#'):
                if line:
                    item = OpensourceThreatIntelItem()
                    ip = line.split('|')[2]
                    alive_time = line.split('|')[3]
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = ip
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = True
                    item['description'] = 'none'
                    item['confidence'] = 9
                    item['source'] = 'dragonresearchgroup.org'
                    item['updated_time'] = alive_time
                    item['created_time'] = now_time
                    yield item
    def parse_2(self, response):
            tag = 5
            data_type = 0
            lines = response.body.split('\n')
            for line in lines:
                if not str.startswith(line, '#'):
                    if line:
                        network = line.split(' | ')[2]
                        ipList = IP(network)
                        for ip in ipList:
                            item = OpensourceThreatIntelItem()
                            alive_time = line.split('|')[3]
                            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                            item['indicator'] =str(ip)
                            item['data_type'] = data_type
                            item['tag'] = tag
                            item['alive'] = True
                            item['description'] = 'none'
                            item['confidence'] = 9
                            item['source'] = 'dragonresearchgroup.org'
                            item['updated_time'] = alive_time
                            item['created_time'] = now_time
                            yield item