# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
import codecs
import json
from collections import OrderedDict
class MongoPipeline(object):
    def __init__(self):
        connection=pymongo.MongoClient(settings['MONGO_HOST'],settings['MONGO_PORT'])
        self.db=connection[settings['MONGO_DB']]
        self.collection=self.db[settings['MONGO_COLLECTION']]
    def process_item(self, item, spider):
        existing_document = self.collection.find_one({"indicator":item["indicator"],"tag":item["tag"]})
        if not existing_document:
            self.collection.insert({
                "indicator":item["indicator"],                   
                "data_type":item["data_type"],                   
                "tag":item["tag"],                   
                "source":item["source"],                   
                "confidence":item["confidence"],                   
                "alive":item["alive"],
                "description": item['description'],
                "updated_time":item["updated_time"],
                "created_time":item["created_time"],                   
            })
        else:
            self.collection.update( {"indicator":item["indicator"],"tag":item["tag"]},
                                    {
                                        "$set":{
                                             "updated_time":item["updated_time"],                   
                                        }
                                    },
                                    upsert=True)
        return item

class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
