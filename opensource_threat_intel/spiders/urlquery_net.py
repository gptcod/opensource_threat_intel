#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/9/8
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from ..items import OpensourceThreatIntelItem
import time

class Spider(CrawlSpider):
    name = '028_urlquery.net'
    start_urls = [
        'https://urlquery.net/',
    ]

    rules = (
        Rule(LinkExtractor(allow='/report\S+'),callback='parse_1', follow=True),

    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse_1(self, response):
            sel = Selector(response)
            ip = sel.xpath('//*[@id="main"]/section/table[1]/tbody/tr[2]/td[2]/text()')[0].extract()
            url = sel.xpath('//*[@id="main"]/section/table[1]/tbody/tr[1]/td[2]/text()')[0].extract()
            alive_time = sel.xpath('//*[@id="main"]/section/table[1]/tbody/tr[5]/td[2]/text()')[0].extract().replace(' ','T')[:-5]


            # IP 作为ID
            data_type = 0
            tag = 7
            item = OpensourceThreatIntelItem()
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = ip
            item['data_type'] = data_type
            item['tag'] = tag
            item['alive'] = True
            item['description'] = url
            item['confidence'] = 5
            item['source'] = 'urlquery.net'
            item['updated_time'] = alive_time
            item['created_time'] = now_time
            yield item


            #url 作为ID
            data_type = 2
            tag = 7
            item = OpensourceThreatIntelItem()
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = url
            item['data_type'] = data_type
            item['tag'] = tag
            item['alive'] = True
            item['description'] = ip
            item['confidence'] = 5
            item['source'] = 'urlquery.net'
            item['updated_time'] = alive_time
            item['created_time'] = now_time
            yield item


