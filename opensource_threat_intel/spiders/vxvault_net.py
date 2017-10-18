# -*- coding: utf-8 -*-
import time

from scrapy import Request
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem


class Spider(CrawlSpider):
    name = "021_vxvault.net"
    allowed_domains = ["vxvault.net"]
    start_urls = [
        'http://vxvault.net/URL_List.php',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse_1)

    def parse_1(self, response):
        tag = 7
        data_type = 2
        lines = response.body.split('\n')
        content = lines[2]
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
        for line in lines:
            if str.startswith(line, 'http'):
                if line:
                    item = OpensourceThreatIntelItem()
                    url = line.split(' ')[0].strip()
                    alive_time = content_list[3] + '-' + month[content_list[2]] + '-' + content_list[1] + 'T' + content_list[4]
                    now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                    item['indicator'] = url
                    item['data_type'] = data_type
                    item['tag'] = tag
                    item['alive'] = True
                    item['description'] = 'none'
                    item['confidence'] = 8
                    item['source'] = 'vxvault.net'
                    item['updated_time'] = alive_time
                    item['created_time'] = now_time
                    yield item
