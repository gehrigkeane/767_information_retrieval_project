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
#i made title and snap csv files as arguments in case you wanted to test and change stuff
#titlecsv-title of the csv file you want to write to and same with snapcsv
#also, this function adds to a file
def createTitleAndSnaps(pathname, test, titlecsv, snapcsv):
	html_files = [file for file in os.listdir("Plotsummary/") if file.endswith(".htm") or file.endswith(".html")]
    	o_pathname = "3.ASSETS/"
    	# x = file number 0, 1, ..., n
    	# y = file name
	open("titleCSV/titleCollections.csv",'w').write("")
	open("snapShotCSV/snapShotCollection.csv",'w').write("")
	for x,y in enumerate(html_files):
		if test and y != '0033110.html':			# Isolates document pool for testing
				continue
		ofile = open(pathname+y)
	    	soup = bsoup(ofile)
		#-------------------------------------------------#
		#finds the film TITLE and write them to a csv file
		#-------------------------------------------------#
		b = soup.find(itemprop="name").find('a', href=True)
		title = '\'' + b.get_text() + '\''
		filename = y[:-5]+","
	 	with open(o_pathname+titlecsv, "a") as myfile:
	        	myfile.write(filename)
	        	#some titles have weird characters in them
	        	myfile.write(title.encode('utf8') + ',' + '\n')
	
	    	#-------------------------------------------------#
	    	#finds the film PLOTSUMMARY and write them to a csv file
	    	#-------------------------------------------------#
	    	desc = soup.find("p", class_="plotSummary")
	    	filename = y[:-5]+","
	    	with open(o_pathname+snapcsv, "a") as myfile:
	        	myfile.write(filename)
	    	if desc != None:
		        snap = '\'' + desc.get_text().replace('\n','') + '\''
		        with open(o_pathname+snapcsv, "a") as myfile:
		        	myfile.write(snap.encode('utf8')+',\n')
		else:
			with open(o_pathname+snapcsv, "a") as myfile:
				myfile.write('\'\','+'\n')

#------------------------------------------------------------------------------------------
#	Correct invokation of parse_html
#------------------------------------------------------------------------------------------
# parse_html("0.HTML/")
