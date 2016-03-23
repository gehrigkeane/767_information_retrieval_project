#------------------------Author: Qiaozhi Wang-----------------------------------#
import pickle
from collections import Counter
import os
import math
#----------------------open all the documents--------------------#
#----------which can be changed to loop later---------------------#
filenames = os.listdir("tour")
	#get all the filenames of 63 documents under folder Documents
total_text = []
for filename in filenames:
	if not ".txt" in filename:
		continue
	print('Filename: %s'%filename)	
	f = open('tour/%s'%filename,'rb')
	total_text.append(f.read) #total_text; [text1,text2...]

class TFIDF():
	def __init__(self):
		self.word_lists = []
		self.total_tf = []
		self.count_tf = []
		self.count_df = []
		self.D_total = []	#store tf-idf for all documents
		self.similarity = []
	
	def tf(self, total_text):		
		#--------------calculate the term frequency----------------------#
		for text in total_text:
			self.count_tf = Counter(text)		#count_tf includes all document's tf, each of them is a list
			self.total_tf.append(self.count_tf)	#total_tf: [text1_tf,text2_tf,text3_tf...]
			self.word_lists.append(list(self.count_tf.keys()))
		return self.word_lists, self.total_tf

	def idf(self, word_lists):
		#----------------------calculate the document frequency-----------------#
		total_words = []
		n = len(word_lists)
		for word_list in word_lists:
			total_words.extend(word_list)
		self.count_df = Counter(total_words)
		for key, value in self.count_df.items():
			self.count_df[key] = math.log(n/float(self.count_df[key]),10)
		return self.count_df

	def tf_idf(self,total_tf,count_df):
		#----------------------calculate the tf-idf score-------------------------#
		D = []		#D for per document
		for per_tf in total_tf:
			for key, value in count_df.items():
				if key in list(per_tf.keys()):
					D.append(count_df[key]*per_tf[key])
				else:
					D.append('0')
			self.D_total.append(D)
			D = []
		return self.D_total
#--------------------calculate the similarity between two sentences or documents----------------------#
#----parameters: D1: document1_tf-idf and D2: document2_tf-idf, both of them from D_total----------------------#
def similarity(D1,D2):
	v_sum = 0
	s1_sum = 0
	s2_sum = 0
	for i in range(0,len(D1)):
		v_sum = float(D1[i])*float(D2[i])+v_sum
		s1_sum = float(D1[i])**2+s1_sum
		s2_sum = float(D2[i])**2+s2_sum
	sim = v_sum/(math.sqrt(s1_sum*s2_sum))
	return sim

#-----------similarity between two documents-------------------------------------#
test = TFIDF()
(t_wl,t_total_tf) = test.tf(total_text)
t_idf = test.idf(t_wl)
t_tfidf = test.tf_idf(t_total_tf,t_idf)
si = similarity(t_tfidf[2],t_tfidf[3])
print(si)
