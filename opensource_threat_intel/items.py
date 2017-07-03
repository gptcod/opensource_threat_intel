# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OpensourceThreatIntelItem(scrapy.Item):
    # define the fields for your item here like:
    indicator = scrapy.Field()
    '''
    data_type : 
        ip          0    
        domain      1
        url         2
        md5         3
    '''
    data_type = scrapy.Field()
    '''
    tags:
    0   Suspicious      可疑的
    1   DDos            DDos攻击
    2   Exploits        漏洞攻击
    3   Spam Sources    垃圾邮件
    4   Web Attacks     Web攻击
    5   Scanners        扫描源
    6   Botnets         僵尸网络被控端
    7   C&C             僵尸网络控制端
    8   Phishing        钓鱼
    9   Proxy           代理
    10  Malware         恶意软件
    11  Whitelist       白名单
    12  Honeypot        蜜罐
    '''
    tag = scrapy.Field()
    source = scrapy.Field()
    '''
    confidence
    (9-10)  Certain
    (7-8)   Very Confident
    (6-7)   Somewhat Confident
    (5-6)   Not Confident
    (5)     "50/50 shot"
    (0-4)   Informational Data
    '''
    confidence = scrapy.Field()
    # 数据源有明确时间戳的，更新为update_time,没有则为none
    updated_time = scrapy.Field()
    # 数据入库时间
    created_time = scrapy.Field()
    '''
    数据源是否有更新属性
    True    有更新属性      
    False   没有更新属性    
    '''
    # 更新机制： 每天根据updated_time更新 昨天写入量用created_time更新
    alive = scrapy.Field()
    description = scrapy.Field()
