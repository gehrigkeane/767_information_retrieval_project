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
	def self.load_ii
		inverted_index = {}
		dict = []
		CSV.foreach("memory_assets/ii.csv") do |row|
			term,df,tf,pl = row
			#next if term != "stag"
			dict.push(term)
			inverted_index[term.intern] = [df.to_i, tf.to_i, []]
			pl.split('`').each do |str|
				posting = str.split ';'
				posting[1] = posting[1].delete('[]').split(':') if posting[1]
				posting[1] = posting[1].map(&:to_i) if posting[1]
				posting[2] = posting[2].to_i

				inverted_index[term.intern][2].push(posting)
			end

			# Debugging Term printing
			#puts "#{term}: "
			#pp inverted_index[:term]
		end

		# Return the inverted index
		return inverted_index,dict
	end

	#--------------------------------------------------------------------------------
	#	 Load the Term IDF's into a hash
	#
	#--------------------------------------------------------------------------------
	def self.load_idf
		idf = {}

		CSV.foreach("memory_assets/total_idf.csv") do |row|
			term,value = row
			idf[term.intern] = value.to_f
		end

		# Return the idf hash
		idf
	end

	#--------------------------------------------------------------------------------
	#	 Load the Document Vectors into an array of array's
	#
	#--------------------------------------------------------------------------------
	def load_dv
		dl = []

		CSV.foreach("memory_assets/document_list.csv") do |row|
			num,name = row
			dl.push(name)
		end

		CSV.foreach("memory_assets/document_vectors.csv") do |row|
			name,vector = row
			#incomplete logic
		end
	end
end


ii,dict = Consumption.load_ii

puts dict.sort

dl = []
i = 1
CSV.foreach("memory_assets/token_strings.csv") do |row|
	next if i > 1
	name,terms = row
	#print terms.delete('[\'').split(':').sort
	
	i += 1
end
