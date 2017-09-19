# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy import Request
from ..items import OpensourceThreatIntelItem
from scrapy.selector import Selector
#from django.conf.urls import url
from scrapy.linkextractors import LinkExtractor
import time

class Spider(CrawlSpider):
    name = "phishtank"
    #allowed_domains = ["phishtank.com"]
    start_urls = [
        'http://www.phishtank.com/phish_search.php',
	    'http://www.phishtank.com/',
	]
    rules = (
        Rule(LinkExtractor(allow='\?page=\d+')),
        Rule(LinkExtractor(allow='/phish_detail.php\?phish_id=\d+'),callback='parse_1',follow=True),
    )
    
        
    def parse_1(self, response):
            sel = Selector(response)
            item = OpensourceThreatIntelItem()
            item['indicator'] = sel.xpath('//div/span[@style="word-wrap:break-word;"]/b/text()').extract()
            yield item

    def parse_2(self,response):
            pass
    
