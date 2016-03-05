import re
from HTMLParser import HTMLParser


f = open('Arches_National_Park.htm','r')
data = f.read()
#print data

n = open("a.txt",'w')

def letters(input):
    return ''.join([c for c in input if str.isalpha or c in str.isspace])
    #return ''.join(filter(str.isalpha, input))
    #return ''.join([c for c in input if c in str.isalpha or c in str.isspace])

def parseStringBySpace(string):
    	string = string.split(" ")
    	print string
    	return string

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        #print data
        #data = data.replace(',','')
        data = data.replace('\n','')
        data = data.replace('\t',' ')
        data = data.lower()
        data = letters(data)
        print data
        n.write(data)


# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(data)
