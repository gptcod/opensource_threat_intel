#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Created by manue1 on 2017/7/14
import csv
import os
import time
import tarfile
import gzip

from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

DPATH = '../data_bak/watcherlab/'

class Spider(CrawlSpider):
    name = '022_watcherlab.com'

    start_urls = [
        'http://feed.watcherlab.com/',
    ]

    # item数据格式规范
    @staticmethod
    def format_data(line):
        item = OpensourceThreatIntelItem()
        now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        item['indicator'] = line.split(',')[1]
        item['data_type'] = 1
        item['tag'] = 10
        item['alive'] = True
        # 这里白名单的描述 为watcherlab排名
        item['description'] = 'none'
        item['confidence'] = 9
        item['source'] = 'watcherlab.com'
        item['updated_time'] = line.split(',')[2].replace(' ','T')
        item['created_time'] = now_time
        return item

    def parse_start_url(self, response):
        download_url = ["http://feed.watcherlab.com/watcherlab-%s.tgz" % time.strftime('%Y-%m-%d', time.localtime(time.time()-24*60*60))]
        url = download_url[0]
        bak_dir = '%s%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())))
        #创建存放tar.gz 的当天文件夹
        if not os.path.exists(bak_dir):
            os.system('mkdir -p %s ' % bak_dir)
            print "create dir success" ,bak_dir
        filename = url.split("/")[-1]
        #tag.gz 文件名
        bak_file = '%s%s/%s' % (DPATH, time.strftime('%Y-%m-%d', time.localtime(time.time())), filename)
        # 当天下载操作
        if not os.path.exists(bak_file):
            cmd = " wget  -c '%s'  -O %s" % (url, bak_file)
            os.system(cmd)
            print "download success"
        else:
            pass

        print "文件名:" ,  bak_file
        #解压
        if os.path.exists(bak_file):
            cmd = "tar -zxvf %s -C %s" %(bak_file,bak_dir)
            os.system(cmd )
            print "解压成功"
        else:
            pass
        dir_txt = bak_dir + "/" + "watcherlab-%s" % time.strftime('%Y-%m-%d', time.localtime(time.time()-24*60*60))
        if os.path.exists(dir_txt):
            txt_file_1 =dir_txt + '/' + 'watcherlab-tor-%s.txt' % time.strftime('%Y-%m-%d', time.localtime(time.time()-24*60*60))
            print txt_file_1
            txt_file_2 =dir_txt + '/' + 'watcherlab-proxy-%s.txt' % time.strftime('%Y-%m-%d', time.localtime(time.time()-24*60*60))
            print txt_file_2
            with open(txt_file_1,'r') as f:
                for line in f:
                    #print line
                    pass
                    item = self.format_data(line)
                    yield item
            with open(txt_file_2,'r') as f:
                for line in f:
                    #print line
                    pass
                    item = self.format_data(line)
                    yield item
