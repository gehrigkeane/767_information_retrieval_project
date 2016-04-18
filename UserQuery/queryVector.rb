load 'userQueryParser.rb'

#made a few assumptions
#we know about TF-IDF

#the structure we have:
#key is the term, value is the list of 3 values,
#in addition to a posting list

#we would take our query that's been stemmed
#for each document
#for i in 0 ... userQuery.size
#  if simpleHash.has_key?(userQuery[i])
  #  puts "it's true bro"
    #we would put the idfs here
#  end
#end


def queryHasher(userQuery)
  userHash = {}
  userQuery.gsub(/\s+/m, ' ').strip.split(" ").each do |word|
    if userHash.has_key? word
      userHash[word] = userHash[word] + 1
    else
      userHash[word] = 1
    end
  end
  puts userHash
  return userHash
end


def produceVector(webHash, userHash)
  newArray = []
  webHash.each do |key, array|
    if userHash.has_key? key
      temp = userHash[key]*webHash[key]
      newArray.push(temp)
    else
      newArray.push(0)
    end
  end

  #use it and pass it
  for i in 0 ... newArray.size
    puts newArray[i]
  end
end

simpleHash = {}
simpleHash['jayhawk'] = 0.602
simpleHash["college"] = 0
simpleHash["basketball"] = 0.301
simpleHash["university"] = 0.125

#user hash will have term as key, & tf as value
userHash = { }
userHash['jayhawk'] = 2.0
userHash["college"] = 3.0
userHash["basketball"] = 1.0
userHash["university"] = 0.0

#produceVector(simpleHash, userHash)
userQuery = "hello college jayhawk college stupid rational stuff"
#userHash2 = queryHasher(userQuery)

produceVector(simpleHash, queryHasher(Stemmer(removeStopWords(userQuery))))
