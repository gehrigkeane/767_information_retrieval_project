#'	Author:		Gehrig Keane
#	Purpose:	Converting Inverted Index et all to csv files

import csv
import os
import pickle
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

#------------------------------------------------------------------------------------------
#	Create idf csv file
#------------------------------------------------------------------------------------------
def idf_to_csv(idf, terms):
	print("CSV: IDF")
	with open('3.ASSETS/idf.csv', 'w') as f:
		for x in terms:
			f.write (x + "," + str(idf[x]) + ",\n")

#------------------------------------------------------------------------------------------
#	Create inverted index csv file
#------------------------------------------------------------------------------------------
def index_to_csv(pathname):
	print("CSV: Inverted Index")
	tk_files = [file for file in os.listdir(pathname+".") if file.endswith(".token")]

	total_doc = len(tk_files)

	with open("3.ASSETS/ii_purged",'rb') as f:
		while True:
			try:
				index = pickle.load(f)
			except EOFError:
				break

	ii = list(index.keys())
	ii = sorted(ii)
	#pp.pprint(ii)

	with open('3.ASSETS/ii.csv', 'w') as f:  # Just use 'w' mode in 3.x
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

#------------------------------------------------------------------------------------------
#	Create document vector csv file
#------------------------------------------------------------------------------------------
def dv_to_csv():
	print("CSV: Document Vectors")
	with open('3.ASSETS/dv.csv', 'w') as f:
		vec_files = [file for file in os.listdir("3.ASSETS/vectors/.") if file.endswith("vector")]
		dv = {}

		# x = index, y = filename
		for x,y in enumerate(vec_files):
			#	Open all of the token lists
			with open("3.ASSETS/vectors/"+y,'rb') as ff:
				while True:
					try:
						vector = pickle.load(ff)
					except EOFError:
						break
			dv[y] = vector

		fnames = list(dv.keys())
		fnames = sorted(fnames)

		for x,y in enumerate(fnames):
			print (str(x) + " " + str(y))
			vec = ""
			for i in dv[y]:
				vec += str(i).replace(', ',':').replace('[','').replace(']','') + ";"
			#print (vec[:-1])
			#print(y + "," + str(dv[y]).replace(', ', ':') + ",\n")
			f.write (y + "," + vec[:-1] + ",\n")

#------------------------------------------------------------------------------------------
#	Create token list csv file
#------------------------------------------------------------------------------------------
def token_lists_to_csv(pathname):
	print("CSV: Token Lists")
	tk_files = [file for file in os.listdir(pathname+".") if file.endswith(".token")]

	for x,y in enumerate(tk_files):
		print(str(x) + ": Opening: " + str(y))
		with open(pathname+y,'rb') as f:
			while True:
				try:
					content = pickle.load(f)
				except EOFError:
					break
		#print(content)

		with open('3.ASSETS/token_strings.csv', 'a') as f:
			f.write (y + "," + str(content).replace(', ', ':') + ",\n")

#------------------------------------------------------------------------------------------
#	Correct invokation of the methods
#------------------------------------------------------------------------------------------
# index_to_csv("2.TOKEN/")
# token_lists_to_csv("2.TOKEN/")
# ...
