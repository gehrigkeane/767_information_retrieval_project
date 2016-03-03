import pickle
from collections import Counter
import os
import math
#----------------------open all the documents--------------------#
#----------which can be changed to loop later---------------------#
filenames = os.listdir("/home/qiaozhi/Desktop/767-project/767_information_retrieval_project/Documents")		#get all the filenames of 63 documents under folder Documents
total_text = []
for filename in filenames:
	f = open('Documents/%s'%filename,'rb')
	total_text.append(pickle.load(f))

def tf(document):
	count_tf = Counter(document)
	return count_tf

def df(word_lists):
	total_words = []
	n = len(word_lists)
	for word_list in word_lists:
		total_words.extend(word_list)
	count_df = Counter(total_words)
	for key, value in count_df.items():
		count_df[key] = math.log(n/float(count_df[key]),10)
	return count_df

def tf_idf(total_tf,count_df):
	D = []		#D for per document
	D_total = []
	for per_tf in total_tf:
		for key, value in count_df.items():
			if key in list(per_tf.keys()):
				D.append(count_df[key]*per_tf[key])
			else:
				D.append('0')
			print(len(D))
		D_total.append(D)
		D = []
		print(len(D_total))
	return D_total

def similarity(D1,D2):
	v_sum = 0
	s1_sum = 0
	s2_sum = 0
	for i in range(0,len(D1)):
		v_sum = float(D1[i])*float(D2[i])+v_sum
		s1_sum = float(D1[i])**2+s1_sum
		s2_sum = float(D2[i])**2+s2_sum
	similarity = v_sum/(math.sqrt(s1_sum*s2_sum))
	return similarity


#-----------similarity between two documents
word_lists = []
total_tf = []
for text in total_text:
	count_tf = tf(text)		#count_tf includes all document's tf, each of them is a list
	total_tf.append(count_tf)
	word_lists.append(list(count_tf.keys()))

count_df = df(word_lists)
D_total = tf_idf(total_tf,count_df)
#print(D_total)
similarity = similarity(D_total[1],D_total[0])
print(similarity)
print(D_total[1])
print(D_total[0])