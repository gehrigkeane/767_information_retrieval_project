#'	Author:		Gehrig Keane
#	Purpose:	Converting Inverted Index and such to csv files
#	Description:N/A

import os
import sys
import pickle
import pprint
import csv

import pprint
pp = pprint.PrettyPrinter(indent=4)

def index_to_csv(filename):
	tk_files = [file for file in os.listdir(filename+".") if file.endswith(".pickle")]

	total_doc = len(tk_files)

	with open("memory_assets/ii_purged.pickle",'rb') as f:
		while True:
			try:
				index = pickle.load(f)
			except EOFError:
				break

	ii = list(index.keys())
	ii = sorted(ii)
	#pp.pprint(ii)

	with open('memory_assets/ii_purged.csv', 'w') as f:  # Just use 'w' mode in 3.x
		# Header Line
		# f.write("term,document frequency,term frequency,posting list\n")

		# x = term, y = value
		for x in ii:
			if index[x][0] >= 934:
				pp.pprint(str(x) + "," + str(index[x][0]) + "," + str(index[x][1]))
			f.write (str(x) + "," + str(index[x][0]) + "," + str(index[x][1]) + ",")
			n = index[x][2].head
			while n:
				temp = str(n.word_num)
				temp = temp.replace(', ', ':')
				f.write (str(n.file_name) + ";" + temp + ";" + str(n.term_f) + "`")
				n = n.next
			f.write ("\n")
			#y[2].print_postings()

def token_lists_to_csv(filename):
	tk_files = [file for file in os.listdir(filename+".") if file.endswith(".pickle")]

	for x,y in enumerate(tk_files):
		print(str(x) + ": Opening: " + str(y))
		with open(filename+y,'rb') as f:
			while True:
				try:
					content = pickle.load(f)
				except EOFError:
					break
		#print(content)

		with open('memory_assets/token_strings.csv', 'a') as f:
			f.write (y + "," + str(content).replace(', ', ':') + ",\n")

index_to_csv("newtokenization/")
#token_lists_to_csv("newtokenization/")