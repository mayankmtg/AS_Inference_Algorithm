import pymongo
from pymongo import MongoClient
import sys
import progressbar as pb

widgets = ['Time:', pb.Percentage(), ' ',pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]

timer = pb.ProgressBar(widgets=widgets, maxval=8100000).start()

client= MongoClient('localhost', 27017)
db=client.bgpPaths
collection=db.bgpGraph

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python populate.py <file-name>")
	sys.exit(0)


# function to check the occurance of consecutive repeating ases due to as prepending
def pathCleaning(path_array):
	cleaned_array=[]
	top=-1
	n=len(path_array)
	for i in range(n-1,0,-1):
		if(top==-1):
			cleaned_array.append(path_array[i])
			top+=1
		
		elif(cleaned_array[top]!=path_array[i]):
			cleaned_array.append(path_array[i])
			top+=1

	return cleaned_array


with open(sys.argv[1]) as bgp_routeviews:

	time=0
	for bgp_advertisement in bgp_routeviews:
		path_array=bgp_advertisement.split()
		
		prefix_data=collection.find_one({'prefix':path_array[0]})

		
		# list of base ases
		baseAs=[]
		
		clean_path=pathCleaning(path_array)

		path_rev=""
		as_index=1
		n=len(path_array)
		for auto_system in clean_path:
			baseAs.append(auto_system)
			path_rev+=auto_system
			path_rev+="|"

		if prefix_data!=None:
			nPaths=len(prefix_data['paths'])
			prefix_data['paths']["path"+str(nPaths+1)]=path_rev
			collection.save(prefix_data)
		
		else:
			new_prefix_data={}

			# prefix contains the name of the IP prefix taken into consideration
			new_prefix_data['prefix']=path_array[0]
			
			# paths contains the list of all paths in dictionary format like:-   "path1":"1|2|"
			new_prefix_data['paths']={}
			ref_object=new_prefix_data['paths']
			ref_object['path1']=path_rev

			# base ases contain the unique ases that belong to each as path for a particular prefix
			new_prefix_data['baseAs']=baseAs

			
			collection.insert(new_prefix_data)
		
		# optimised base as addition.... applying indexing on the baseAs field mongo
		# TODO: Apply multikey indexing mongo for accessing faster from list
		for base in baseAs:
			baseData=collection.find_one({'prefix':path_array[0], 'baseAs':base})
			if(baseData==None):
				collection.update(
					{"prefix":path_array[0]},
					{"$push":{"baseAs":base}}
				)
		time+=1
		timer.update(time)
	timer.finish()
