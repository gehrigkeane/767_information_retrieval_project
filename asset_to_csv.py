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

# def print_postings(self):
# 	n = self.head # cant point to ll!
# 	while n:
# 		print ("[fn:" + str(n.file_name) + ", wn:" + str(n.word_num) + ", tf:" + str(n.term_f) + "] -> ", end="")
# 		n = n.next
# 	print ("None", end="")

def print_index(inv_index):
	# x = key - the word
	# y = value - the array of [doc_freq, tot_freq, ll]
	for x,y in inv_index.items():

		print (x, end="")

		print ("[" + str(y[0]) + ", " + str(y[1]) + ", LL", end="")
		#y[2].print_postings()
		print ("]")

with open("memory_assets/inverted_index.pickle",'rb') as f:
	while True:
		try:
			index = pickle.load(f)
		except EOFError:
			break

with open('memory_assets/ii.csv', 'w') as f:  # Just use 'w' mode in 3.x
	# Header Line
	# f.write("term,document frequency,term frequency,posting list\n")

	for x,y in index.items():
		f.write (str(x) + "," + str(y[0]) + "," + str(y[1]) + ",")
		n = y[2].head
		while n:
			temp = str(n.word_num)
			temp = temp.replace(', ', ':')
			f.write (str(n.file_name) + ";" + temp + ";" + str(n.term_f) + "`")
			n = n.next
		f.write ("\n")
		#y[2].print_postings()