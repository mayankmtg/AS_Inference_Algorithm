import pymongo
from pymongo import MongoClient
import sys
import Queue 
from Queue import PriorityQueue
import heapq
from utils import surePath, ribin_insert, peers, makePath, makePathArray, valleyFree, bestPath, extendPath



client= MongoClient('localhost', 27017)
db=client.bgpPaths

# Graph contains all the paths
Graph=db.bgpGraph
# neighs contains the neighbours 
Neighs=db.bgpNeighs
Ribin=db.bgpRibin
Freq=db.bgpFreq

queue=Queue.Queue()

def INITACTIVEQUEUE(prefix_data):
	baseASset=prefix_data['baseAs']
	for v in baseASset:
		queue.put(v)
		surepath_array=surePath(v, prefix_data['paths'].values())
		for sure in surepath_array:
			res=ribin_insert(Ribin,prefix_data['prefix'],v,sure)



def KNOWNPATH(prefix_data):
	INITACTIVEQUEUE(prefix_data)
	baseASset=prefix_data['baseAs']
	while(queue.qsize()>0):
		u=queue.get()
		u_neighs=peers(Neighs,u)
		for v in u_neighs:
			ribin_object=Ribin.find_one({'prefix':prefix_data['prefix'], 'as':u})
			P_u=bestPath(Freq, ribin_object['paths'])
			if (v not in prefix_data['baseASset']) and (v not in makePathArray) and (valleyFree(Neighs, P_u, v)==1):
				validPath=extendPath(P_u, v)
				tempPath_object=Ribin.find_one({'prefix':prefix_data['prefix'], 'as':v})
				tempPath=bestPath(Freq, tempPath_object['paths'])
				ribin_insert(Ribin, prefix_data['prefix'], v, tempPath)
				if(tempPath != bestPath(tempPath_object['paths']+[validPath])) and (v not in queue.queue):
					queue.put(v)
	

# main method

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python knownpath.py <IP-prefix>")
	sys.exit(0)
	
print("AS-Inference Algorithm\nKnown AS-Paths and BGP Routeviews")
print("Prefix: "+sys.argv[1])


prefix_data=Graph.find_one({'prefix':sys.argv[1]})
print(queue.qsize())
result=KNOWNPATH(prefix_data)

# print makePath(["1", "2", "3", "4", "5"], 2)
