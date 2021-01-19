from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mongo_base = client.instaparser
collection = mongo_base['instagram']


for i in collection.find({"user_id": "2280876151"}):
    print(i)

print('subscribe')
for i in collection.find({"subscribe_user_id": "2280876151"}):
    print(i)

