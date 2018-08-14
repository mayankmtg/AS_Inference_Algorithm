import pymongo
from pymongo import MongoClient
import sys
import Queue 
from Queue import PriorityQueue
import heapq
from utils import surePath, ribin_insert, peers, makePath, makePathArray, valleyFree, bestPath, extendPath


# indexing based on single key, dict get returns list of the values with value as that key
# list is because there are multiple objects with same value for one key
# incomplete but kept for reference


def build_ind_sin(seq,key):
	dic=dict()
	for (index,d) in enumerate(seq):
		if(dic.get(d[key])==None):
			dic[d[key]]=[]
		dic[d[key]].append(dict(d,index=index))
	return dic

# combined indexing based on 2 keys, key1 and key2, separated by '_'
def build_ind_comb(seq,key1,key2):
	return dict((d[key1]+"_"+d[key2], dict(d,index=index)) for (index,d) in enumerate(seq))



client= MongoClient('mongodb://mayank:mayank@192.168.2.75/bgpPaths', 27017)
db=client.bgpPaths

# Graph contains all the paths
Graph=db.bgpGraph
# neighs contains the neighbours 
Neighs=db.bgpNeighs
Ribin=db.bgpRibin
Freq=db.bgpFreq
Rel=db.bgpRel

print("Local Indexing")

Freq_list=list(Freq.find())
Freq_as1_ind=build_ind_sin(Freq_list,"as1")
Freq_as2_ind=build_ind_sin(Freq_list,"as2")
Freq_as1_as2_ind=build_ind_comb(Freq_list, "as1","as2")

Rel_list=list(Rel.find())
Rel_as1_ind=build_ind_sin(Rel_list,"as1")
Rel_as2_ind=build_ind_sin(Rel_list,"as2")
Rel_as1_as2_ind=build_ind_comb(Rel_list, "as1","as2")

print("Indexing Complete")


queue=Queue.Queue()

def INITACTIVEQUEUE(prefix_data):
#	print("initactive")
	baseASset=prefix_data['baseAs']
	for v in baseASset:
		queue.put(v)
		surepath_array=surePath(v, prefix_data['paths'].values())
		for sure in surepath_array:
			res=ribin_insert(Ribin,prefix_data['prefix'],v,sure)
#	print("initactive done")



def KNOWNPATH(prefix_data):
	INITACTIVEQUEUE(prefix_data)
	baseASset=prefix_data['baseAs']
	my_iter=0
	while(queue.qsize()>0):
#		print(my_iter)
		my_iter+=1
		u=queue.get()
		u_neighs=peers(Rel_as1_ind,u)
		for v_neigh in u_neighs:
			v=v_neigh['as2']
			ribin_object=Ribin.find_one({'prefix':prefix_data['prefix'], 'as':u})
			P_u=bestPath(Freq_as1_as2_ind, ribin_object['paths'])
			if (v not in prefix_data['baseAs']) and (v not in makePathArray(P_u)) and (valleyFree(Rel_as1_as2_ind, P_u, v)==1):
				validPath=extendPath(P_u, v)
				tempPath_object=Ribin.find_one({'prefix':prefix_data['prefix'], 'as':v})
				if(tempPath_object==None):
					tempPath_object={
						'paths':[],
						'prefix':prefix_data['prefix'],
						'as':v
					}
				tempPath=bestPath(Freq_as1_as2_ind, tempPath_object['paths'])
				ribin_insert(Ribin, prefix_data['prefix'], v, validPath)
				if(tempPath != bestPath(Freq_as1_as2_ind, tempPath_object['paths']+[validPath])) and (v not in queue.queue):
					queue.put(v)
	

# main method

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python knownpath.py <IP-prefix>")
	sys.exit(0)
	
print("AS-Inference Algorithm\nKnown AS-Paths and BGP Routeviews")
print("Prefix: "+sys.argv[1])


prefix_data=Graph.find_one({'prefix':sys.argv[1]})
KNOWNPATH(prefix_data)

# print makePath(["1", "2", "3", "4", "5"], 2)
