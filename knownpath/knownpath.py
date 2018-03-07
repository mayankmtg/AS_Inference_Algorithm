import pymongo
from pymongo import MongoClient
import sys
import Queue 
from Queue import PriorityQueue
import heapq
from .utils import *


queue=Queue.Queue()

client= MongoClient('localhost', 27017)
db=client.bgpPaths
collection=db.bgpPaths


def INITACTIVEQUEUE(prefix, queue, graph, baseASset):

	for v in baseASset:
		queue.put(v)
		rib_in(v)[p][0] = sure path of v
		SORT(rib in(v)[p])


def KNOWNPATH(prefix):
	queue = Queue()
	INITACTIVEQUEUE(p, queue, G, baseASset)
	while queue.length > 0:
		u ← POP(queue, 0)
		for v ∈ peers(u)
			Pu ← rib in(u)[p][0]
			if v /∈ baseASset and (v) + Pu = ψ:
				tmppath ← rib in(v)[p][0]
				rib in(v)[p] ← rib in(v)[p]  {(v) + Pu}
				SORT(rib in(v)[p])
				if tmppath = path(v)[p][0] and v /∈ queue:
					APPEND(queue, v)
	return {rib in(v)|∀v ∈ V }


# main method

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python knownpath.py <IP-prefix>")
	sys.exit(0)
	
print("AS-Inference Algorithm\nKnown AS-Paths and BGP Routeviews")
print("Prefix: "+sys.argv[1])


prefix_data=collection.find_one({'prefix':sys.argv[1]})
baseAsSet=prefix_data['baseAs']

result=KNOWNPATH(sys.argv[1])
