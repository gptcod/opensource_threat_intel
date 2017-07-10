# -*- coding: utf-8 -*-
import json
import os

from scrapy import Request
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider


class FtpMetaRequest(Request):
    # add user with password to ftp meta request
    user_meta = {'ftp_user': settings['CYREN_FTP_USER'], 'ftp_password': settings['CYREN_FTP_PASS']}

    def __init__(self, args, **kwargs):
        super(FtpMetaRequest, self).__init__(args, **kwargs)
        self.meta.update(self.user_meta)



class ListFtpRequest(FtpMetaRequest):
    pass


class MedisumSpider(CrawlSpider):
    name = 'cyren'

    allowed_domains = [
        "ftp.ctmail.com"
    ]

    def start_requests(self):
        # start request to get all files
        yield ListFtpRequest("ftp://ftp.ctmail.com/ZombieIntelligence/delta/")

    def parse(self, response):
        # get response with all files
        files = json.loads(response.body)
        # file filter not check md5
        files = filter(lambda dic: dic['filename'].endswith('gz'), files)
        for f in files:
            path = os.path.join(response.url, f['filename'])
            request = Request(path,
                              callback=self.parse_item,
                              meta={'ftp_user': settings['CYREN_FTP_USER'], 'ftp_password': settings['CYREN_FTP_PASS']})
            yield request
            break

    def parse_item(self, response):
        open('a.dat.gz','wb').write(response.body)
