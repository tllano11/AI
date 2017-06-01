import nltk
import sys
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from nltk.classify.scikitlearn import SklearnClassifier

class Bernoulli:
    def __init__(self):
        self.classifier = None
        self.word_features = None

    def train(self, listaTweets, listaTweets2):
        selected_tweets = listaTweets
        rejected_tweets = listaTweets2
        self.word_features = self.features(selected_tweets, rejected_tweets)
        training_set = self.get_training_set(selected_tweets, rejected_tweets)
        self.classifier = SklearnClassifier(BernoulliNB())
        self.classifier.train(training_set)

    def features(self, selected_tweets, rejected_tweets):
        selected_tweets = np.array(selected_tweets,dtype=object)
        selected_tweets = np.hstack(selected_tweets.flat)
        rejected_tweets = np.array(rejected_tweets,dtype=object)
        rejected_tweets = np.hstack(rejected_tweets.flat)
        wordlist1 = nltk.FreqDist(selected_tweets)
        wordlist2 = nltk.FreqDist(rejected_tweets)
        word_features1,v = zip(*wordlist1.most_common())
        word_features2,g = zip(*wordlist2.most_common())
        return word_features1+word_features2

    def extract_features(self, tweet):
        if self.word_features is not None:
            tweet_words = set(tweet)
            features = {}
            for word in self.word_features:
                features['contains(%s)' % word] = (word in tweet_words)
            return features
        else:
            print("Bernoulli  must be trained before classifying")
            sys.exit(1)

    def get_training_set(self, selected_tweets, rejected_tweets):
        training_set = []
        for tweet in selected_tweets:
            training_set.append((self.extract_features(tweet),"selected"))

        for tweet in rejected_tweets:
            training_set.append((self.extract_features(tweet),"rejected"))
        return training_set

    def classify(self, inputs):
        if self.classifier is not None:
            return self.classifier.classify(self.extract_features(inputs))
