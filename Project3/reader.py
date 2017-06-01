import nltk
import pandas
import operator
import numpy as np
import pyexcel as pe
from nltk.stem import *
from ann import ANN
import feature_extractor as fe
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from naive_bayes import NaiveBayes
from nltk.tokenize import RegexpTokenizer

from functions import Functions

def read(file_name):
    tweets = []
    excel = pe.iget_records(file_name=file_name)
    for tweet in excel:
        tweets.append(tweet['Texto'])
    return tokenize(tweets)

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

def train_net(net, selected_tweets, rejected_tweets):
    inputs, outs = net.get_training_set(selected_tweets, rejected_tweets)
    net.train(inputs, outs)

def classify_using_net(net, tweets):
    global net_output
    result = net.classify(tweets)
    for r in result:
        if r[0] >= r[1]:
            net_output.append("selected")
        else:
            net_output.append("rejected")
