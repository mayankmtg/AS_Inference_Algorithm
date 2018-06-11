import pymongo
from pymongo import MongoClient
import sys
import progressbar as pb


widgets = ['Time:', pb.Percentage(), ' ',pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]

timer = pb.ProgressBar(widgets=widgets, maxval=8100000).start()

client= MongoClient('mongodb://mayank:mayank@192.168.2.75/bgpPaths', 27017)
db=client.bgpPaths
collection=db.bgpFreq



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

if(len(sys.argv)<2):
	print("Error-Enter Command in format: python freq.py <file-name>")
	sys.exit(0)

with open(sys.argv[1]) as bgp_routeviews:
	time=0
	for bgp_advertisement in bgp_routeviews:
		advertisement_array=bgp_advertisement.split()
		
		clean_path=pathCleaning(advertisement_array)

		for auto_sys1, auto_sys2 in zip(clean_path[:-1], clean_path[1:]):
			as_data=collection.find_one({'as1':auto_sys1, 'as2':auto_sys2})
			if(as_data==None):
				new_as_data={
					'as1':auto_sys1,
					'as2':auto_sys2,
					'freq':0
				}
				collection.insert(new_as_data)
				as_data=collection.find_one({'as1':auto_sys1, 'as2':auto_sys2})
			as_data['freq']+=1
			collection.save(as_data)

		time+=1
		timer.update(time)
	timer.finish()

