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
from naive_bayes import NaiveBayes
from nltk.stem import *
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

"""Funcion para la lectura del archivo de excel con el campo texto predefinido"""

def read(nombreArchivo,nombreArchivo2):
    listaTweets = []
    listaTweets2 = []
    excel = pe.iget_records(file_name=nombreArchivo)
    excel2 = pe.iget_records(file_name=nombreArchivo2)
    for tweet in excel:
        listaTweets.append(tweet['Texto'])
    for tweet2 in excel2:
        listaTweets2.append(tweet2['Texto'])
    return tokenize(listaTweets),tokenize(listaTweets2)

def tokenize(tweets):
    list_tokens = []
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

def stop_words(words):
    filteredWords = []
    stopWords = set(stopwords.words('spanish'))
    stopWords.update(["https", "http", "RT", "co"])
    for w in words:
        if w not in stopWords:
            filteredWords.append(stem_token(w))
    return filteredWords

def main(archivo,archivo2):
    selected_tweets, rejected_tweets = read(archivo,archivo2)
    naive_bayes = NaiveBayes()
    naive_bayes.train(selected_tweets, rejected_tweets)
    result = naive_bayes.classify(rejected_tweets[0])
    print(result)
    
if __name__ == "__main__":
    main("./files/Tweets_Seleccionados.xlsx","./files/Tweets_Rechazados.xlsx")
