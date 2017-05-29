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
        listaTweets2.append(tweet['Texto'])
    naiveBayes(listaTweets,listaTweets2)
    #tokenize(listaTweets)
    
def tokenize(lista):
    size = len(lista)
    for i in range(0, size):
        sentence = lista[i]
        list_tokens.append(nltk.word_tokenize(sentence))
    #porter_stemmer(list_tokens)
    #snowball_stemmer(list_tokens)
    #stop_words(list_tokens)
    naiveBayes(list_tokens)
    
def porter_stemmer(list_tokens):
    sentences = str(list_tokens)
    stemmer = PorterStemmer()
    return [stemmer.stem(str(sentence)) for sentence in sentences]

def snowball_stemmer(list_tokens):
    stemmer = SnowballStemmer("spanish")
    return stemmer.stem(str(list_tokens))

def stop_words(list_tokens):
    filteredWords = []
    stopWords = set(stopwords.words('spanish'))
    words = porter_stemmer(list_tokens)

    for i in words:
        if i not in stopWords:
            filteredWords.append(i)
    print(filteredWords)
    
def naiveBayes(listaTweets, listaTweets2):
    train = [(str(listaTweets), "Classified")]
    test = [(str(listaTweets2), "Unclassified")]
    cl = NaiveBayesClassifier(train)
    print(cl.classify(str(test)))
    
def main(archivo,archivo2):
    excel_reader(archivo,archivo2)
    
if __name__ == "__main__":
    main("./files/Tweets_Seleccionados.xlsx","./files/Todos.xlsx")
