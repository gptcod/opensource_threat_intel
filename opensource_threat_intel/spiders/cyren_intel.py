# -*- coding: utf-8 -*-
import gzip
import json
import os
import time
from scrapy import Request
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider

from ..items import OpensourceThreatIntelItem

bak_path = '../data_bak/cyren/'+ time.strftime('%y%m%d', time.localtime(time.time()))+'/'
if not os.path.exists(bak_path):
    os.system('mkdir -p %s ' % bak_path)

class FtpMetaRequest(Request):
    # add user with password to ftp meta request
    user_meta = {'ftp_user': settings['CYREN_FTP_USER'], 'ftp_password': settings['CYREN_FTP_PASS']}

    def __init__(self, args, **kwargs):
        super(FtpMetaRequest, self).__init__(args, **kwargs)
        self.meta.update(self.user_meta)

    def today_time(self):
        return time.strftime('%y%m%d', time.localtime(time.time()))

class FileFtpRequest(FtpMetaRequest):
    pass


class ListFtpRequest(FtpMetaRequest):
    pass


class MedisumSpider(CrawlSpider):
    name = '008_cyren.com'

    allowed_domains = [
        "ftp.ctmail.com"
    ]

    def start_requests(self):
        # start request to get all files
        yield ListFtpRequest("ftp://ftp.ctmail.com/ZombieIntelligence/delta/")
        # yield ListFtpRequest("ftp://ftp.ctmail.com/ZombieIntelligence/snapshot/")

    def parse(self, response):
        # get response with all files
        files = json.loads(response.body)
        # file filter not check md5
        files = filter(lambda dic: dic['filename'].endswith('gz')
                       and dic['filename'].find(self.today_time()) >= 0,files)
        for f in files:
            path = os.path.join(response.url, f['filename'])
            filename = bak_path + f['filename']
            if os.path.exists(filename):
                self.logger.info('file %s exist ..',f['filename'])
                continue
            self.logger.info('start download %s ..', f['filename'])
            request = FileFtpRequest(path,callback=self.parse_item)
            yield request


    def today_time(self):
        return time.strftime('%y%m%d', time.localtime(time.time()))
    # 解压gz文件
    def un_gz(self,file_name):
        """ungz zip file"""
        f_name = file_name.replace(".gz", "")
        # 获取文件的名称，去掉
        g_file = gzip.GzipFile(file_name)
        # 创建gzip对象
        open(f_name, "w+").write(g_file.read())
        # gzip对象用read()打开后，写入open()建立的文件中。
        g_file.close()
        return f_name

    def ip_format(self,ipstr):
        ip_int = reduce(lambda x,y:(x<<8)+y,map(int,ipstr.split('.')))
        tostr = lambda x: '.'.join([str(x/(256**i)%256) for i in range(3,-1,-1)])
        return tostr(ip_int)

    def parse_item(self, response):
        filename = bak_path + response.url.split('/')[-1]
        print filename
        open(filename,'wb').write(response.body)
        self.logger.info('download file  %s ', filename)
        ungz_file = self.un_gz(filename)
        with open(ungz_file, 'r') as ungz:
            os.remove(ungz_file)
            for line in ungz:
                item = OpensourceThreatIntelItem()
                indicator = self.ip_format(line.split(',')[1])
                print indicator
                now_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
                item['indicator'] = indicator
                item['data_type'] = 0
                item['tag'] = 6
                item['alive'] = True
                item['description'] = line.split(',')[6]
                item['confidence'] = 9
                item['source'] = 'cyren.com'
                item['updated_time'] = line.split(',')[3].replace('-','T').replace('T','-',2)
                item['created_time'] = now_time
                yield item
