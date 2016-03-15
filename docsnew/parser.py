import re
import os
from HTMLParser import HTMLParser

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
        data = data.replace('\n',' ')
        data = data.replace('  ', ' ')
        data = data.replace('\t',' ')
        data = data.lower()
        data = letters(data)
        if "document." in data:
            data = ""
        if "{{{" in data:
            data = ""
        if "\",\"" in data:
            data = ""
        if "\"})" in data:
            data = ""
        if re.match('\w', data):
            data = data + " "
            n.write(data)


# List and open every file in current dir
html_files = [file for file in os.listdir(".") if file.endswith(".htm") or file.endswith(".html")]

    # x = file number 0, 1, ..., n
    # y = file name
for x,y in enumerate(html_files):
    with open(y, 'r') as fin:
        data = fin.read().decode('ascii','ignore')

        z =  y[:-4]
        n = open(z + ".txt",'w')
        parser = MyHTMLParser()
        parser.feed(data)

#print data

    #write the files


    # instantiate the parser and fed it some HTML
    #parser = MyHTMLParser()
    #parser.feed(data)
