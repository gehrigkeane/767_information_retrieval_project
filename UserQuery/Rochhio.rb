#adds two arrays of ints
def queryAddition(query1, query2)
  for i in 0..query1.length-1
    #temp = query1[i]+query2[i]
    temp1 =  query1[i].to_f
    temp2 = query2[i].to_f
    temp3 = temp1 + temp2
    query1[i] = temp3
  end
  return query1
end

#pass in a array of query words
#pass in array of 2d array rel docs
#same with irrev docs
#basically Rocchio equation
def newQuery(query, relev, irrelev)
  #recommended values by wiki
  alpha = 1
  beta = 0.8
  betaQuery = []
  for i in 0..relev[0].length-1
    betaQuery[i] = relev[0][i]
  end

  if alpha!=1
    for i in 0..query.length-1
      query[i] = query[i].to_f*alpha
    end
  end

  for i in 1..relev.length-1
    betaQuery = queryAddition(betaQuery, relev[i])
  end

  for i in 0..betaQuery.length-1
    betaQuery[i] = (betaQuery[i].to_f/ relev.length) * 0.8
  end

  feedbackQuery = queryAddition(query, betaQuery)
  #puts feedbackQuery
  return feedbackQuery

end

simpleQueryVector = [0,0,0.301,0.125]
arrOfArrs = [[0,0,0.301,0.25],[0.4,0.23,0,0]]

puts newQuery(simpleQueryVector, arrOfArrs, arrOfArrs)
