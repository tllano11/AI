import reader
import numpy as np
import threading
import argparse
import sys
import pickle
import csv
from ann import ANN
from functions import Functions
from naive_bayes import NaiveBayes
from bernoulli import Bernoulli

ann_output = []
nb_output = []
bn_output = []

def train_net(net, selected_tweets, rejected_tweets):
  inputs, outs = net.get_training_set(selected_tweets, rejected_tweets)
  net.train(inputs, outs)
  net.get_error(Functions.MSE, outs)
  f = open('ann_trained.pickle', 'wb')
  pickle.dump(net, f)
  f.close()
  with open('error_ann.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(net.error)

def train_nb (nb, selected_tweets, rejected_tweets):
  nb.train(selected_tweets, rejected_tweets)
  f = open('naive_bayes_trained.pickle', 'wb')
  pickle.dump(nb, f)
  f.close()

def train_bn (bn, selected_tweets, rejected_tweets):
  bn.train(selected_tweets, rejected_tweets)
  f = open('bernoulli_trained.pickle', 'wb')
  pickle.dump(bn, f)
  f.close()

def classify_using_net(net, tweets):
  global ann_output
  result = net.classify(tweets)
  for r in result:
    if r[0] >= r[1]:
      ann_output.append("selected")
    else:
      ann_output.append("rejected")

  with open('results_ann.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(ann_output)

def classify_using_nb(nb, tweets):
  global nb_output
  for tweet in tweets:
    nb_output.append(nb.classify(tweet))
  with open('results_naive_bayes.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(nb_output)

def classify_using_bn(bn, tweets):
  global bn_output
  for tweet in tweets:
    bn_output.append(bn.classify(tweet))
  with open('results_bernoulli.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(bn_output)

def get_help():
  message = "Usage: classifier.py [t <selected tweets> <rejected tweets>]\n"\
            "                  |  [c <ann_data> <nb_data> <bn_data> <tweets to classify>]"
  return message

def main(argv):
  argc = len(argv)
  if argc < 2:
    print(get_help())
    exit(0)

  if argv[1] == 't':
    net = ANN(Functions.SIGMOID, Functions.MSE)
    nb = NaiveBayes()
    bn = Bernoulli()
    selected_tweets = reader.read(argv[2])
    rejected_tweets = reader.read(argv[3])
    t1 = threading.Thread(target=train_net,\
                          args=(net, selected_tweets, rejected_tweets))
    t2 = threading.Thread(target=train_nb,\
                          args=(nb, selected_tweets, rejected_tweets))
    t3 = threading.Thread(target=train_bn,\
                          args=(bn, selected_tweets, rejected_tweets))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()

  elif argv[1] == 'c':
    f_net = open(argv[2], 'rb')
    net = pickle.load(f_net)
    f_net.close()

    f_nb = open(argv[3], 'rb')
    nb = pickle.load(f_nb)
    f_nb.close()

    f_bn = open(argv[4], 'rb')
    bn = pickle.load(f_bn)
    f_bn.close()

    tweets = reader.read(argv[5])

    t1 = threading.Thread(target=classify_using_net,\
                          args=(net, tweets))
    t2 = threading.Thread(target=classify_using_nb,\
                          args=(nb, tweets))
    t3 = threading.Thread(target=classify_using_bn,\
                          args=(bn, tweets))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
  else:
    print(get_help())
    exit(0)

if __name__ == "__main__":
  main(sys.argv)
