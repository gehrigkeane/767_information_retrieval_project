import pickle
import pprint
import calendar

path = 'tokenization/Miami_Dolphins_seasons-tokens.pickle'
f = open(str(path),'rb')
while True:
	try:
		content = pickle.load(f)	
		pprint.pprint(content)
		"""
		for status in content:
			print(status.created_at, calendar.timegm(status.created_at.timetuple()))
		"""
	except EOFError:
		break
