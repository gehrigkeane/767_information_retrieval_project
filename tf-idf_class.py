#------------------------Author: Qiaozhi Wang-----------------------------------#
import pickle
from collections import Counter
import os
import math
import llist

total_idf = {}
document_list = {}
D_vectors = []

#----------------------open inverted index--------------------#
filenames = os.listdir("tokenization")
N = len(filenames)			# total number of files

path = 'memory_assets/inverted_index.pickle'
f = open(str(path),'rb')
while True:
	try:
		inverted_index = pickle.load(f)	
	except EOFError:
		break

for key, value in inverted_index.items():
	total_idf.update({key:math.log(N/value[0],10)})

o_path = "processed"
if not os.path.exists(o_path): 	
	os.makedirs(o_path) 
pickle.dump(total_idf,open(str(o_path)+"/total_idf.pickle",'wb'))

#--------------read the tf of each document ----------------------#
path = 'memory_assets/document_index.pickle'
f = open(str(path),'rb')
while True:
	try:
		document_index = pickle.load(f)	
	except EOFError:
		break
i = 0
for key, value in document_index.items():
	document_list.update({i:key})
	i += 1
	pickle.dump(document_list,open(str(o_path)+"/document_list.pickle",'wb'))
	D = []
	for term, tf in value.items():
		if term in total_idf:
			D.append(value[term]*total_idf[term])
		else:
			D.append('0')
	D_vectors.append(D)
	pickle.dump(D_vectors,open(str(o_path)+"/document_vectors.pickle",'wb'))

def similarity(D1,D2):
	v_sum = 0
	s1_sum = 0
	s2_sum = 0
	for i in range(0,len(D1)):
		v_sum = float(D1[i])*float(D2[i])+v_sum
		s1_sum = float(D1[i])**2+s1_sum
		s2_sum = float(D2[i])**2+s2_sum
	sim = v_sum/(math.sqrt(s1_sum*s2_sum))
	return sim
