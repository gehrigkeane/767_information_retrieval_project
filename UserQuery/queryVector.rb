load 'userQueryParser.rb'

#puts all my work together for the query vector

#made a few assumptions
#we know about TF-IDF

#the structure we have:
#key is the term, value is the list of 3 values,
#in addition to a posting list

#takes a string and makes it into a hashtable
#so like if query is "I am bad at examples examples"
#it would be userHash["bad"]=1 userHash["example"]=2
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

#takes 2 hashtables and produces
#the idf of each vector in the doc if we had one
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

  puts newArray
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
userQuery = "hello college jayhawk jayhawk college stupid rational stuff"
#userHash2 = queryHasher(userQuery)

produceVector(simpleHash, queryHasher(Stemmer(removeStopWords(userQuery))))
