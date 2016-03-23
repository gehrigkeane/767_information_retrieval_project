import pickle
import pprint
import calendar

path = 'memory_assets/inverted_index.pickle'
f = open(str(path),'rb')
while True:
	try:
		content = pickle.load(f)	
		pprint.pprint(content)
	except EOFError:
		break
		

