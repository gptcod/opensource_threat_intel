#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/9/8
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import OpensourceThreatIntelItem


class Spider(CrawlSpider):
    name = 'phishtank_com'
    custom_settings = {
        # "DOWNLOADER_MIDDLEWARES": {
        #     'opensource_threat_intel.middlewares.RandomProxyMiddleware': 1
        # },
        "DOWNLOAD_DELAY" :2

    }
    # start_urls = [
    #     'http://www.phishtank.com/',
    # ]
    #
    # rules = (
    #     Rule(LinkExtractor(allow='/phish_search.php\?page=\d+'), follow=True),
    #     Rule(LinkExtractor(allow='/phish_detail.php\?phish_id=\d+'), callback='parse_detail'),
    # )
    start_urls = [
        'http://www.phishtank.com/phish_search.php',
        'http://www.phishtank.com/',
    ]


    rules = (
        Rule(LinkExtractor(allow='\?page=\d+')),
        Rule(LinkExtractor(allow='/phish_detail.php\?phish_id=\d+'), callback='parse_detail', follow=True),
    )


def parse_detail(self, response):
    url = response.xpath("//*[@id='widecol']/div/div[3]/span/b/text()").extract()[0] + "\n"
    open("data_url","w+").write(url)
    # sel = Selector(response)
    # item = OpensourceThreatIntelItem()
    # item['indicator'] = sel.xpath('//div/span[@style="word-wrap:break-word;"]/b/text()').extract()
    # yield item
