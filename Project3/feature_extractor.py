import nltk
import numpy as np


def extract_features(tweets):
  tweets = np.array(tweets, dtype=object)

  #All words from all tweets
  words_in_st = np.hstack(tweets.flat)

  #Size of  tweets
  size_st = len(tweets)

  word_tweets_amount = {}

  #Computes how many documments have at least one instance of each word.
  for word in set(words_in_st):
    for tweet in tweets:
      if word in tweet:
        if word in word_tweets_amount:
          word_tweets_amount[word] += 1
        else:
          word_tweets_amount[word] = 1
  word_index = {}

  #Computes "relevance index" for each word.
  for tweet in tweets:
    word_frequence_tweet = nltk.FreqDist(tweet)
    for word in word_frequence_tweet:
      index = (word_frequence_tweet[word]/word_tweets_amount[word])/size_st
      if word not in word_index:
        word_index[word] = index
      else:
        word_index[word] += index
  return word_index
