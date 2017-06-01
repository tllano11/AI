import lectura as reader
import numpy as np
import threading
import argparse
import sys
import pickle
from ann import ANN
from functions import Functions
from naive_bayes import NaiveBayes

ann_output = []
nb_output = []
xx_output = None

def train_net(net, selected_tweets, rejected_tweets):
  inputs, outs = net.get_training_set(selected_tweets, rejected_tweets)
  net.train(inputs, outs)
  net.get_error(Functions.MSE, outs)
  f = open('ann_trained.pickle', 'wb')
  pickle.dump(net, f)
  f.close()

def train_nb (nb, selected_tweets, rejected_tweets):
  nb.train(selected_tweets, rejected_tweets)
  f = open('naive_bayes_trained.pickle', 'wb')
  pickle.dump(nb, f)
  f.close()

def classify_using_net(net, tweets):
  global ann_output
  result = net.classify(tweets)
  for r in result:
    if r[0] >= r[1]:
      ann_output.append("selected")
    else:
      ann_output.append("rejected")

def classify_using_nb(nb, tweets):
  global nb_output
  for tweet in tweets:
    nb_output.append(nb.classify(tweet))

def get_help():
  message = "Usage: classifier.py [t <selected tweets> <rejected tweets>]\n"\
            "                  |  [c <ann_data> <nb_data> <tweets to classify>]"
  return message

def main(argv):
  argc = len(argv)
  if argc < 2:
    print(get_help())
    exit(0)

  if argv[1] == 't':
    net = ANN(Functions.SIGMOID, Functions.MSE)
    nb = NaiveBayes()
    selected_tweets = reader.read(argv[2])
    rejected_tweets = reader.read(argv[3])
    t1 = threading.Thread(target=train_net,\
                          args=(net, selected_tweets, rejected_tweets))
    t2 = threading.Thread(target=train_nb,\
                          args=(nb, selected_tweets, rejected_tweets))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

  elif argv[1] == 'c':
    f_net = open(argv[2], 'rb')
    net = pickle.load(f_net)
    f_net.close()

    f_nb = open(argv[3], 'rb')
    nb = pickle.load(f_nb)
    f_nb.close()

    tweets = reader.read(argv[4])

    t1 = threading.Thread(target=classify_using_net,\
                          args=(net, tweets))
    t2 = threading.Thread(target=classify_using_nb,\
                          args=(nb, tweets))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

  else:
    print(get_help())
    exit(0)

  print(ann_output)
  #print(nb_output)

if __name__ == "__main__":
  main(sys.argv)
