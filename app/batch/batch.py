from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(60)

while True:
    try:
        es = Elasticsearch(['es'])
    except:
        time.sleep(30)
    else:
        break

while True:
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    except:
        time.sleep(10)
    else:
        break

item1 = {"id": 1,
    "seller": "haoranzhu",
    "seller_id": 3,
    "title": "Swipes at Newcomb",
    "content": "Got some swipe to trade at Newcomb dinning hall",
    "pub_date": "2020-03-25T03:13:25.734Z",
    "price": 1.0,
    "remaining_nums": 1,
    "pickup_address": "Anywhere near E-way"}
item2 = {"id": 2,
    "seller": "haoranzhu",
    "seller_id": 3,
    "title": "Cheap swipe at O'Hill",
    "content": "3",
    "pub_date": "2020-03-25T03:23:53.268Z",
    "price": 3.0,
    "remaining_nums": 3,
    "pickup_address": "New dorm"}
item3 = {"id": 3,
    "seller": "haoranzhu",
    "seller_id": 3,
    "title": "50% off plus dollar",
    "content": "I have some plus dollars extra to sell here",
    "pub_date": "2020-03-25T19:25:49.745Z",
    "price": 25.0,
    "remaining_nums": 50,
    "pickup_address": "On grounds only"}
    
es.index(index='listing_index', doc_type='listing', id=item1['id'], body=item1)
es.update(index='listing_index', doc_type='listing', id=item1['id'] , body={ 'script' : 'ctx._source.visits = 10'})
es.index(index='listing_index', doc_type='listing', id=item2['id'], body=item2)
es.update(index='listing_index', doc_type='listing', id=item2['id'] , body={ 'script' : 'ctx._source.visits = 0'})
es.index(index='listing_index', doc_type='listing', id=item3['id'], body=item3)
es.update(index='listing_index', doc_type='listing', id=item3['id'] , body={ 'script' : 'ctx._source.visits = 0'})
es.indices.refresh(index="listing_index")

while True:
    for message in consumer:
        new_item = json.loads((message.value).decode('utf-8'))
        # print(new_item)
        es.index(index='listing_index', doc_type='listing', id=new_item['id'], body=new_item)
        es.update(index='listing_index', doc_type='listing', id=new_item['id'] , body={ 'script' : 'ctx._source.visits = 0'})
        es.indices.refresh(index="listing_index")

