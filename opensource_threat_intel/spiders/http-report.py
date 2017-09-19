# -*- coding: utf-8 -*-
import scrapy
#from first.items import FirstItem
from scrapy.spiders import CrawlSpider
from scrapy import Request
from ..items import OpensourceThreatIntelItem
from IPy import IP
import time

class Spider(CrawlSpider):
    name = "http-report"
	#allowed_domains = ["dragonresearchgroup.org"]
    start_urls = [
	    'http://dragonresearchgroup.org/insight/http-report.txt',
	]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)
            
            
    def parse_1(self, response):
            tag = 3
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
