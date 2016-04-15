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
	def load_ii
		inverted_index = {}

		CSV.foreach("memory_assets/ii.csv") do |row|
			term,df,tf,pl = row
			#next if term != "stag"
			inverted_index[:term] = [df.to_i, tf.to_i, []]
			pl.split('`').each do |str|
				posting = str.split ';'
				posting[1] = posting[1].delete('[]').split(':') if posting[1]
				posting[1] = posting[1].map(&:to_i) if posting[1]
				posting[2] = posting[2].to_i

				inverted_index[:term][2].push(posting)
			end

			# Debugging Term printing
			#puts "#{term}: "
			#pp inverted_index[:term]
			inverted_index
		end
	end

	#--------------------------------------------------------------------------------
	#	 Load the Document Index into an array of array's
	#
	#--------------------------------------------------------------------------------
	def load_di
		nil
	end

	#--------------------------------------------------------------------------------
	#	 Load the Document Vectors into an array of array's
	#
	#--------------------------------------------------------------------------------
	def load_dv
		nil
	end
end