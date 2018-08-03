import pymongo
from pymongo import MongoClient
import sys
# import progressbar as pb

# timer = pb.ProgressBar(widgets=widgets, maxval=8100000).start()

client= MongoClient('mongodb://mayank:mayank@192.168.2.75/bgpPaths', 27017)
db=client.bgpPaths
collection=db.bgpRel

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python rel_new.py <relationship-file>")
	sys.exit(0)

with open(sys.argv[1]) as bgp_relations:
	for relation in bgp_relations:
		relation_arr=relation.split('|')
		if(relation_arr[2]=='0'):
			new_relation={
				"as1":relation_arr[0],
				"as2":relation_arr[1],
				"rel":'s'
			}
			collection.insert(new_relation)
			new_relation={
				"as1":relation_arr[1],
				"as2":relation_arr[0],
				"rel":'s'
			}
			collection.insert(new_relation)
		else:
			# 2|3|-1|bpg 2 is the provider and 3 is the customer
			new_relation={
				"as1":relation_arr[0],
				"as2":relation_arr[1],
				"rel":'p'
			}
			collection.insert(new_relation)
			new_relation={
				"as1":relation_arr[1],
				"as2":relation_arr[0],
				"rel":'c'
			}
			collection.insert(new_relation)
