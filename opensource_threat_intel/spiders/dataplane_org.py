#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/8/7


import time

from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/dataplane_org'


class Spider(CrawlSpider):
    name = '010_dataplane.org'
    start_urls = [
    "https://dataplane.org/sshclient.txt",
    "https://dataplane.org/sshpwauth.txt",
    "https://dataplane.org/sipquery.txt",
    "https://dataplane.org/sipinvitation.txt",
    "https://dataplane.org/sipregistration.txt",

    "https://dataplane.org/dnsrd.txt",
    "https://dataplane.org/dnsrd.txt",
    "https://dataplane.org/dnsversion.txt",
    "https://dataplane.org/vncrfb.txt",
    ]
    # item数据格式规范
    @staticmethod
    def format_data(line):
        item = OpensourceThreatIntelItem()
        its = line.split("|")
        updated_time = its[3].strip().replace(" ","T")
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = its[2].strip()
        item['data_type'] = 0
        item['tag'] = 5
        item['alive'] = True
        item['description'] = its[-1].strip()
        item['confidence'] = 5
        item['source'] = 'dataplane.org'
        item['updated_time'] = updated_time
        item['created_time'] = now_time
        return item

    def parse_start_url(self, response):
        lines = response.body.strip().split('\n')
        for line in lines:
            if not line.startswith("#"):
                print line
                yield self.format_data(line)
