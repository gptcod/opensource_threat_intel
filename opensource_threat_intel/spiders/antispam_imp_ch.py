# -*- coding: utf-8 -*-
import os
import re
import time
import scrapy
from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/antispam_imp_ch'


class Antispam_Spider(scrapy.Spider):
    name = 'antispam.imp.ch'
    start_urls = ['http://antispam.imp.ch/spamlist']

    def bak(self, response):
        if not os.path.exists(DPATH):
            a = os.system('mkdir -p %s ' % DPATH)
            print a
        bak_file = '%s/%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())) + '-antispam')
        with open(bak_file, 'w') as f:
            f.write(response.body)

    def parse(self, response):
        self.bak(response)
        content = response.body
        ip_name = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', content)
        content_list = content.split('\t')
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
            'Dec': '12'
        }
        content_data = []
        for i in range(0, len(content_list) - 1):
            if content_list[i] in ip_name:
                dic = {}
                dic['ip'] = content_list[i]
                dic_time = content_list[i + 2].split()
                updated_time = dic_time[4] + '-' + month[dic_time[1]] + '-' + dic_time[2].zfill(2) + 'T' + dic_time[3]
                dic['updated_time'] = updated_time
                content_data.append(dic)
            else:
                pass
        for dic in content_data:
            item = OpensourceThreatIntelItem()
            now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
            item['indicator'] = dic['ip']
            item['data_type'] = 0
            item['tag'] = 3
            item['alive'] = True
            item['description'] = 'none'
            item['confidence'] = 9
            item['source'] = 'antispam.imp.ch'
            item['updated_time'] = dic['updated_time']
            item['created_time'] = now_time
            yield item
