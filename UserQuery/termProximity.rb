#does term proximity

#The question, I'm thinking through is how are we gonna
#factor term proximity with the cosine similarity


#turns a bunch of numbers delimited by commas
#from string to ints in an array
#e.g. "1,7,15" -> [1,7,15] of ints
def parseTermLocations(str)
  scores = []
  if str==""
    return 0
  end
  #we go through for each comma and push the terms to the array
  str.split(/, ?/).each do |loc|
    scores.push(loc.to_i)
  end
  return scores
end

#finds the score if the item was replaced with new location
#we are given the key, minHash, and newItem
def withReplacedItem(key, minHash, newItem)
  minHash.delete_if{|_,v| v == key}
  minHash[newItem] = key
  minV = minHash.keys.min
  maxV = minHash.keys.max
  newScore = maxV - minV
  #puts newScore
  return newScore
end

def calcMinScore(locHash, minHash, minV, maxV, minScore)
  #go through each word
  locHash.each do |key,array|
    #go through each location of the word instance
    for i in 1.. array.length-1
      #we check if with new item the score is smaller
      #if so, we replace it
      if minScore > withReplacedItem(key, minHash, locHash[key][i])
        minScore = withReplacedItem(key, minHash, locHash[key][i])
        minHash.delete_if{|_,v| v == key}
        minHash[locHash[key][i]] = key
      end
    end
  end
  puts minScore
end

#calls the other stuff
#takes the user query
def tpScore(webHash)
  locHash = {}

  #creates an array with an array of ints rather than string
  #e.g. lochHash["someword"] = "1,2,3,4"
  #-> lochHash["someword"] = [1,2,3,4]
  webHash.each do |key,array|
    locHash[key] = parseTermLocations(webHash[key])
  end

  minScore=0
  minV = 0
  maxV = 0
  #let's just add each loc to an array
  minHash = {}
  #find min, max, and the score of the locations given
  #by all the keys of the hash
  #e.g. a-1 b-5 c-3 d-9 score: 8, min: 1, max: 9
  locHash.each do |key,array|
    minHash[locHash[key][0]] = key
    if minV == 0
      minV = locHash[key][0]
      maxV = locHash[key][0]
    elsif locHash[key][0] > maxV
      maxV = locHash[key][0]
    elsif locHash[key][0] < minV
      minV = locHash[key][0]
    end
  end
  #initial min score
  minScore = maxV-minV

  #this function will find the min score accounting for
  #all the locations
  calcMinScore(locHash, minHash, minV, maxV, minScore)
end

simpleHash = {}
simpleHash["jayhawk"] = "1,7,15"
simpleHash["college"] = "2"
simpleHash["basketball"] = "4,9"

test2 = {}
test2['a'] = "1,7,11"
test2["b"] = "2,12"
test2["c"] = "4,9,13"

query = ["hello", "dude", "sore"]

tpScore(simpleHash)
tpScore(test2)
