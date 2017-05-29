""" INSTALACION
sudo -H pip install setuptools
sudo -H pip install pyexcel
sudo -H pip install pyexcel-xlsx
nltk.download('punkt')
nltk.download('stopwords')
"""

import pyexcel as pe
import nltk
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
    #naiveBayes(listaTweets,listaTweets2)
    selected_tweets = tokenize(listaTweets)
    not_selected_tweets = tokenize(listaTweets2)

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

def snowball_stemmer(list_tokens):
    stemmer = SnowballStemmer("spanish")
    return stemmer.stem(str(list_tokens))

def stop_words(words):
    filteredWords = []
    stopWords = set(stopwords.words('spanish'))
    stopWords.update(["https", "http", "RT", "co"])
    for w in words:
        if w not in stopWords:
            filteredWords.append(stem_token(w))
    return filteredWords

def naiveBayes(listaTweets, listaTweets2):
    train = [(str(listaTweets), "Classified")]
    test = [(str(listaTweets2), "Unclassified")]
    cl = NaiveBayesClassifier(train)
    print(cl.classify(str(test)))

def main(archivo,archivo2):
    excel_reader(archivo,archivo2)

if __name__ == "__main__":
    main("./files/Tweets_Seleccionados.xlsx","./files/Todos.xlsx")
