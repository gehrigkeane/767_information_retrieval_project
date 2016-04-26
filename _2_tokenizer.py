#	Author:		Qiaozhi Wang
#	Purpose:	Produce pure - stemmed - lemmatized token from rought txt input in '1.TXT/'

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
import os
import pickle
# nltk not working? Try the following
#	import nltk
#	nltk.download('all')

#------------------------------------------------------------------------------------------
#	<TODO: Find out what this thing does>
#------------------------------------------------------------------------------------------
def get_wordnet_pos(treebank_tag):						#seperate to different kind of word
	if treebank_tag.startswith('J'):
		return wordnet.ADJ
	if treebank_tag.startswith('V'):
		return wordnet.VERB
	if treebank_tag.startswith('N'):
		return wordnet.NOUN
	if treebank_tag.startswith('R'):
		return wordnet.ADV
	else:
		return ''

#------------------------------------------------------------------------------------------
#	Tokenize files in '1.TXT'
#------------------------------------------------------------------------------------------
def tokenize_text(pathname, test):
	filenames = [file for file in os.listdir(pathname+".") if file.endswith(".txt")]
	lemmatizer = WordNetLemmatizer()
	ps = PorterStemmer()
	o_pathname = "2.TOKEN/"

	for x,y in enumerate(filenames):
		if test and y != '0033110.txt':						# Isolates txt pool for testing
			continue
		document = []
		with  open(pathname+y,'rb') as f:
			filename = y[:-4]+".token"
			print(str(x) + ": Tokenizing: " + str(y) + " -> " + filename)

			sents = sent_tokenize(f.read().decode("utf-8"))
			for sent in sents:
				tokens = word_tokenize(sent)
				words = [w.lower() for w in tokens if w.isalpha() or w.isalnum()]

				#stop list
				stop_words = set(stopwords.words('english'))
				filtered_text = [w for w in words if not w in stop_words]
				tagged_tokens = pos_tag(filtered_text)

				#Lemmatize and Stemmer (I'm afraid lemmatizer improve recall, but decrease precision)
				for i in range(0,len(filtered_text)):
					if get_wordnet_pos(tagged_tokens[i][1]):
						w = lemmatizer.lemmatize(filtered_text[i], get_wordnet_pos(tagged_tokens[i][1]))
						w = ps.stem(w)
					else:
						w = ps.stem(filtered_text[i])
					document.append(w)

			if not os.path.exists(o_pathname):
					os.makedirs(o_pathname)
			#print (document)
			pickle.dump(document,open(o_pathname+filename,'wb'))

#------------------------------------------------------------------------------------------
#	Correct invokation of tokenize_text
#------------------------------------------------------------------------------------------
# tokenize_text('1.TXT/')
