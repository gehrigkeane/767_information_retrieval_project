#	Author:		Gehrig Keane
#	Purpose:	Testing posting list creation
#	Description:N/A

import os
import llist
import token_rename

# List and open every file in current dir
tk_files = [file for file in os.listdir(".") if file.endswith(".tk")]
words = {}

for x,y in enumerate(tk_files):
	line_count, word_count = 0, 0
	with open(y,'r') as f:
		for line in f:
			for word in line.split():
				# We are now parsing word by word
				# y = filename
				# x = filenumber - don't trust this number as it will change with new files in the dir
				# f is the file object
				# word = current word

				# Check if word is in the dict
				if word in words.keys():
					# Capture dict entry for existing word
					w = words[word]
					w[1] += 1	# increment total frequency

					# Operate on linked list object
					ll = w[2]
					# Search linked list for filename
					#	if found
					#		increment tf
					#		append new line count
					#		append new word count
					#	else
					#		new node
					ll.check(y, line_count, word_count)
					w[0] = ll.length
				# Create Dict entry for new word
				else:
					ll = llist.linked_list()
					ll.add(y, line_count, word_count)
					words[word] = [1,1,ll]

				word_count += 1
			line_count += 1

# with open('doc3.tk','r') as f:
#	 for line in f:
#		 for word in line.split():
#			words.append(word)

for x,y in words.items():
	print x,
	print "[" + str(y[0]) + ", " + str(y[1]),
	y[2].list_print()
	print "]"

#print(words)

#dict_post = {'be': [17, 17], 'a': [5, 4], 'truck': [20, 3]}

# for x,y in dict_post.items():
# 	print x,
# 	print (y) 

























# class Post:
# 	postCount = 0

# 	def __init__(self, term, df, tf):
# 		self.term = term
# 		self.df = df
# 		self.tf = tf
# 		self.ent
# 		postCount += 1
