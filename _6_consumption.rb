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

		# Dump inverted index and dictionary (much like python's pickle)
		File.open('3.ASSETS/ii.mar', 'w') {|f| f.write(Marshal.dump(inverted_index)) }
		File.open('3.ASSETS/dict.mar', 'w') {|f| f.write(Marshal.dump(dict)) }

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
			idf[term.intern] = value.to_f
		end

		File.open('3.ASSETS/idf.mar', 'w') {|f| f.write(Marshal.dump(idf)) }

		# Return the idf hash
		return idf if live
		return nil unless live
	end

	#--------------------------------------------------------------------------------
	#	 Load the Document Vectors into an array of array's
	#--------------------------------------------------------------------------------
	def self.load_dv(live=false)
		dv = {}

		# Retrieve name,vector pairs from csv
		CSV.foreach("3.ASSETS/dv.csv") do |row|
			name, vector = row
			vector = vector.delete('[]').split(':').map(&:to_f)
			dv[name.intern] = vector
		end

		File.open('3.ASSETS/dv.mar', 'w') {|f| f.write(Marshal.dump(dv)) }

		# Return document vector hash
		return dv if live
		return nil unless live
	end

	#--------------------------------------------------------------------------------
	#	 Load the Document Vectors into an hash w/ k=term#, v=w_t,d
	#--------------------------------------------------------------------------------
	def self.load_dv_n(live=false)
		dv = {}

		# Retrieve name,vector pairs from csv
		CSV.foreach("3.ASSETS/dv.csv") do |row|
			name, vector = row
			#next unless name == '0007145-vector'
			vector = vector.split(';').map!{ |x| x.split(':').map(&:to_f) }
			vec = {}
			vector.each { |arr| vec[arr[1].to_i] = arr[0] }
			#pp vector
			dv[name.intern] = vec
		end

		File.open('3.ASSETS/dv.mar', 'w') {|f| f.write(Marshal.dump(dv)) }

		# Return document vector hash
		return dv if live
		return nil unless live
	end
	
	#--------------------------------------------------------------------------------
	#	 Simply calculate dot product of two vectors
	# => see the following for benchmarks
	# => http://stackoverflow.com/questions/7372489/whats-the-efficient-way-to-multiply-two-arrays-and-get-sum-of-multiplied-values/7373434#7373434
	#
	# => hash resources: http://stackoverflow.com/questions/8407756/ruby-for-each-key-value-pair-in-a-hash
	#--------------------------------------------------------------------------------
	def self.calc_sim(qv, dv)
		#while i < size
		#	sum += qv[i][0] * dv[i][0]
		#	i += 1
		#end
		sum, i, size = 0, 0, qv.size
		qv.each { |key,value| sum += value * dv[key] if dv.key? key }
		sum
	end
	
	#--------------------------------------------------------------------------------
	#	 Calculate Pagerank
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
		
		if File.file?('3.ASSETS/dv.mar')
			dv = Marshal.load(File.read('3.ASSETS/dv.mar'))
		else
			dv = load_dv_n(true)
		end

		# Gather candidate vectors
		# calculate similarity based off candidates - of course
		candidate_docs = []
		sim = {}
		q_freq = {}
		qv = {}

		# Retrieve candidate documents from Inverted index
		query.each do |term|
			#puts "#{term}: #{ii[term.intern][2]}" if ii[term.intern]
			# Build a small query dictionary for weight calculation later
			next unless dict.include? term 
			q_freq[term] += 1 if q_freq.key?(term)
			q_freq[term] = 1 unless q_freq.key?(term)

			# Retrieve all documents that contain a query term
			#puts "#{term}: #{ii[term.intern][0]}"
			ii[term.intern][2].each do |posting|
				#puts posting
				candidate_docs |= [posting[0].sub('token','vector')]
			end
		end
		
		#puts q_freq
		# Create query vector for calculation
		dict.each_with_index do |term, i|
			qv[i] = q_freq[term] * idf[term.intern]	if query.include?(term)#qv.push(Array.new([q_freq[term] * idf[term.intern],i])) if query.include?(term)
		end

		#pp candidate_docs
		#pp dv[candidate_docs[0].intern]

		# Calculate all necessary similarities
		candidate_docs.each do |doc|
		#	pp dv[doc.intern]
		#	next unless doc == candidate_docs[0]
			sim[doc] = calc_sim(qv, dv[doc.intern])
		end

		#pp sim

		# Sort similarities
		sim = sim.sort_by { |key, value| value }.reverse

		return sim[0..10], candidate_docs.length
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
#------------------------------------------------------------------------------------------
# Consumption.load_ii
# Consumption.load_idf
# Consumption.load_dv_n

#------------------------------------------------------------------------------------------
#	Query Example - terms pulled from 0097574-tokens.pickle
#------------------------------------------------------------------------------------------
query = ['date','1989','american','journalist','work','french','newspap','write','articl','reaction','peopl','aid','without','know','infect','find','decid','cut','leav','wife','daughter']
query1 = [	'1989','journalist','newspap','articl','reaction','infect' ]
#pp Consumption.calc_pagerank(query) 
s,l = 0,0
Benchmark.bm(7) do |x|
	x.report("1:")	{ Consumption.calc_pagerank(query) }
	x.report("2:")	{ Consumption.calc_pagerank(query) }
	x.report("3:")	{ s,l = Consumption.calc_pagerank(query) }
end
pp "Query candidate_docs: #{l}"

Benchmark.bm(7) do |x|
	x.report("1:")	{ Consumption.calc_pagerank(query1) }
	x.report("2:")	{ Consumption.calc_pagerank(query1) }
	x.report("3:")	{ s,l = Consumption.calc_pagerank(query1) }
end
pp "Query1 candidate_docs: #{l}"
