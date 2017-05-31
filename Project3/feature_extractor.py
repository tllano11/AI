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

def get_relevant_words(s_tweets_features, r_tweets_features):
  for word in s_tweets_features:
    for word2 in r_tweets_features:
      if word in r_tweets_features:
        pass
      else:
        pass

if __name__ == "__main__":
  i_st = extract_features([['hola', 'hola'],\
                        ['hola', 'hola','hola'],\
                        ['usted','usted', 'como', 'usted']])
  i_nst = extract_features([['david', 'andres'], ['andres']])
  print("Selected tweets index: \n", i_st)
  print("Rejected tweets index: \n", i_nst)
