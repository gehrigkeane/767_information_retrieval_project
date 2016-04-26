#	Author:		Young Liu
#	Purpose:	Parse and Strip HTML/Javascript from HTML document collection '0.HTML/'

from html.parser import HTMLParser
import os
import pickle
import re

#------------------------------------------------------------------------------------------
#	Create a subclass and override the handler methods
#------------------------------------------------------------------------------------------
class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.data = ""

	def handle_data(self, d):
		d = d.replace('\n',' ')
		d = d.replace('  ', ' ')
		d = d.replace('\t',' ')
		d = d.lower()
		if "document." in d or "\",\"" in d or "\"})" in d or re.match('var', d) or re.match('if \(', d):
			d = ""
		if d != "" and d[0] == " ":
			d = d[1:]
		if re.match('\w', d):
			d = d + " "
			self.data += d

def parse_html(pathname, test):
	html_files = [file for file in os.listdir(pathname+".") if file.endswith(".htm") or file.endswith(".html")]
	o_pathname = "1.TXT/"							# Output path name
	for x,y in enumerate(html_files):				# x = file number 0, 1, ..., n , y = file name
		if test and y != '0033110.html':			# Isolates document pool for testing
				continue
		with open(pathname+y, 'r') as f:
			filename = y[:-5]+".txt"
			print(str(x) + ": Parsing: " + str(y) + " -> " + filename)
			parser = MyHTMLParser()
			parser.feed(f.read())					#f.read() = data for parser
			#print (parser.data)
			#pickle.dump(parser.data.split(),open(pathname + y[:-4] + "pickle",'wb'))
			if not os.path.exists(o_pathname):
				os.makedirs(o_pathname)
			open(o_pathname + filename,'w').write(parser.data)

#------------------------------------------------------------------------------------------
#	Correct invokation of parse_html
#------------------------------------------------------------------------------------------
# parse_html("0.HTML/")
