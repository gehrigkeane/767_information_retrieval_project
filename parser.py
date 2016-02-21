import re
from HTMLParser import HTMLParser

f = open('Arches_National_Park.htm','r')
data = f.read()
#print data

#the big list that I pass on to the next guy
l = []

def parseStringBySpace(string):
    	string.split(" ")
    	return string

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        #print data
        data = data.replace(',','')
        data = data.replace(';','')
        data = data.replace(':','')
        data = data.lower()
        print data
        #l.append(parseStringBySpace(data))

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(data)


a = "AAAA"
print a
print a.lower()

#print l

#'<html><head><title>Test</title></head>'
 #           '<body><h1>Parse me!</h1></body></html>'