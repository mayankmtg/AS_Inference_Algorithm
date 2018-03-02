import pymongo
from pymongo import MongoClient
import sys
from Queue import PriorityQueue
import heapq
from .utils import *





# def INITACTIVEQUEUE(p, queue, G, baseASset):
# 	for v in baseASset:
# 		APPEND(queue, ∪v)
# 		path(v)[p] ← sure path of v
# 		SORT(rib in(v)[p])


# def KNOWNPATH(p, G = (V,E), baseASset):
# 	queue = Queue()
# 	INITACTIVEQUEUE(p, queue, G, baseASset)
# 	while queue.length > 0:
# 		u ← POP(queue, 0)
# 		for v ∈ peers(u)
# 			Pu ← rib in(u)[p][0]
# 			if v /∈ baseASset and (v) + Pu = ψ:
# 				tmppath ← rib in(v)[p][0]
# 				rib in(v)[p] ← rib in(v)[p]  {(v) + Pu}
# 				SORT(rib in(v)[p])
# 				if tmppath = path(v)[p][0] and v /∈ queue:
# 					APPEND(queue, v)
# 	return {rib in(v)|∀v ∈ V }

