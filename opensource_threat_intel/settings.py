# -*- coding: utf-8 -*-

# Scrapy settings for opensource_threat_intel project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'opensource_threat_intel'
SPIDER_MODULES = ['opensource_threat_intel.spiders']
NEWSPIDER_MODULE = 'opensource_threat_intel.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    #'opensource_threat_intel.pipelines.MongoPipeline': 200,
    'opensource_threat_intel.pipelines.JsonWithEncodingPipeline': 300,
}
#  运行环境采用info级别
LOG_LEVEL = 'INFO'
#  下载大文件的时候，设置延时时间300s
DOWNLOAD_TIMEOUT = 300
#  文件内容防爬0.25秒延时请求
DOWMLOAD_DELY = 1
# 请求失败再次尝试
RETRY_ENABLED = False
# RETRY_TIMES = 1

# 默认32线程并发
CONCURRENT_REQUESTS = 32

DOWNLOAD_HANDLERS = {'ftp': 'opensource_threat_intel.ftp.FtpListingHandler'}

DOWNLOADER_MIDDLEWARES = {
        'opensource_threat_intel.middlewares.OpensourceThreatIntelSpiderMiddleware':None,
        'opensource_threat_intel.middlewares.RandomUserAgent':1
}


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0)",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
]

##########################

MONGO_HOST='localhost'
MONGO_PORT = 27017
MONGO_DB = 'opensource_threat_intel'
MONGO_COLLECTION = 'data_v1'
# cyren ftp
CYREN_FTP_USER = ''
CYREN_FTP_PASS = ''
