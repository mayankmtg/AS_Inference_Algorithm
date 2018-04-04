import pymongo
from pymongo import MongoClient
import sys
import Queue 
from Queue import PriorityQueue
import heapq
from utils import surePath, ribin_insert, peers



client= MongoClient('localhost', 27017)
db=client.bgpPaths
Graph=db.bgpGraph
Neighs=db.bgpNeighs
Ribin=db.bgpRibin

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
	while(queue.qsize()>0):
		u=queue.get()
		u_neighs=peers(Neighs,u)
		for v in u_neighs:
			


	


# main method

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python knownpath.py <IP-prefix>")
	sys.exit(0)
	
print("AS-Inference Algorithm\nKnown AS-Paths and BGP Routeviews")
print("Prefix: "+sys.argv[1])


prefix_data=Graph.find_one({'prefix':sys.argv[1]})
print(queue.qsize())
result=KNOWNPATH(prefix_data)
