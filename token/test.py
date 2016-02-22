#	Author:		Gehrig Keane
#	Purpose:	Testing posting list creation
#	Description:N/A

import os

# List and open every file in current dir
tk_files = [file for file in os.listdir(".") if file.endswith(".tk")]
words = []

for x,y in enumerate(tk_files):
	with open(y,'r') as f:
		for line in f:
			for word in line.split():
				words.append(word)

# with open('doc3.tk','r') as f:
#	 for line in f:
#		 for word in line.split():
#			words.append(word)

print(words)



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