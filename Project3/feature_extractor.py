import nltk
import numpy as np


def extract_features(selected_tweets, not_selected_tweets):
  selected_tweets = np.array(selected_tweets, dtype=object)
  not_selected_tweets = np.array(not_selected_tweets, dtype=object)

  #All words from all selected tweets
  words_in_st = np.hstack(selected_tweets.flat)
  #All words from all rejected tweets
  words_in_nst = np.hstack(not_selected_tweets.flat)

  #Size of selected tweets
  size_st = len(selected_tweets)
  #Size of not selected tweets
  size_nst = len(not_selected_tweets)

  word_tweets_amount = {}

  #Computes how many documments have at least one instance of each word.
  for word in set(words_in_st):
    for tweet in selected_tweets:
      if word in tweet:
        if word in word_tweets_amount:
          word_tweets_amount[word] += 1
        else:
          word_tweets_amount[word] = 1
  word_index = {}

  #Computes "relevance index" for each word.
  for tweet in selected_tweets:
    word_frequence_tweet = nltk.FreqDist(tweet)
    for word in word_frequence_tweet:
      index = (word_frequence_tweet[word]/word_tweets_amount[word])/size_st
      if word not in word_index:
        word_index[word] = index
      else:
        word_index[word] += index
  return word_index

if __name__ == "__main__":
  i = extract_features([['hola', 'hola'],\
                        ['hola', 'hola','hola'],\
                        ['usted','usted', 'como', 'usted']],\
                       [['david', 'andres'], ['andres']])
  print(i)
