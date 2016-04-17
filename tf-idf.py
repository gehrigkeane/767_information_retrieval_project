#------------------------Author: Qiaozhi Wang-----------------------------------#
import pickle
from collections import Counter
import os, csv, sys
import math
import llist
import pprint as pp

sys.setrecursionlimit(5000)

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
#print("inverted_index: ")
#print(inverted_index)
for key, value in inverted_index.items():
	total_idf.update({key:math.log(N/value[0],10)})
#print("total_idf: ")
#print(total_idf)

o_path = "new_processed"
if not os.path.exists(o_path): 	
	os.makedirs(o_path) 
#pickle.dump(total_idf,open(str(o_path)+"/total_idf.pickle",'wb'))
with open(str(o_path)+"/total_idf.csv", 'a', newline='', encoding='utf8') as f_totalidf:
	writer = csv.writer(f_totalidf)
	for key, value in total_idf.items():
		writer.writerow([key, value])

#--------------read the tf of each document ----------------------#
path = 'memory_assets/document_index.pickle'
f = open(str(path),'rb')
while True:
	try:
		document_index = pickle.load(f)	
	except EOFError:
		break
#print("document_index:")
#print(document_index)
i = 0
for key, value in document_index.items(): 
	#document_list.update({i:key})
	#pickle.dump(document_list,open(str(o_path)+"/document_list.pickle",'wb')) 
	with open(str(o_path)+"/document_list.csv",'a',newline='',encoding='utf8') as f_docindex:
		writer1 = csv.writer(f_docindex)
		writer1.writerow([i, key])
	i += 1
	D = []
	for term in total_idf:
		if term in value.keys():
			D.append(value[term]*total_idf[term])
		else:
			D.append('0')
	#print("D: ", D)
	D_vectors.append(D)

with open(str(o_path)+"/document_vectors.csv",'a',newline='',encoding='utf8') as f_docvec:
	writer2 = csv.writer(f_docvec)
	for pD in D_vectors:
		writer2.writerow(pD)
	#pickle.dump(D_vectors,open(str(o_path)+"/document_vectors.pickle",'wb'))
#pp.pprint("D_vectors")
#pp.pprint(D_vectors)
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

