import pymongo
from pymongo import MongoClient
import sys
import json
import time


# indexing based on single key, dict get returns list of the values with value as that key
# list is because there are multiple objects with same value for one key
# incomplete but kept for reference
#def build_dict(seq, key):
#	return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

def build_dict_sin(seq,key):
	dic=dict()
	for (index,d) in enumerate(seq):
		if(dic.get(d[key])==None):
			dic[d[key]]=[]
		dic[d[key]].append(dict(d,index=index))
	return dic

# combined indexing based on 2 keys, key1 and key2, separated by '_'
def build_dict_comb(seq,key1,key2):
	return dict((d[key1]+"_"+d[key2], dict(d,index=index)) for (index,d) in enumerate(seq))

client= MongoClient('mongodb://mayank:mayank@192.168.2.75/bgpPaths', 27017)
db=client.bgpPaths

# neighs contains the neighbours
Neighs=db.bgpNeighs
Freq=db.bgpFreq
Rel=db.bgpRel

res=list(Rel.find())
print("not sleeping")
print(len(res))
print("sleeping")
time.sleep(1)
print(len(res))

# the result is the proof of mongo giving reference cursor and not copying the values in the ram
# calling the list function here provides access to RAM and thus should reduce computations and time loss in communication
# but the result of this copying and list conversion makes the res contents non-indexed
# Thus indexing must be implemented on our own


