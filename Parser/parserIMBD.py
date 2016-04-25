import re
import os
import pickle
from HTMLParser import HTMLParser

#creates the global variable.. pretty bad programming
n = open("a.txt",'w')

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

    def handle_data(self, data):
        data = data.replace('\n',' ')
        data = data.replace('  ', ' ')
        data = data.replace('\t',' ')
        data = data.lower()
        if "document." in data: #filters out bad stuff
            data = ""
        if "\",\"" in data:
            #print data For testing purposes
            data = ""
        if "\"})" in data:
            data = ""
        if re.match('var', data):
            data = ""
        if data!= "" and data[0] == " ":
            data = data[1:]
        if re.match('if \(', data):
            data = ""
        if re.match('\w', data):
            data = data + " "
            #print(data)
            n.write(data)

# List and open every file in current dir

currDir = os.getcwd()
newDir = currDir + "/Plotsummary"
os.chdir(newDir)

html_files = [file for file in os.listdir(".") if file.endswith(".htm") or file.endswith(".html")]

    # x = file number 0, 1, ..., n
    # y = file name
for x,y in enumerate(html_files):
    #print(x, " ", y)
    with open(y, 'r') as fin:

        #certain image files that we don't really care for...
        data = fin.read().decode('ascii','ignore')

        #we first strip away the .htm part of the naming
        z =  y[:-4]
        n = open(z + ".txt",'w') #then we concatenate the rest
        parser = MyHTMLParser()
        parser.feed(data)

#temporary list to store each word
file_list = []
#os.remove("a.txt")
txtFiles = [file for file in os.listdir(".") if file.endswith(".txt")]

#FOR TESTING PURPOSES
#with open('Yosemite_National_Park.txt', 'r') as f:
#    for eachLine in f: #strips out the new lines from the file
#        file_list.append(eachLine.split())
#print file_list

for x,y in enumerate(txtFiles):
    with open(y, 'r') as f:
        for eachLine in f: #strips out the new lines from the file
            file_list.append(eachLine.split())
        #print file_list
        z =  y[:-4]
        n = open(z + ".pickle",'w')
        pickle.dump(file_list,n)
