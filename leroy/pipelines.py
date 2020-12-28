# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroyMerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print(f"item={item}")
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        print(f"results={results}")
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        print(f"item_completed={item}")
        return item


    def file_path(self, request, response=None, info=None, *, item=None):
        dir = str(item['name'])
        image_guid = request.url.split('/')[-1]
        return  'full/%s/%s' % (dir, image_guid)





class LeroyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        dict_charac = {}
        item['characteristic'] = []
        print("type")
        print(type(item['name']))
        try:
            for i in range(len(item['characteristic_key'])):
                dict_charac = (item['characteristic_key'][i], item['characteristic_val'][i].replace('\n', '').replace('                ', '').replace('            ', ''))
                item['characteristic'].append(dict_charac)
        except Exception as e:
            print(e)
        del item['characteristic_key']
        del item['characteristic_val']
        print(f"LeroyPipeline={item}")
        collection.insert_one(item)
        return item
