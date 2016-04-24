import codecs, os, re, pprint, pickle, csv

in_path = "Plotsummary"
filenames = os.listdir(in_path)
total_film = {}
for fn in filenames:
	f = codecs.open("Plotsummary/%s"%fn,'r')
	content = f.read()
	ct = re.search(r'(\<meta\sproperty\=\'og\:title\'\scontent\=\")(.*)(\")',content)
	film_title = ct.group(2)
	cl = re.search(r'(\<meta\sproperty\=\"og\:url\"\scontent\=\")(.*)(\")',content)
	film_link = cl.group(2)
	total_film[fn[0:-5]] = [film_title,film_link]

f = open("document_list.pickle", "rb")
dl = []
while True:
	try:
		dl.append(pickle.load(f))
	except EOFError:
		break

final_list = []
for l in range(0, len(dl[0])):
	movie_id = dl[0][l][1]
	final_list.append([l, movie_id, total_film[movie_id][0],total_film[movie_id][1]])
#pprint.pprint(final_list)

with open("id_name_url.csv", 'a', newline='') as ff:
	writer = csv.writer(ff)
	for movie in final_list:
		#print(movie)
		wstring = str(movie[1])+';'+'"'+str(movie[2])+'"'+';'+str(movie[3])
		writer.writerow([movie[0],wstring])
#pprint.pprint(total_film)
	#<meta property='og:title' content="Back to the Future (1985)" />
	#<meta property="og:url" content="http://www.imdb.com/title/tt0088763/plotsummary" />