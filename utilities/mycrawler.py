from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import threading, time, pprint, re, os
try: 
	import Queue
except:
	import queue as Queue

class LinkParser(HTMLParser):
	def __init__(self):
		super().__init__()

	def handle_starttag(self, tag, attrs):	#how it call this func
		if tag == 'a':
			for (key, value) in attrs:
				if key == "href":
					newUrl = parse.urljoin(self.baseUrl, value)
					self.links = self.links + [newUrl]

	def getLinks(self, seed_url):
		global q
		global visited
		global recorded
		plan = []
		self.links = []
		self.baseUrl = seed_url
		response = urlopen(seed_url)
		try:
			if response.getheader("Content-Type")=="text/html;charset=UTF-8":
				htmlString = response.read().decode("utf-8")
				self.feed(htmlString)
				for link in self.links:
					m = re.match(r"(http://www.imdb.com/title/tt)(\d+)",link)
					if not m:
						continue
					if m.group(2) in recorded or link in visited or link in plan:
						continue
					q.put(link)
					plan.append(link)						
				#[q.put(link) for link in self.links if not link in visited and re.match(r"(http://www.imdb.com/title/tt\d+\w+)",link)]
				#pprint.pprint(self.links)
				return htmlString
			else:
				return "", []
		except Exception as e:
			print(e)

def spider(url):
	global q
	global visited
	global recorded
	pagesToVisit = url
	while pagesToVisit != "":
		if pagesToVisit in visited:
			pagesToVisit = q.get()
			continue
		url = pagesToVisit
		visited.append(url)
		try:
			rec = re.match(r"(http://www.imdb.com/title/tt)(\d+)",url)
			if rec.group(2) in recorded:
				print("visited: ", url)
				pagesToVisit = q.get()
				continue
			print ("Visiting: ", url)
			parser = LinkParser()
			data = parser.getLinks(url)
			if re.match(r"(http://www.imdb.com/title/tt)(\d+)(/plotsummary)",url):
				m = re.match(r"(http://www.imdb.com/title/tt)(\d+)(/plotsummary)",url)
				filmid = m.group(2)
				if not filmid in recorded:
					recorded.append(filmid)
					print("recorded: ",recorded)
					o_path = "Plotsummary"
					if not os.path.exists(o_path):
						os.makedirs(o_path)
					f = open(o_path+"/%s.txt"%filmid,"w")
					f.write(data)
					f.close()
					print(filmid, "**Write down**")
			pagesToVisit = q.get()
			#print("**Success! But not recorded!**")
		except Exception as e:
			#print (e)
			#print ("Failed downloading and saving: ", url)
			pagesToVisit = q.get()
			continue
			
if __name__ == "__main__":
	q = Queue.Queue()
	global visited
	global recorded
	recorded = []
	visited = []
	seed_url = "http://www.imdb.com/chart/top?ref_=nv_mv_250_6"
	visited.append(seed_url)
	ob = LinkParser()
	ob_data = ob.getLinks(seed_url)
	threadnum = 10
	threads = []
	for i in range(0, threadnum):
		t = threading.Thread(target=spider, args = (q.get(), ))
		threads.append(t)
	[t.start() for t in threads]
	print('\nThread Count: '+
		str(threading.activeCount()))
	print(threading.enumerate())