import pymongo
from pymongo import MongoClient
import sys

def peers(Neighs, u):
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


# return 'p' if a is provider of b and 'c', 's' otherwise else returns 'n' if no relation
def relation(Neighs,a,b):
	# find the relationship of a to b

	peers_a=peers(Neighs,a)
	for i in peers_a:
		if(i[0]==b):
			return i[1]

	return 'n'





# method returns 1 if the extended path is valley free
def valleyFree(Neighs,path, extended_AS):
	prev_path=path.split('|')

	# path of the form '1|2|3|4|' therefore 1 is subtracted
	n=len(prev_path)-1
	# main concentration on relationship of n-2 and n-1 elements of the array only

	last_relation=relation(Neighs,prev_path[n-2], prev_path[n-1])
	new_relation=relation(Neighs,prev_path[n-1], extended_AS)

	# last_relation=='p'   => provider to customer

	if(last_relation=='p' and new_relation=='c'):
		return 0
	elif(last_relation=='p' and new_relation=='s'):
		return 0
	elif(last_relation=='s' and new_relation=='c'):
		return 0
	elif(last_relation=='s' and new_relation=='s'):
		return 0
	else:
		return 1





# the autonomous systems passed is the v in rib_in(v)[p] and the path list is the list of paths corresponding to the prefix p
def surePath(auto_system, path_list):
	returnPaths=[]
	for path in path_list:
		path_array=path.split('|')
		path_current=""
		for AS in path_array:
			path_current+=AS+"|"
			if(AS==auto_system):
				returnPaths.append(path_current)
				break
	# returns unique elements from the array of the sure paths from v to p
	return list(set(returnPaths))


# the autonomous system and prefix passed are v and p respectively in rib_in(v)[p], new_path is new entry 
def ribin_insert(Ribin, prefix, auto_system, new_path):
	# apply the following indexes
		# db.bgpRibin.ensureIndex({'prefix':1})
		# db.bgpRibin.ensureIndex({'as':1})
	rib_in = Ribin.find_one({'prefix':prefix, 'as':auto_system})
	if(rib_in==None):
		new_ribin={
			'prefix':prefix,
			'as':auto_system,
			'paths':[]
		}
		Ribin.insert(new_ribin)

	Ribin.update(
		{'prefix':prefix, 'as':auto_system},
		{'$addToSet':{'paths':new_path}}
	)
	return 1



# the Freq is the bgpFreq collection and path is any path separated with '|'
def pathFreq(Freq, path_array):
	consec_freq=[]
	for x,y in zip(path_array[:-1], path_array[1:]):
		freq=Freq.find_one({'as1':x, 'as2':y})
		consec_freq.append(freq['freq'])
	return min(freq)




# path list contains path in the form of a|b|c||d|e where || stands for unsure path after

def bestPath(Freq, path_list):
	path_dict_array=[]
	for path in path_list:

		unsure_sec=path.split('||')
		
		ulen=len(unsure_sec[1])

		path_array=unsure_sec[0].split('|')+unsure_sec[1].split('|')
		path_len=len(path_array)
		freq=pathFreq(Freq, path_array)
		path_dict={
			'path':path,
			'len':path_len,
			'freq':freq,
			'ulen':ulen
		}
		path_dict_array.append(path_dict)
	# sorting based on len first, freq second and then ulen
	return sorted(path_dict_array, key= lambda i:(i['len'],i['freq'], i['ulen']))

	