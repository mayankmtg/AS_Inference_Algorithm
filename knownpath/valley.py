import pymongo
from pymongo import MongoClient
import sys

client= MongoClient('mongodb://mayank:mayank@192.168.2.75/bgpPaths', 27017)
db=client.bgpPaths

Graph=db.bgpGraph
Rel=db.bgpRel



def build_ind_sin(seq,key):
	dic=dict()
	for (index,d) in enumerate(seq):
		if(dic.get(d[key])==None):
			dic[d[key]]=[]
		dic[d[key]].append(dict(d,index=index))
	return dic


def build_ind_comb(seq,key1,key2):
	return dict((d[key1]+"_"+d[key2], dict(d,index=index)) for (index,d) in enumerate(seq))

Rel_list=list(Rel.find())
Rel_as1_as2_ind=build_ind_comb(Rel_list, "as1","as2")

def relation(a,b):
	rel=Rel_as1_as2_ind.get(a + '_' + b)
	if(rel==None):
		return str('n')
	else:
		return str(rel['rel'])


def check_valley(path_array):
	temp_object = {
		'trip':'111',
		'rel':'nv'
	}
	for p,q,r in zip(path_array[:-2],path_array[1:-1], path_array[2:]):
		rel1=relation(p,q)
		rel2=relation(q,r)
		if(rel1=='p' and rel2=='c'):
			temp_object['trip']=p+'|'+q+'|'+r
			temp_object['rel']='pc'
			return temp_object
		elif(rel1=='p' and rel2=='s'):
			temp_object['trip']=p+'|'+q+'|'+r
                        temp_object['rel']='ps'
			return temp_object
		elif(rel1=='s' and rel2=='c'):
			temp_object['trip']=p+'|'+q+'|'+r
                        temp_object['rel']='sc'
			return temp_object
		elif(rel1=='s' and rel2=='s'):
			temp_object['trip']=p+'|'+q+'|'+r
                        temp_object['rel']='ss'
			return temp_object
	return temp_object


data=Graph.find()
count=0
for prefix_data in data:
	#print(prefix_data['prefix'])

	paths=prefix_data['paths']
	#print(paths)
	#print(len(paths))

	for pn,p in paths.iteritems():
		p=p.rstrip('|')
		path_array=p.split('|')
		if(len(path_array)>2):
			path_property=check_valley(path_array)	
			if(path_property['rel']!='nv'):
				print p,
				print path_property['trip'],
				print path_property['rel']
#	print(count)
#print(count)

