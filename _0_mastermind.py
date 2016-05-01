from subprocess import call		#call(['ls', '-a'])
import os
import sys
import pickle
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)

import _1_parser
import _2_tokenizer
import _3_indexer
import _4_tfidf
import _5_converter

TEST = False

#ntlk for python 3
#	sudo apt-get install python-setuptools 
#	sudo easy_install pip  
#	sudo pip install -U nltk 
#ntlk for python 3
#	sudo apt-get install python3-setuptools
#	sudo pip3 install nltk

# Populates '1.TXT/' directory with text files
#	Future Dependencies
#		- Required for Tokenization
_1_parser.parse_html("0.HTML/", TEST)

# Populates '2.TOKEN/' directory with pickle files
# 	Future Dependencies
#		- Required for Indexing
_2_tokenizer.tokenize_text('1.TXT/', TEST)

# Indexes '2.TOKEN/' files and returns/dumps result [purge requires manual dump]
# 	Future Dependencies
#		- Required for TF-IDF Calculations
#		- Required for Ruby Similarity Calculations
#		- Required for EVERYTHING
inv_index, doc_index = _3_indexer.create_inverted_index('2.TOKEN/', TEST)
pickle.dump(inv_index,open('3.ASSETS/ii','wb'))
pickle.dump(doc_index,open('3.ASSETS/di','wb'))

# Cleans up the Inverted Index [dumps new file for us]
# 	Future Dependencies
#		- Required for Managable filesize
inv_index = _3_indexer.purge_index('2.TOKEN/')

# Retrieves the IDF, Terms data structures - creates document vectors
# 	Future Dependencies
#		- Required for Vector magnitudes, yes it's very slow
#		  But it's something that's entirely necessary
idf,terms = _4_tfidf.get_idf(inv_index)
dv = _4_tfidf.get_dv(inv_index, idf, terms, True, TEST)

# Output everything we've made to CSV files
_5_converter.idf_to_csv(idf, terms)			# requires idf data structure
_5_converter.index_to_csv("2.TOKEN/")		# opens purged ii pickle file
_5_converter.token_lists_to_csv("2.TOKEN/")	# operates on straight token files
_5_converter.dv_to_csv()					# requires get_dv w/ dump=True ergo: get_dv(ii, idf, t, True, False)
