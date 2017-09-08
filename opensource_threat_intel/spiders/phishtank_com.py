#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/9/8

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule



class Spider(CrawlSpider):
    name = 'phishtank_com'

    start_urls = [
        'http://www.phishtank.com/',
    ]

    rules = (
        Rule(LinkExtractor(allow='/phish_search.php\?page=\d+'), follow= True),
        Rule(LinkExtractor(allow='/phish_detail.php\?phish_id=\d+'), callback='parse_detail',follow= True),
    )


    def parse_detail(self,response):
       print  response.xpath("//*[@id='widecol']/div/div[3]/span/b/text()").extract()[0]
