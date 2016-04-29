#require_dependency 'PorterStemmer'
#load 'PorterStemmer.rb'
module StringToFreqHash

  require 'fast_stemmer'

  #takes a string and stems the word
  #then returns a hashtable with key being the word, and value being freq
  def self.queryHasher(userQuery)
    userHash = {}
    userQuery.gsub(/\s+/m, ' ').strip.split(" ").each do |word|
      temp = ""
      temp << word.stem
      if userHash.has_key? temp
        userHash[temp] = userHash[temp] + 1
      else
        userHash[temp] = 1
      end
    end
    return userHash
  end
end
