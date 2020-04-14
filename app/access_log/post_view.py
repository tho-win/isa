from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(120)

while True:
    try:
        es = Elasticsearch(['es'])
    except:
        time.sleep(30)
    else:
        break

while True:
    try:
        consumer = KafkaConsumer('listing-view-topic', group_id='view-counter', bootstrap_servers=['kafka:9092'])
    except:
        time.sleep(10)
    else:
        break

with open('access_log.csv', 'a') as file:
    while True:
        for message in consumer:
            new_item = json.loads((message.value).decode('utf-8'))
            es.update(index='listing_index', doc_type='listing', id=new_item['listing_id'] , body={ 'script' : 'ctx._source.visits += 1'})
            es.indices.refresh(index="listing_index")
            entry = str(new_item['user_id']) + "," + str(new_item['listing_id']) + "\n"
            file.write(entry)

