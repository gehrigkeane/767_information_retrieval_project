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
filenames = os.listdir("Plotsummary")
N = len(filenames)			# total number of files
#print("N: ", N)

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
	if value[0] == N:			
		continue
	total_idf.update({key:round(math.log(N/value[0],10),5)})
total_idf = sorted(total_idf.items(), key=lambda x: x[1])
#print("total_idf: ", total_idf)
o_path = "new_processed"
if not os.path.exists(o_path): 	
	os.makedirs(o_path) 
#pickle.dump(total_idf,open(str(o_path)+"/total_idf.pickle",'wb'))
with open(str(o_path)+"/total_idf.csv", 'a', newline='') as f_totalidf:
	writer = csv.writer(f_totalidf, delimiter=',')
	for i in range(0, len(total_idf)):
		wstring = total_idf[i][0]+":"+str(total_idf[i][1])
		writer.writerow([i,wstring])

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

doc_id = 0
dlist = []
exist_terms = [et[0] for et in total_idf]
#print("total_idf: ", total_idf)
#print("exist_terms:", exist_terms)
for key, value in document_index.items(): 
	dlist.append([i, key[0:-14]])
	with open(str(o_path)+"/document_list.csv",'a',newline='') as f_docindex:
		writer1 = csv.writer(f_docindex)
		writer1.writerow([doc_id, key[0:-14]])
	doc_id += 1
	D = []
	for term in value.keys():
		try:
			pos = exist_terms.index(term)
			tfidf = value[term]*total_idf[pos][1]
			ft= str(pos)+':'+str(tfidf)
			D.append(ft) 
		except ValueError:
			continue
	#print("D: ", D)
	D_vectors.append(D)
pickle.dump(dlist, open(str(o_path)+"/document_list.pickle",'wb'))

doc_count = 0
with open(str(o_path)+"/document_vectors.csv",'a',newline='') as f_docvec:
	writer2 = csv.writer(f_docvec)
	for pD in D_vectors:
		docv = ""
		for t in range(0, len(pD)-1):
			docv = docv+str(pD[t])+';'
		docv = docv+str(pD[-1])
		writer2.writerow([doc_count, docv])
		doc_count += 1
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

