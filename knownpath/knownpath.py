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
Graph=db.bgpPaths
Neighs=db.bgpNeighs



def valleyFree(path, extended_AS):
	path_length=len(path)
	



def INITACTIVEQUEUE(prefix, queue, graph, baseASset):

	for v in baseASset:
		queue.put(v)
		rib_in(v)[p][0] = sure path of v
		SORT(rib in(v)[p])

def peers(u):
	# return a tupple of neighbour and type of neighbour
	peers=Neighs.find_one({'as':u})
	peer_tupples=[]
	siblings=peers['neighbours']['siblings']
	customers=peers['neighbours']['customers']
	providers=peers['neighbours']['providers']
	for sibling in siblings:
		peer_tupples.append((sibling, 's'))
	for customer in customers:
		peer_tupples.append((customer, 'c'))
	for provider in providers:
		peer_tupples.append((provider, 'p'))

	return peer_tupples


def KNOWNPATH(prefix):
	queue = Queue()
	INITACTIVEQUEUE(p, queue, G, baseASset)
	while queue.length > 0:
		u=queue.get()
		neighbours=peers(u)
		for v in neighbours:
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


prefix_data=Graph.find_one({'prefix':sys.argv[1]})
baseAsSet=prefix_data['baseAs']
result=KNOWNPATH(sys.argv[1])
