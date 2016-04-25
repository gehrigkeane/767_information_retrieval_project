#	Author:		Gehrig Keane
#	Purpose:	Testing posting list creation
#	Description:N/A

import os
import sys
import pickle
import pprint
import llist
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)

filename = "newtokenization/"
sys.setrecursionlimit(5000)

def create_inverted_index():
	# List and open every file in current dir
	tk_files = [file for file in os.listdir(filename+".") if file.endswith(".pickle")]
	num_docs = len(tk_files)
	ninty_eight_percent = int(.98 * num_docs)
	inv_index = {}
	doc_index = {}

	# x = file number 0, 1, ..., n
	# y = file name
	for x,y in enumerate(tk_files):
		#print(str(x) + ": Opening: " + str(y))
		# Reset line and word counters
		line_count, word_count = 0, 0
		# Open file y for writing
		with open(filename+y,'rb') as f:

			# Load each pickle file
			while True:
				try:
					content = pickle.load(f)
				except EOFError:
					break
			
			doc_index[y] = {}
			current_term_dict = doc_index[y]

			# For each word in the list of tokens
			for word in content:

				if word in current_term_dict.keys():
					current_term_dict[word] += 1
				else:
					current_term_dict[word] = 1

				# We are now parsing word by word
				# y = filename
				# x = filenumber - don't trust this number as it will change with new files in the dir
				# f is the file object
				# word = current word
				# Check if word is in the dictionary
				if word in inv_index.keys():
					# Capture dict entry for existing word
					w = inv_index[word]
					w[1] += 1	# increment total frequency
					# Check Augments/Modifies the linked list appropriately
					ll = w[2]
					ll.check(y, word_count)
					w[0] = ll.length

				# Create Dict entry for new word
				else:
					ll = llist.posting_list()
					ll.add(y, word_count)
					inv_index[word] = [1,1,ll]
				word_count += 1
	return inv_index, doc_index

def purge_index():
	with open("memory_assets/ii.pickle",'rb') as f:
		while True:
			try:
				inv_index = pickle.load(f)
			except EOFError:
				break

	tk_files = [file for file in os.listdir(filename+".") if file.endswith(".pickle")]
	num_docs = len(tk_files)
	init_size,fin_size = sys.getsizeof(inv_index),0
	ninty_eight_percent = int(.98 * num_docs)

	terms = list(inv_index.keys())
	terms = sorted(terms)

	for x in terms:
		if inv_index[x][0] >= ninty_eight_percent:
			pp.pprint(x + ": " + str( (inv_index.pop(x, None))[0:-1] ))

	pickle.dump(inv_index,open('memory_assets/ii_new.pickle','wb'))
	with open("memory_assets/ii_new.pickle",'rb') as f:
		while True:
			try:
				inv_index = pickle.load(f)
			except EOFError:
				break
	fin_size = sys.getsizeof(inv_index)
	print("Init: " + str(init_size) + "\tFin: " + str(fin_size))

def print_index(inv_index):
	# x = key - the word
	# y = value - the array of [doc_freq, tot_freq, ll]
	for x,y in inv_index.items():
		print (x, end="")

		print ("[" + str(y[0]) + ", " + str(y[1]) + ", LL", end="")
		y[2].print_postings()
		print ("]")

purge_index()
#inv_index, doc_index = create_inverted_index()


#pickle.dump(inv_index,open('memory_assets/ii.pickle','wb'))
#pickle.dump(doc_index,open('memory_assets/document_index.pickle','wb'))

# with open("memory_assets/inverted_index.pickle",'rb') as f:
# 	while True:
# 		try:
# 			index = pickle.load(f)
# 		except EOFError:
# 			break

# #print_index(index)
# for x,y in doc_index.items():
# 	print ("{ " + str(x) + " { ", end="")
# 	for i,j in y.items():
# 		print ( str(i) + ":" + str(j) + ", ", end="")
# 	print ( " } } " )
