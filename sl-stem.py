import pickle
import os
import pprint
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag

lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()

def get_wordnet_pos(treebank_tag):		#seperate to different kind of word
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

#-------------------open text processed by Young-------------------------#
#filenames = os.listdir("raw_Documents")		#get all the filenames of 63 documents under folder Documents
#f = open(str('filenames[i].pickle'),'rb')
#text = pickle.load(f)
#----------------------txt version-----------------------#
filenames = os.listdir("Parsed_Plotsummary")
	#get all the filenames of 63 documents under folder Documents
total_text = []
for filename in filenames:
	document = []
	if not ".txt" in filename:
		continue
	#print('Filename: %s'%filename)	
	f = open('Parsed_Plotsummary/%s'%filename,'rb')
	text = f.read().decode("utf-8")
	sents = sent_tokenize(text)
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
	o_path = "newtokenization"
	if not os.path.exists(o_path):
			os.makedirs(o_path)
	pickle.dump(document,open(o_path+'/%s-tokens.pickle'%filename[:-5],'wb'))