from urllib.error import URLError, HTTPError
from pyspark import SparkContext
import urllib.request
import urllib.parse
import itertools
import json

sc = SparkContext("spark://spark-master:7077", "PopularItems")
sc.setLogLevel("ERROR") # reduce the number of logs printed

data = sc.textFile("/tmp/data/access_log.csv", 2)     		# each worker loads a piece of the data file

pairs = data.map(lambda line: tuple(line.split(","))).distinct()	# (user, item)			

clicks = pairs.groupByKey()		# (user, [item1, item2, ...])

# clickpairs = clicks.map(lambda click: (list(itertools.combinations(click[1],2)), click[0])) 

def iterpairs(click):
  combs = itertools.combinations(click[1],2)
  res = []
  for comb in combs:
  	sorted_comb = (min(comb[0], comb[1]), max(comb[0], comb[1]))
  	res.append((sorted_comb,click[0])) 	# map all pair combos to each user
  return res

clickpairs = clicks.map(iterpairs) 		# ((item1, item2), user); Every row is now a list containing tuples with the same user

# ordered_clickpairs = clickpairs.map(lambda pair: (orderTuple(pair[0]), pair[1])) 

coclicks = clickpairs.flatMap(lambda line: line) 		# expand/flatten the list in every row

coclickers = coclicks.groupByKey().map(lambda x : (x[0], list(x[1]))) 		# ((item1, item2), [user1, user2, ...])

distinct = coclicks.map(lambda pair: (pair[0], len(pair[1]))) 	#((item1, item2), count of distinct users who co-clicked (item1, item2)

distinct = distinct.reduceByKey(lambda x, y: x + y) 	# sum up the counts

massclicks = distinct.filter(lambda pair: pair[1] >= 3) 	# only include pairs with >= 3 coclicks 

output = massclicks.collect()

print("======================================================================================================================")
for item in output:
	print(item)
print(str(output))
print("======================================================================================================================")

sc.stop()

# erase recommendation
print("***erasing previous recommendation records...")
req = urllib.request.Request('http://models:8000/delete_recomm/')
resp_json = urllib.request.urlopen(req).read().decode('utf-8')
resp = json.loads(resp_json)
if 'ok' not in resp.keys():
	print("Error: erase recommendation table")
print(resp)


# organize data into a dict with pairs: (item_id, [coviewed_item_id1, coviewed_item_id2, coviewed_item_id3, ...])
item_recomm = {}
for item in output:
	id1 = int(item[0][0])
	id2 = int(item[0][1])
	if str(id1) in item_recomm:
		item_recomm[str(id1)].append(id2)
	else:
		item_recomm[str(id1)] = [id2]
	if str(id2) in item_recomm:
		item_recomm[str(id2)].append(id1)
	else:
		item_recomm[str(id2)] = [id1]
print("***recommendation records:")
print(item_recomm)

file = open('/tmp/data/recommendation_table.csv', 'w')
for key in item_recomm:
	entry = str(key) + "," + str(item_recomm[key]) + "\n"
	file.write(entry)
file.close()
print("records are written to recommendation_table.csv")


# create Recommendation objects
data = {"data" : json.dumps(item_recomm)}
data = urllib.parse.urlencode(data).encode()
req = urllib.request.Request('http://models:8000/create_recomm/', data=data)
try:
	response = urllib.request.urlopen(req)
except urllib.error.URLError as e:
	print("Error: create Recommendation objects")
	print(e.read().decode("utf8", 'ignore'))
else:
	print("***creating Recommendation objects...")
	resp_json = response.read().decode('utf-8')
	resp = json.loads(resp_json)
	print(resp)


