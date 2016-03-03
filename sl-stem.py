import pickle
import os
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

#----------------------example-----------------------------------#
text = "Yellowstone National Park (Arapaho: Henihco'oo or Héetíhco'oo)[4] is a national park located primarily in the U.S. state of Wyoming, although it also extends into Montana and Idaho. It was established by the U.S. Congress and signed into law by President Ulysses S. Grant on March 1, 1872.[5][6] Yellowstone, the first National Park in the U.S. and widely held to be the first national park in the world,[7] is known for its wildlife and its many geothermal features, especially Old Faithful Geyser, one of the most popular features in the park.[8] It has many types of ecosystems, but the subalpine forest is the most abundant. It is part of the South Central Rockies forests ecoregion."
tokens = word_tokenize(text)
words = [w.lower() for w in tokens if w.isalpha()]

#stop list
stop_words = set(stopwords.words('english'))
filtered_text = [w for w in words if not w in stop_words]
tagged_tokens = pos_tag(filtered_text)

#Lemmatize and Stemmer (I'm afraid lemmatizer improve recall, but decrease precision)
document = []
for i in range(0,len(filtered_text)):
	if get_wordnet_pos(tagged_tokens[i][1]):
		w = lemmatizer.lemmatize(filtered_text[i], get_wordnet_pos(tagged_tokens[i][1]))
		w = ps.stem(w)
	else:
		w = ps.stem(filtered_text[i])
	document.append(w)
	print(w)
	pickle.dump(document,open('document4.pickle','wb'))

