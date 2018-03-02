import pymongo
from pymongo import MongoClient
import sys

client= MongoClient('localhost', 27017)
db=client.bgpNeighs
collection=db.bgpNeighs

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python relate.py <relationship-file-name>")
	sys.exit(0)

with open(sys.argv[1]) as bgp_relations:

	for relation in bgp_relations:
		relation_array=relation.split('|')
		
		as_data=collection.find_one({'as':relation_array[0]})

		if as_data==None:
			new_as_data={
				'as':relation_array[0],
				'neighbours':{
					'siblings':{},
					'customers':{},
					'providers':{},
				},
			}
		else:
			if(relation_array[2]==0):




		neighbour_dict={}
		sibling_dict={}
		customer_dict={}

		# sibling code
		if(int(relation_array[2])==0):
			auto_system=relation_array[1]
			sibling_dict[auto_system]=relation_array[2]
		elif(int(relation_array[2])==-1):


		if as_data!=None:
			nPaths=len(as_data['neighbours'])
			as_data['neighbours']["path"+str(nPaths+1)]=neighbour_dict
			collection.save(as_data)
		
		else:
			new_prefix_data={}
			new_prefix_data['prefix']=relation_array[0]
			new_prefix_data['neighbours']={}
			ref_object=new_prefix_data['neighbours']
			ref_object['path1']=neighbour_dict
			collection.insert(new_prefix_data)
