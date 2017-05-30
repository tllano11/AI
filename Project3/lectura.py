""" INSTALACION
sudo -H pip install setuptools
sudo -H pip install pyexcel
sudo -H pip install pyexcel-xlsx
nltk.download('punkt')
nltk.download('stopwords')
"""

import pyexcel as pe
import nltk
import numpy as np
from nltk.stem import *
from nltk.corpus import stopwords
from textblob.classifiers import NaiveBayesClassifier
from nltk.tokenize import RegexpTokenizer

listaTweets = []
listaTweets2 = []
list_tokens = []

"""Funcion para la lectura del archivo de excel con el campo texto predefinido"""

def excel_reader(nombreArchivo,nombreArchivo2):
    excel = pe.iget_records(file_name=nombreArchivo)
    excel2 = pe.iget_records(file_name=nombreArchivo2)
    for tweet in excel:
        listaTweets.append(tweet['Texto'])#.encode('utf-8'))          #Creacion de una lista con los tweets
    for tweet2 in excel:
        listaTweets2.append(tweet2['Texto'])
    selected_tweets = tokenize(listaTweets)
    dict_selected = features(selected_tweets)
    training_set1 = get_training_set("selected", selected_tweets, dict_selected)
    rejected_tweets = tokenize(listaTweets2)
    dict_rejected = features(rejected_tweets)
    training_set2 = get_training_set("rejected",rejected_tweets, dict_rejected)
    print(training_set1)

def get_training_set(label, tweets, word_features):
    training_set = []
    for tweet in tweets:
        training_set.append((extract_features(tweet,word_features),label))
    return training_set
    
def tokenize(tweets):
    tokenizer = RegexpTokenizer("[a-zA-Z]+[a-zA-Z]+[a-zA-Z]*")
    for tweet in tweets:
        words = tokenizer.tokenize(tweet)
        list_tokens.append(stop_words(words))
    return list_tokens

def porter_stemmer(list_tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(sentence) for sentence in list_tokens]

def stem_token(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)

# def snowball_stemmer(list_tokens):
#     stemmer = SnowballStemmer("spanish")
#     return stemmer.stem(str(list_tokens))

def stop_words(words):
    filteredWords = []
    stopWords = set(stopwords.words('spanish'))
    stopWords.update(["https", "http", "RT", "co"])
    for w in words:
        if w not in stopWords:
            filteredWords.append(stem_token(w))
    return filteredWords

def features(lista):
    tweets = np.array(lista,dtype=object)
    tweets = np.hstack(tweets.flat)
    wordlist = nltk.FreqDist(tweets)
    word_features,v = zip(*wordlist.most_common())
    return word_features

def extract_features(tweet, word_features):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def naiveBayes(selected_tweets, rejected_tweets):
    pass
    # train = [(str(tokenize(listaTweets)), "Classified")]
    # test = [(str(tokenize(listaTweets2)), "Unclassified")]
    # cl = NaiveBayesClassifier(train)
    # #return cl.classify(str(test))
    # return train

def main(archivo,archivo2):
    excel_reader(archivo,archivo2)

if __name__ == "__main__":
    main("./files/Tweets_Seleccionados.xlsx","./files/Todos.xlsx")
