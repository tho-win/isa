from pyspark import SparkContext
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

# ordered_clickpairs = clickpairs.map(lambda pair: (orderTuple(pair[0]), pair[1])) 	# reorder (item1, item2) so that (3,4) = (4,3)

coclicks = clickpairs.flatMap(lambda line: line) 		# expand/flatten the list in every row

coclickers = coclicks.groupByKey().map(lambda x : (x[0], list(x[1]))) 		# ((item1, item2), [user1, user2, ...])

distinct = coclicks.map(lambda pair: (pair[0], len(pair[1]))) 	#((item1, item2), count of distinct users who co-clicked (item1, item2)

distinct = distinct.reduceByKey(lambda x, y: x + y) 	# sum up the counts

massclicks = distinct.filter(lambda pair: pair[1] >= 3)

output = distinct.collect()

print("======================================================================================================================")
for item in output:
	print(item)
print(str(output))
print("======================================================================================================================")

sc.stop()