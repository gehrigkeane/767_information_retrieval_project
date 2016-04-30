import codecs, os, re, pprint, pickle, csv

in_path = "Plotsummary"
filenames = os.listdir(in_path)
total_film = []
for fn in filenames:
	f = codecs.open("Plotsummary/%s"%fn,'r')
	content = f.read()
	try:
		ct = re.search(r'(\<meta\sproperty\=\'og\:title\'\scontent\=\")(.*)(\")',content)
		film_title = ct.group(2)
		if "&quot;" in film_title:
			film_title = re.sub(r'\&quot\;', '',film_title)
		print(film_title)
		total_film.append([fn[0:-5], film_title]) 
		print("why?")
	except:
		print("File %s is empty!"%fn)
		continue

with open("id_name.csv", 'a', newline='') as ff:
	writer = csv.writer(ff)
	for m in total_film:
		mt = '"%s"'%m[1]
		writer.writerow([str(m[0]),str(mt)])
#pprint.pprint(total_film)
	#<meta property='og:title' content="Back to the Future (1985)" />
	#<meta property="og:url" content="http://www.imdb.com/title/tt0088763/plotsummary" />