#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/9/8
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import OpensourceThreatIntelItem
import time

class Spider(CrawlSpider):
    name = 'phishtank_com'
    custom_settings = {
        # "DOWNLOADER_MIDDLEWARES": {
        #     'opensource_threat_intel.middlewares.RandomProxyMiddleware': 1
        # },
        "DOWNLOAD_DELAY" :0.5

    
    }
    start_urls = [
        'http://www.phishtank.com/phish_search.php',
        'http://www.phishtank.com/',
    ]


    rules = (
        Rule(LinkExtractor(allow='\?page=\d+')),
        Rule(LinkExtractor(allow='/phish_detail.php\?phish_id=\d+'), callback='parse_detail', follow=True),
    )


    def parse_detail(self, response):
            tag = 8
            data_type = 2
            sel = Selector(response)
            content = sel.xpath('//div[@class="url"]/span[@class="small"]/text()')[0].extract().strip()
            content_list = content.split(' ')
            month = {
                'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12',
            }
            alive_time = content_list[3] + '-' + month[content_list[1]] + '-' + content_list[2][:-2] + 'T' + content_list[4].zfill(5) + ':00'
            item = OpensourceThreatIntelItem()
            url = sel.xpath('//div/span[@style="word-wrap:break-word;"]/b/text()')[0].extract()
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = url
            item['data_type'] = data_type
            item['tag'] = tag
            item['alive'] = True
            item['description'] = 'none'
            item['confidence'] = 9
            item['source'] = 'phishtank.com'
            item['updated_time'] = alive_time
            item['created_time'] = now_time
            yield item