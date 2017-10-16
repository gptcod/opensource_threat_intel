# -*- coding: utf-8 -*-
import time
from scrapy import Selector
from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem


#TODO 加代理
class Spider(CrawlSpider):
    name = "TODO_maxmind.com"
    allowed_domains = ["maxmind.com"]
    start_urls = [
        'https://www.maxmind.com/en/high-risk-ip-sample-list',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 0
        data_type = 0
        sel = Selector(response)
        a_s = sel.xpath("//*[@id='content']/p[@class='row']/a[@class='span3']")
        for i in range(0,len(a_s)):
            item = OpensourceThreatIntelItem()
            a = a_s[i]
            #ip = a.xpath('text()')[0].extract().strip()
            ip = a.xpath('string(.)').extract()[0]
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = ip
            item['data_type'] = data_type
            item['tag'] = tag
            item['alive'] = False
            item['description'] = 'none'
            item['confidence'] = 5
            item['source'] = 'maxmind.com'
            item['updated_time'] = 'none'
            item['created_time'] = now_time
            yield item
