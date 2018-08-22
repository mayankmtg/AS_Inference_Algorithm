import pymongo
from pymongo import MongoClient
import sys

client= MongoClient('mongodb://mayank:mayank@192.168.2.75/bgpPaths', 27017)
db=client.bgpPaths

Graph=db.bgpGraph
Rel=db.bgpRel



# return 'p' if a is provider of b and 'c', 's' otherwise else returns 'n' if no relation
def relation(a,b):
        # find the relationship of a to b

        rel=Rel.find_one({"as1":a,"as2":b})
        if(rel==None):
                return str('n')
        else:
                return str(rel['rel'])


def check_valley(path_array):
	for p,q,r in zip(path_array[:-2],path_array[1:-1], path_array[2:]):
		rel1=relation(p,q)
		rel2=relation(q,r)

		if(rel1=='p' and rel2=='c'):
			return True
		elif(rel1=='p' and rel2=='s'):
			return True
		elif(rel1=='s' and rel2=='c'):
			return True
		elif(rel1=='s' and rel2=='s'):
			return True
	return False




data=Graph.find()
count=0
for prefix_data in data:
#	print(prefix_data['prefix'])

	paths=prefix_data['paths']
	#print(paths)
	#print(len(paths))

	for pn,p in paths.iteritems():
		p=p.rstrip('|')
		path_array=p.split('|')
		if(check_valley(path_array)):
			count+=1
#			print(p)
#	print(count)
print(count)

