# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instaparser

    def process_item(self, item, spider):
        # print(f"")
        collection = self.mongo_base[spider.name]
        print(f"collection={collection}, spider.name={spider.name}")
        if collection.count_documents({'user_id': item['user_id'], 'subscribe_user_id': item['subscribe_user_id']}) == 0:
            collection.insert_one(item)
        return item
