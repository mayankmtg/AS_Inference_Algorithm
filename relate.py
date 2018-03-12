import pymongo
from pymongo import MongoClient
import sys
import progressbar as pb


widgets = ['Time:', pb.Percentage(), ' ',pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]

timer = pb.ProgressBar(widgets=widgets, maxval=8100000).start()

client= MongoClient('localhost', 27017)
db=client.bgpPaths
collection=db.bgpNeighs

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python relate.py <relationship-file-name>")
	sys.exit(0)

with open(sys.argv[1]) as bgp_relations:
	time=0
	for relation in bgp_relations:
		relation_array=relation.split('|')
		
		as_data=collection.find_one({'as':relation_array[0]})
		neighbour_data=collection.find_one({'as':relation_array[1]})
		if as_data==None:
			new_as_data={
				'as':relation_array[0],
				'neighbours':{
					'siblings':[],
					'customers':[],
					'providers':[],
				},
			}
			collection.insert(new_as_data)
			as_data=collection.find_one({'as':relation_array[0]})
		if neighbour_data==None:
			new_neighbour_data={
				'as':relation_array[1],
				'neighbours':{
					'siblings':[],
					'customers':[],
					'providers':[],
				},
			}
			collection.insert(new_neighbour_data)
			neighbour_data=collection.find_one({'as':relation_array[1]})

		if(int(relation_array[2])==0):
			# if relation_array[1] not in as_data['neighbours']['siblings']:
			as_data['neighbours']['siblings'].append(relation_array[1])
			# if relation_array[0] not in neighbour_data['neighbours']['siblings']:
			neighbour_data['neighbours']['siblings'].append(relation_array[0])
		
		# 2|3|-1|bpg 2 is the provider and 3 is the customer
		elif(int(relation_array[2])==-1):
			# if(relation_array[1] not in as_data['neighbours']['customers']):
			as_data['neighbours']['customers'].append(relation_array[1])
			# if(relation_array[0] not in neighbour_data['neighbours']['providers']):
			neighbour_data['neighbours']['providers'].append(relation_array[0])
		collection.save(as_data)
		collection.save(neighbour_data)
		time+=1
		timer.update(time)
	timer.finish()

