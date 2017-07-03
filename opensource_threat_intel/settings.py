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

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    #'opensource_threat_intel.pipelines.MongoPipeline': 200,
    'opensource_threat_intel.pipelines.JsonWithEncodingPipeline': 300
}
MONGO_HOST='localhost'
MONGO_PORT = 27017
MONGO_DB = 'opensource_threat_intel'
MONGO_COLLECTION = 'data_v1'
