#	Author:		Gehrig Keane
#	Purpose:	Calculate IDF figures
#	Description:N/A
# 	TODO: incorporate into pipelined structure
#	TODO: formulate strategy for zero elimination in dv's

import os
import sys
import pickle
import pprint
import csv
import math

import pprint
pp = pprint.PrettyPrinter(indent=4)

# --------------------------------------------------------------------------------
#	Load Inverted Index into memory
# --------------------------------------------------------------------------------
def get_index():
	with open("memory_assets/ii.pickle",'rb') as f:
		while True:
			try:
				index = pickle.load(f)
			except EOFError:
				break
	return index

def get_idf(index):
	tk_files = [file for file in os.listdir("newtokenization/.") if file.endswith(".pickle")]
	N = len(tk_files)		# Total Document count
	idf = {}
	
	# --------------------------------------------------------------------------------
	#	Calculate IDF figures
	# --------------------------------------------------------------------------------
	# x = key, y = value
	for x,y in index.items():
		idf[x] = math.log10(N/y[0])	# idf = log_10(N/df)

	# --------------------------------------------------------------------------------
	#	Produce list of sorted terms
	# --------------------------------------------------------------------------------
	terms = list(index.keys())
	terms = sorted(terms)

	# --------------------------------------------------------------------------------
	#	Create idf csv file
	# --------------------------------------------------------------------------------
	with open('memory_assets/idf.csv', 'w') as f:
		for x in terms:
			f.write (x + "," + str(idf[x]) + ",\n")

	return idf, terms

# --------------------------------------------------------------------------------
#	Retrieve Term Frequency from postings list
# --------------------------------------------------------------------------------
def get_tf(node, f):
	while node:
		if node.file_name == f:
			return node.term_f
		node = node.next
	return None

# --------------------------------------------------------------------------------
#	Create document vectors
# --------------------------------------------------------------------------------
def get_dv(index, idf, terms, dump):
	tk_files = [file for file in os.listdir("newtokenization/.") if file.endswith(".pickle")]
	dv = {}
	
	# x = index, y = filename
	for x,y in enumerate(tk_files):
		print(str(x) + ": Opening: " + str(y))
		#	Open all of the token lists
		with open("newtokenization/"+y,'rb') as f:
			while True:
				try:
					content = pickle.load(f)
				except EOFError:
					break
		
		# Iterate through every term in the dictionary
		# and insert the appropriate weight for each 
		# indicie of a document vector
		vec = [0] * len(index)	# init a list of size n , n = total number of terms
		for i,j in enumerate(terms):
			if j in content:	# term j is in document y
				tf = get_tf(index[j][2].head, y)
				if tf is not None:		#double check that term frequency returned
					vec[i] = tf * idf[j]
		dv[y] = vec

		# --------------------------------------------------------------------------------
		#	Dump document vector in pickle file
		# --------------------------------------------------------------------------------
		if dump:
			pickle.dump(vec,open('memory_assets/vectors/'+y,'wb'))
	return dv

# --------------------------------------------------------------------------------
#	Create document vector csv file
# --------------------------------------------------------------------------------
def dv_to_csv():
	with open('memory_assets/dv.csv', 'w') as f:
		vec_files = [file for file in os.listdir("memory_assets/vectors/.") if file.endswith(".pickle")]
		dv = {}

		# x = index, y = filename
		for x,y in enumerate(vec_files):
			#	Open all of the token lists
			with open("memory_assets/vectors/"+y,'rb') as ff:
				while True:
					try:
						vector = pickle.load(ff)
					except EOFError:
						break
			dv[y] = vector

		fnames = list(dv.keys())
		fnames = sorted(fnames)

		for x in fnames:
			f.write (x + "," + str(dv[x]).replace(', ', ':') + ",\n")

# --------------------------------------------------------------------------------
#	Pick and choose functions
# --------------------------------------------------------------------------------
index = get_index()
idf,terms = get_idf(index)

# Rebuild pickle files - this is very time consuming
#dv = get_dv(index, idf, terms, True)

# Rebuild CSV file
dv_to_csv()

