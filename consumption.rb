module Consumption
	require 'csv'
	require 'pp'

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

		CSV.foreach("memory_assets/ii.csv") do |row|
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
		File.open('memory_assets/ii.mar', 'w') {|f| f.write(Marshal.dump(inverted_index)) }
		File.open('memory_assets/dict.mar', 'w') {|f| f.write(Marshal.dump(dict)) }

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
		CSV.foreach("memory_assets/idf.csv") do |row|
			term,value = row
			idf[term.intern] = value.to_f
		end

		File.open('memory_assets/idf.mar', 'w') {|f| f.write(Marshal.dump(idf)) }

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
		CSV.foreach("memory_assets/dv.csv") do |row|
			name, vector = row
			vector = vector.delete('[]').split(':').map(&:to_f)
			dv[name.intern] = vector
		end

		File.open('memory_assets/dv.mar', 'w') {|f| f.write(Marshal.dump(dv)) }

		# Return document vector hash
		return dv if live
		return nil unless live
	end
	
	#--------------------------------------------------------------------------------
	#	 Simply calculate dot product of two vectors
	# => see the following for benchmarks
	# => http://stackoverflow.com/questions/7372489/whats-the-efficient-way-to-multiply-two-arrays-and-get-sum-of-multiplied-values/7373434#7373434
	#--------------------------------------------------------------------------------
	def self.calc_sim(qv, dv)
		sum, i, size = 0, 0, qv.size
		while i < size
			sum += qv[i] * dv[i]
			i += 1
		end
		sum
	end
	
	#--------------------------------------------------------------------------------
	#	 Calculate Pagerank
	#--------------------------------------------------------------------------------
	def self.calc_pagerank(query)
		if File.file?('memory_assets/ii.mar') and File.file?('memory_assets/dict.mar')
			ii = Marshal.load(File.read('memory_assets/ii.mar'))
			dict = Marshal.load(File.read('memory_assets/dict.mar'))
		else
			ii,dict = load_ii
		end

		if File.file?('memory_assets/idf.mar')
			idf = Marshal.load(File.read('memory_assets/idf.mar'))
		else
			idf = load_idf
		end
		
		if File.file?('memory_assets/dv.mar')
			dv = Marshal.load(File.read('memory_assets/dv.mar'))
		else
			dv = load_dv
		end

		# Gather candidate vectors
		# calculate similarity based off candidates - of course
		candidate_docs = []
		sim = {}
		q_freq = {}
		qv = Array.new(dict.length, 0)

		# Retrieve candidate documents from Inverted index
		query.each do |term|
			#puts "#{term}: #{ii[term.intern][2]}" if ii[term.intern]
			# Build a small query dictionary for weight calculation later
			q_freq[term] += 1 if q_freq.key?(term)
			q_freq[term] = 1 unless q_freq.key?(term)

			# Retrieve all documents that contain a query term
			next if ii[term.intern][0] == dv.length		#skip if query term not in dictionary
			#puts "#{term}: #{ii[term.intern][0]}"
			ii[term.intern][2].each do |posting|
				candidate_docs |= [posting[0]]
			end
		end
		
		# Create query vector for calculation
		dict.each_with_index do |term, i|
			qv[i] = q_freq[term] * idf[term.intern] if query.include?(term)
		end
		
		# Calculate all necessary similarities
		candidate_docs.each do |doc|
			sim[doc] = calc_sim(qv, dv[doc.intern])
		end

		# Sort similarities
		sim = sim.sort_by { |key, value| value }.reverse

		return sim[0..10]
	end
end

# To build mar files
#Consumption.load_ii
#Consumption.load_idf
#Consumption.load_dv

# Query Example - terms pulled from 0097574-tokens.pickle
query = ['date','1989','american','journalist','work','french','newspap','write','articl','reaction','peopl','aid','without','know','infect','find','decid','cut','leav','wife','daughter']
#query = [	'1989','journalist','newspap','articl','reaction','infect' ]
pp Consumption.calc_pagerank(query)
