import pickle
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
#filename = os.listdir("Documents")		#get all the filenames of 63 documents under folder Documents
#f = open(str('filename[i].pickle'),'rb')
#text = pickle.load(f)

#----------------------example-----------------------------------#
text = "Better Machine learning is the science of getting computers to act without being explicitly programmed. In the past decade, machine learning has given us self-driving cars, practical speech recognition, effective web search, and a vastly improved understanding of the human genome. Machine learning is so pervasive today that you probably use it dozens of times a day without knowing it. Many researchers also think it is the best way to make progress towards human-level AI. In this class, you will learn about the most effective machine learning techniques, and gain practice implementing them and getting them to work for yourself. More importantly, you'll learn about not only the theoretical underpinnings of learning, but also gain the practical know-how needed to quickly and powerfully apply these techniques to new problems. Finally, you'll learn about some of Silicon Valley's best practices in innovation as it pertains to machine learning and AI."
tokens = word_tokenize(text)
words = [w.lower() for w in tokens if w.isalpha()]

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
	print(w)