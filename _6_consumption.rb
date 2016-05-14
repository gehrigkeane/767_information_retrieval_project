module Consumption
	require 'csv'
	require 'pp'
	require 'benchmark'

	#--------------------------------------------------------------------------------
	#	Load the Inverted Index into main memory
	#		ii = 	{
	# 					term0:	[ document frequency, total frequency, posting_list ]
	# 					term1:	[	
	# 								df,
	# 								tf, 
	# 								[
	# 									[	filename,
	# 										[location 1 in filename, ...],
	# 										term frequency in filename
	# 									], ...
	# 								] - posting list, array of 3 element tuples
	# 							] - term value is an array of |3|
	# 					...
	# 				}
	#--------------------------------------------------------------------------------
	def self.load_ii(live=false)
		inverted_index, dict = {}, []

		CSV.foreach("3.ASSETS/ii.csv") do |row|
			term,df,tf,pl = row

			# Augment Dictionary
			dict.push(term)
			# Augment inverted index with strightforward information
			inverted_index[term.intern] = [df.to_i, tf.to_i, []]
			# Partition postings list into array of array's
			pl.split('`').each do |str|
				posting = str.split ';'
				posting[1] = posting[1].delete('[]').split(':') if posting[1]
				posting[1] = posting[1].map(&:to_i) if posting[1]
				posting[2] = posting[2].to_i

				inverted_index[term.intern][2].push(posting)
			end
		end

		i = 0
		dict_hash = {}
		dict.each do |term|
			dict_hash[i] = term
			i += 1
		end

		idf = {}

		# Simple retrieval of key,value pairs from csv file
		CSV.foreach("3.ASSETS/idf.csv") do |row|
			term,value = row
			idf[term.intern] = value.to_f.round(4)
		end

		# Index Fragmentation
		inverted_index.each do |term, list|
			temp = {}
			temp[term] = list
			File.open("3.ASSETS/ii/#{term}", 'w') {|f| f.write(Marshal.dump([temp,idf[term]])) }
		end

		# Dump inverted index and dictionary (much like python's pickle)
		#File.open('3.ASSETS/ii.mar', 'w') {|f| f.write(Marshal.dump(inverted_index)) }
		#File.open('3.ASSETS/dict.mar', 'w') {|f| f.write(Marshal.dump(dict)) }
		#File.open('3.ASSETS/dict_hash.mar', 'w') {|f| f.write(Marshal.dump(dict_hash)) }

		# Return the inverted index
		return inverted_index,dict if live
		return nil unless live
	end

	#--------------------------------------------------------------------------------
	#	 Load the Term IDF's into a hash
	#--------------------------------------------------------------------------------
	def self.load_idf(live=false)
		idf = {}

		# Simple retrieval of key,value pairs from csv file
		CSV.foreach("3.ASSETS/idf.csv") do |row|
			term,value = row
			idf[term.intern] = value.to_f.round(4)
		end

		File.open('3.ASSETS/idf.mar', 'w') {|f| f.write(Marshal.dump(idf)) }

		# Return the idf hash
		return idf if live
		return nil unless live
	end

	#--------------------------------------------------------------------------------
	#	 Load the Term IDF's into a hash
	#--------------------------------------------------------------------------------
	def self.load_snap(live=false)
		snap = {}

		# Simple retrieval of key,value pairs from csv file
		CSV.foreach("3.ASSETS/snap.csv") do |row|
			key,string = row
			snap[key.intern] = string if string
			snap[key.intern] = "No plot summary available..." unless string
		end

		# Index Fragmentation
		snap.each do |doc, string|
			temp = string.split
			File.open("3.ASSETS/snaps/#{doc}", 'w') {|f| f.write(Marshal.dump(temp)) }
		end

		File.open('3.ASSETS/snap.mar', 'w') {|f| f.write(Marshal.dump(snap)) }

		# Return the snap hash
		return snap if live
		return nil unless live
	end

	#--------------------------------------------------------------------------------
	#	 Load the Term snapshot's into a hash
	#--------------------------------------------------------------------------------
	def self.load_title(live=false)
		title = {}

		# Simple retrieval of key,value pairs from csv file
		CSV.foreach("3.ASSETS/title.csv") do |row|
			key,string = row
			title[key.intern] = string if string
			title[key.intern] = "broken title..." unless string
		end

		File.open('3.ASSETS/title.mar', 'w') {|f| f.write(Marshal.dump(title)) }

		# Return the title hash
		return title if live
		return nil unless live
	end


	#--------------------------------------------------------------------------------
	#	 Load the Document Vectors into an hash w/ k=term#, v=w_t,d
	#--------------------------------------------------------------------------------
	def self.load_dv(live=false)
		dv = {}

		# Retrieve name,vector pairs from csv
		CSV.foreach("3.ASSETS/dv.csv") do |row|
			name, vector = row
			#next unless name == '0007145.vector'
			vector = vector.split(';').map!{ |x| x.split(':').map(&:to_f) }
			vec = {}
			vector.each { |arr| vec[arr[1].to_i] = arr[0] }
			dv[name.intern] = vec
		end

		d_mag = {}
		dv.each do |key,value|
			key = key.intern
			value.each do |k,w|
				d_mag[key] = w ** 2 unless d_mag.key? key
				d_mag[key] += w ** 2 if d_mag.key? key
			end
			d_mag[key] = Math.sqrt(d_mag[key])
		end

		# Index Fragmentation
		dv.each do |doc, vector|
			temp = {}
			temp[doc] = vector
			File.open("3.ASSETS/dv/#{doc}", 'w') {|f| f.write(Marshal.dump([temp,d_mag[doc]])) }
		end		

		File.open('3.ASSETS/dmag.mar', 'w') {|f| f.write(Marshal.dump(d_mag)) }
		File.open('3.ASSETS/dv.mar', 'w') {|f| f.write(Marshal.dump(dv)) }

		#pp dv
		# Return document vector hash
		return dv if live
		return nil unless live
	end

	#--------------------------------------------------------------------------------
	#	 Retrieve document snapshots with appropriate words highlighted
	#--------------------------------------------------------------------------------
	def self.get_snap(id, query)
		snaps = Marshal.load(File.read('3.ASSETS/snap.mar'))
		query = query.downcase.split
		snap = snaps[id.intern].split
		
		snap.each_with_index do | term,i |
			if query.include? term.downcase
				snap[i] = "<b>" + term + "</b>"	
			end
		end
		
		snap.join(" ")
	end

	#--------------------------------------------------------------------------------
	#	 Retrieve document snapshots with appropriate words highlighted
	#--------------------------------------------------------------------------------
	def self.get_title(id)
		title = Marshal.load(File.read('3.ASSETS/title.mar'))
		title[id.intern]
	end
	
	#--------------------------------------------------------------------------------
	#	 Calculate Pagerank - query must be a frequency hash
	#--------------------------------------------------------------------------------
	def self.calc_pagerank(query)
		if File.file?('3.ASSETS/ii.mar') and File.file?('3.ASSETS/dict.mar')
			ii = Marshal.load(File.read('3.ASSETS/ii.mar'))
			dict = Marshal.load(File.read('3.ASSETS/dict.mar'))
		else
			ii,dict = load_ii(true)
		end

		if File.file?('3.ASSETS/idf.mar')
			idf = Marshal.load(File.read('3.ASSETS/idf.mar'))
		else
			idf = load_idf(true)
		end
		
		if File.file?('3.ASSETS/dmag.mar')
			d_mag = Marshal.load(File.read('3.ASSETS/dmag.mar'))
		else
			d_mag = load_dv_n(true)
		end

		sim = {}
		q_vector = {}
		q_mag = 0

		# Calculate Query vector magnitude - exclude words not in dictionary
		query.each do |term, tf_t|
			next unless dict.include? term
			q_mag += ( (tf_t * idf[term.intern]) ** 2 )
		end
		q_mag = Math.sqrt(q_mag)

		# Calculate Cosine Similarity
		query.each do |term, tf_t|
			next unless dict.include? term

			# 	Iterate through each relevant posting list and augment Cosine similarity figure
			# 	Note: the vecotr space is never actually constructed, it's generated dynamically
			# 	Vector norm's are precalculated for both the query and documents
			ii[term.intern][2].each do |posting|
				d_w = (posting[2] * idf[term.intern]) / d_mag[posting[0][0...7].intern]
				q_w = (tf_t * idf[term.intern]) / q_mag
				q_vector[term] = q_w

				if sim.key? posting[0][0...7]
					sim[posting[0][0...7]] += q_w * d_w
				else
					sim[posting[0][0...7]] = q_w * d_w
				end
			end
		end

		# Sort similarities return top ten
		sim = sim.sort_by { |key, value| value }.reverse
		sim[0..10]
	end

	def self.calc_relevance(query, docs)

		l_start = Time.now
		ii		= Marshal.load(File.read('3.ASSETS/ii.mar'))
		idf		= Marshal.load(File.read('3.ASSETS/idf.mar'))
		dv		= Marshal.load(File.read('3.ASSETS/dv.mar'))
		dict_hash 	= Marshal.load(File.read('3.ASSETS/dict_hash.mar'))
		l_fin = Time.now
		pp "Load Time: #{l_fin - l_start}"
		a = 1
		b = 0.8

		q_doc = {}

		# Get all of the terms from all relevant documents
		# => sum all relevant docs together
		t_start = Time.now()
		docs.each do |doc|
			next unless doc
			doc = doc+".vector"
			dv[doc.intern].each do |t_num,w_t|
				if q_doc.include? t_num
					q_doc[t_num] += w_t
				else
					q_doc[t_num] = w_t
				end
			end
		end

		# Multiply Sum-D_r by coefficient
		# => multiply by B/|D_r|
		c = b/(docs.length)
		q_doc.each do |t_num, w_t|
			term = dict_hash[t_num]
			query[term] = a * query[term] + c * w_t
		end

		#q_doc.sort_by { |key, value| key }.reverse

		# Perform Addition between a*q_0 and new vector (apply alpha to q_0)
		
		t_fin = Time.now

		pp q_doc
		pp t_fin - t_start
		pp q_doc.length



		# Send new query vector to ranking function
	end
end

#------------------------------------------------------------------------------------------
#	Construct Marshal files - default is return nil
#
#	Total Filesize diff after zero elimination
# => dict.mar 	(183KB)		(185KB)
# => dv.mar 	(761KB)		(26,231KB)
# => idf.mar 	(165KB)		(147KB)
# => ii.mar 	(3,631KB)	(11,346KB)
#
#	Filesizes Pre-5000 v. Post-5000
# => dict.mar	183			408
# => dmag.mar	26			149
# => dv.mar		761			3799
# => idf.mar	146			331
# => ii.mar		3631		16371
# => snap.mar	484			2537
# => title.mar	40			175
#
#	Filesizes post name truncation and rounding
# => dict.mar	408			408
# => dmag.mar	149			149
# => dv.mar		3799		3733
# => idf.mar	331			328		(round 4) 326
# => ii.mar		16371		13286
# => snap.mar	2537		
# => title.mar	175			
#------------------------------------------------------------------------------------------
#Consumption.load_ii
#Consumption.load_idf
Consumption.load_snap
#Consumption.load_title
#Consumption.load_dv

#Consumption.calc_relevance(['0013140','1520211','3220042','1201607','0241527'])
