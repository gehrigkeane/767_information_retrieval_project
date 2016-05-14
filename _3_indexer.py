#	Author:		Gehrig Keane
#	Purpose:	Construct (among other things) an Inverted Index based on token lists in '2.TOKEN/'

import csv
import llist
import os
import pickle
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)
sys.setrecursionlimit(10000)		#Allows pickling of really large files

def create_inverted_index(pathname, test):
	# List and open every file in current dir
	tk_files = [file for file in os.listdir(pathname+".") if file.endswith(".token")]
	inv_index = {}
	doc_index = {}

	# x = file number 0, 1, ..., n , y = file name
	for x,y in enumerate(tk_files):
		if test and y != '0033110.token':			# Isolates token pool for testing
			continue
		print(str(x) + ": Indexing: " + str(y))
		line_count, word_count = 0, 0				# Reset line and word counters
		with open(pathname+y,'rb') as f:			# Open file y for writing
			while True:								# Load each pickle file
				try:
					content = pickle.load(f)
				except EOFError:
					break
			
			#doc_index[y] = {}
			#current_term_dict = doc_index[y]

			for word in content:					# For each word in the list of tokens
				#if word in current_term_dict.keys():
				#	current_term_dict[word] += 1
				#else:
				#	current_term_dict[word] = 1

				# We are now parsing word by word
				# y = pathname
				# x = filenumber - don't trust this number as it will change with new files in the dir
				# f is the file object
				# word = current word
				# Check if word is in the ii dictionary
				if word in inv_index.keys():
					w = inv_index[word]				# Capture ii entry for existing word
					w[1] += 1						# increment total frequency
					if y in w[2].keys():				# File is in word's posting list
						ld = w[2][y]
						ld[0].append(word_count)
						ld[1] += 1
					else:							# Word is in II, but not posting for y
						w[2][y] = [[word_count],1]
					w[0] = len(w[2])				# Check Augments/Modifies the LL appropriately
				else:								# Create inverted index entry for new word
					ld = {y:[[word_count],1]}
					inv_index[word] = [1,1,ld]
				word_count += 1

	num_docs = len(tk_files)
	ninty_eight_percent = int(.98 * num_docs)

	# Extracts and sorts all of the terms from the Inverted Index
	terms = list(inv_index.keys())
	terms = sorted(terms)

	i_len = len(inv_index)						# i_len = Index Length - purely for benchmarking output
	i_post = 0									# i_post = Posting count - again for benchmarking
	for x in inv_index.values():
		i_post += len(x[2])

	for x in terms:								# Remove terms in the 98th percentile
		if inv_index[x][0] >= ninty_eight_percent:
			print("Removing: " + x + " - " + str( (inv_index.pop(x, None))[0:-1] ))

	f_len = len(inv_index)						# f_len = Index Length - purely for benchmarking output
	f_post = 0									# f_post = Posting count - again for benchmarking
	for x in inv_index.values():
		f_post += len(x[2])
	print("Pre-purge terms:\t" + str(i_len) + "\tPosting length: " + str(i_post))
	print("Post-purge terms:\t" + str(f_len) + "\tPosting length: " + str(f_post))

	pickle.dump(inv_index,open('3.ASSETS/ii_purged','wb'))
	return inv_index

def purge_index(pathname):
	with open("3.ASSETS/ii",'rb') as f:
		while True:
			try:
				inv_index = pickle.load(f)
			except EOFError:
				break

	# Count all the token files - for overall document count
	tk_files = [file for file in os.listdir(pathname+".") if file.endswith(".token")]
	num_docs = len(tk_files)
	ninty_eight_percent = int(.98 * num_docs)

	# Extracts and sorts all of the terms from the Inverted Index
	terms = list(inv_index.keys())
	terms = sorted(terms)

	i_len = len(inv_index)						# i_len = Index Length - purely for benchmarking output
	i_post = 0									# i_post = Posting count - again for benchmarking
	for x in inv_index.values():
		i_post += x[2].length

	for x in terms:								# Remove terms in the 98th percentile
		if inv_index[x][0] >= ninty_eight_percent:
			print("Removing: " + x + " - " + str( (inv_index.pop(x, None))[0:-1] ))

	f_len = len(inv_index)						# f_len = Index Length - purely for benchmarking output
	f_post = 0									# f_post = Posting count - again for benchmarking
	for x in inv_index.values():
		f_post += x[2].length
	print("Pre-purge terms:\t" + str(i_len) + "\tPosting length: " + str(i_post))
	print("Post-purge terms:\t" + str(f_len) + "\tPosting length: " + str(f_post))

	pickle.dump(inv_index,open('3.ASSETS/ii_purged','wb'))
	return inv_index

def print_index(inv_index):
	# x = key - the word
	# y = value - the array of [doc_freq, tot_freq, ll]
	for x,y in inv_index.items():
		print (x, end="")

		print ("[" + str(y[0]) + ", " + str(y[1]) + ", LL", end="")
		y[2].print_postings()
		print ("]")

#------------------------------------------------------------------------------------------
#	Create Initial Inverted Index pickle file - should be roughly 14326 terms strong
#------------------------------------------------------------------------------------------
# inv_index, doc_index = create_inverted_index('2.TOKEN/', True)
# pickle.dump(inv_index,open('3.ASSETS/ii','wb'))
# pickle.dump(doc_index,open('3.ASSETS/di','wb'))

#------------------------------------------------------------------------------------------
#	Purge Initial II of useless terms - notice the file size drops dramatically
#		We have to build dumb II first to know which terms are useless
#------------------------------------------------------------------------------------------
# inv_index = purge_index('2.TOKEN/')
# print (len(inv_index))

#------------------------------------------------------------------------------------------
#	Test pickle dump file integrity
#------------------------------------------------------------------------------------------
# with open("3.ASSETS/ii",'rb') as f:
# 	while True:
# 		try:
# 			index = pickle.load(f)
# 		except EOFError:
# 			break
# print (len(index))

#------------------------------------------------------------------------------------------
#	Print Inverted Index, and Document Index
#------------------------------------------------------------------------------------------
# print_index(inv_index)
# pp.pprint(doc_index)
