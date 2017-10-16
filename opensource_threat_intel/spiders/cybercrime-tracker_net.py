# -*- coding: utf-8 -*-
import time
from scrapy import Selector
from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem
import time

class Spider(CrawlSpider):
    name = "TODO_cybercrime-tracker.net"
    allowed_domains = ["cybercrime-tracker.net"]
    start_urls = [
        '''
        TODO
            1.http://cybercrime-tracker.net/index.php?s=160&m=40
                翻页爬取  ip tag=10
                url tag =0

            2.'http://cybercrime-tracker.net/ccam.php',
                页面内的数据 既存在domain 又存在ip 加一个判断 不是ip 就是domain
                md5 信息也提取出来 tag=10
        '''
        'http://cybercrime-tracker.net/ccam.php',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 10
        data_type = 1
        sel = Selector(response)
        trs = sel.xpath('//*[@height="85"]/tbody/tr[@class="monitoring"]')
        for i in range(0,len(trs)):
            item = OpensourceThreatIntelItem()
            tr = trs[i]
            content = tr.xpath('string(td[2])')[0].extract().strip()
            content_list = content.split(' ')
            content_list_num = content_list[0].split('/')
            alive_time = content_list_num[2] + '-' + content_list_num[1] + '-' + content_list_num[0] + 'T' + content_list[1]
            indicator = tr.xpath('string(td[3])')[0].extract().strip()

            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = indicator
            item['data_type'] = data_type
            item['tag'] = tag
            item['alive'] = True
            item['description'] = 'none'
            item['confidence'] = 5
            item['source'] = 'cybercrime-tracker.net'
            item['updated_time'] = alive_time
            item['created_time'] = now_time
            yield item
