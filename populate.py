import pymongo
from pymongo import MongoClient
import sys

client= MongoClient('localhost', 27017)
db=client.bgpPaths
collection=db.bgpPaths

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python populate.py <file-name>")
	sys.exit(0)

with open(sys.argv[1]) as bgp_routeviews:

	for bgp_advertisement in bgp_routeviews:
		path_array=bgp_advertisement.split()
		
		prefix_data=collection.find_one({'prefix':path_array[0]})

		path_dict={}
		as_index=1
		
		n=len(path_array)
		
		for i in range(n-1,0,-1):
			auto_system=path_array[i]
			path_dict["AS"+str(as_index)]=auto_system
			as_index+=1

		if prefix_data!=None:
			nPaths=len(prefix_data['paths'])
			prefix_data['paths']["path"+str(nPaths+1)]=path_dict
			collection.save(prefix_data)
		
		else:
			new_prefix_data={}
			new_prefix_data['prefix']=path_array[0]
			new_prefix_data['paths']={}
			ref_object=new_prefix_data['paths']
			ref_object['path1']=path_dict
			collection.insert(new_prefix_data)
