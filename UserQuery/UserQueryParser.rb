load 'PorterStemmer.rb'

class String
  include Stemmable
end

def Stemmer(a)
  returnStr = ""
  a.gsub(/\s+/m, ' ').strip.split(" ").each do |word|
    returnStr << word.stem
    returnStr << " "
  end
  return returnStr
end

def removeStopWords(a)
  stopWords  = ["","a","ago","also","am","an","and","ani","ar","aren't","arent",
            "as","ask","at","did","didn't","didnt","do","doe","would",
            "be","been","best","better"]
  return a.split.delete_if{|x| stopWords.include?(x.downcase)}.join(' ')
end

b = "why this coalition wants me to do stupid stuff that's irrational"
b =  removeStopWords(b)
#puts Stemmer(b)

#given a string by a user, this class creates a stemmed string
