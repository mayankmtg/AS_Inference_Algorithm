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
Graph=db.bgpGraph
Neighs=db.bgpNeighs


def peers(u):
	# return array of tupples of neighbour and type of neighbour
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


def relation(a,b):
	# find the relationship of a to b

	peers_a=peers(a)
	for i in peers_a:
		if(i[0]==b):
			return i[1]

	# return 'p' if a is provider of b and 'c', 's' otherwise


def valleyFree(path, extended_AS):
	# method returns 1 if the extended path is valley free
	prev_path=path.split('|')

	# path of the form '1|2|3|4|' therefore 1 is subtracted
	n=len(prev_path)-1
	# main concentration on relationship of n-2 and n-1 elements of the array only

	last_relation=relation(prev_path[n-2], prev_path[n-1])
	new_relation=relation(prev_path[n-1], extended_AS)

	# last_relation=='p'   => provider to customer

	if(last_relation=='p' and new_relation=='c'):
		return 0
	elif(last_relation=='s' and new_relation=='c'):
		return 0
	else:
		return 1


def INITACTIVEQUEUE(prefix, queue, graph, baseASset):

	for v in baseASset:
		queue.put(v)
		rib_in(v)[p][0] = sure path of v
		SORT(rib in(v)[p])


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
