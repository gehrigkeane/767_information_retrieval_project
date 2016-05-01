#	Author:		Gehrig Keane
#	Purpose:	Calculate IDF figures based on inverted index

import csv
import math
import os
import pickle
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

#------------------------------------------------------------------------------------------
#	Load Inverted Index into memory
#------------------------------------------------------------------------------------------
def get_index():
	with open("3.ASSETS/ii_purged",'rb') as f:
		while True:
			try:
				index = pickle.load(f)
			except EOFError:
				break
	return index

#------------------------------------------------------------------------------------------
#	Create IDF dictionary
#------------------------------------------------------------------------------------------
def get_idf(index):
	tk_files = [file for file in os.listdir("2.TOKEN/.") if file.endswith(".token")]
	N = len(tk_files)		# Total Document count
	idf = {}
	
	#--------------------------------------------------------------------------------------
	#	Calculate IDF figures
	#--------------------------------------------------------------------------------------
	# x = key, y = value
	for x,y in index.items():
		idf[x] = math.log10(N/y[0])	# idf = log_10(N/df)

	#--------------------------------------------------------------------------------------
	#	Produce list of sorted terms
	#--------------------------------------------------------------------------------------
	terms = list(index.keys())
	terms = sorted(terms)

	return idf, terms

#------------------------------------------------------------------------------------------
#	Retrieve Term Frequency from postings list
#------------------------------------------------------------------------------------------
def get_tf(node, f):
	while node:
		if node.file_name == f:
			return node.term_f
		node = node.next
	return None

#------------------------------------------------------------------------------------------
#	Create document vectors
#------------------------------------------------------------------------------------------
def get_dv(index, idf, terms, dump, test):
	tk_files = [file for file in os.listdir("2.TOKEN/.") if file.endswith(".token")]
	dv = {}
	
	# x = index, y = filename
	for x,y in enumerate(tk_files):
		if test and y != '0033110.token':					# Isolates token pool for testing
			continue
		filename = y[:-5] + "vector"
		print(str(x) + ": Weighing: " + str(y) + " -> " + filename)
		with open("2.TOKEN/"+y,'rb') as f:			# Open all of the token lists
			while True:
				try:
					content = pickle.load(f)
				except EOFError:
					break
		
		vec = []									# vec will grow on non-zero terms
		for i,j in enumerate(terms):				# i = index, j = term
			if j in content:						# term j is in document y
				tf = get_tf(index[j][2].head, y)
				if tf is not None:					# double check that term frequency returned
					vec.append([tf * idf[j], i]) 	# Old dv generation: vec[i] = tf * idf[j]
		dv[y] = vec
		#----------------------------------------------------------------------------------
		#	Dump document vector in pickle file
		#----------------------------------------------------------------------------------
		if dump:
			if not os.path.exists('3.ASSETS/vectors/'):
				os.makedirs('3.ASSETS/vectors/')
			pickle.dump(vec,open('3.ASSETS/vectors/'+filename,'wb'))
	return dv

#------------------------------------------------------------------------------------------
#	Get Index, IDF, and sorted Terms, then build document vectors - VERY TIME CONSUMING
#------------------------------------------------------------------------------------------
# index = get_index()
# idf,terms = get_idf(index)
# dv = get_dv(index, idf, terms, True)
