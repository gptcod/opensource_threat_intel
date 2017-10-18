# -*- coding: utf-8 -*-
import time
import re
from scrapy import Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import OpensourceThreatIntelItem


class Spider(CrawlSpider):
    name = "027_urlvir.com"
    allowed_domains = ["urlvir.com"]
    start_urls = [
        'http://www.urlvir.com/export-ip-addresses',
        'http://www.urlvir.com/export-hosts/',
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,callback=self.parse_1)
                
    def parse_1(self, response):
        tag = 7
        data_type = 0
        lines = response.body.split('\n')
        content = lines[2]
        content_list = content.split(' ')
        month = {
                'January': '01',
                'February': '02',
                'March': '03',
                'April': '04',
                'May': '05',
                'June': '06',
                'July': '07',
                'August': '08',
                'September': '09',
                'October': '10',
                'November': '11',
                'December': '12',
            }
        for line in lines:
            if not str.startswith(line,'#'):
                item = OpensourceThreatIntelItem()
                indicator = line.split(' ')[0].strip()
                if re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', indicator):
                    data_type = 0
                else:
                    data_type = 1
                alive_time = content_list[4][:-1] + '-' + month[content_list[2]] + '-' + content_list[3][:-1] + 'T' + content_list[5] + ':00'
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = indicator
                item['data_type'] = data_type
                item['tag'] = tag
                item['alive'] = True
                item['description'] = 'none'
                item['confidence'] = 8
                item['source'] = 'urlvir.com'
                item['updated_time'] = alive_time
                item['created_time'] = now_time
                yield item
