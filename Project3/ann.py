#!/bin/env python

from functions import *
import numpy as np
import sys
import operator
import feature_extractor as fe

class ANN:

  def __init__(self, activation_function, error_function):
    #Define HyperParameters
    self.input_layer_size = 114
    self.output_layer_size = 2
    self.hidden_layer_size = 10
    self.learning_rate = 0.1
    self.activation_function = activation_function
    self.error_function = error_function
    #Initialize weights from layers 1-2
    self.W1 = np.random.randn(self.input_layer_size,\
                              self.hidden_layer_size).astype(np.float128)
    #Initialize weights from layers 2-3
    self.W2 = np.random.randn(self.hidden_layer_size,\
                              self.output_layer_size).astype(np.float128)

  def classify(self, tweets):
    inputs = self.get_input(tweets)
    self.forward_propagate(inputs)
    return self.prediction

  def get_input(self, tweets):
    inputs = []
    for tweet in tweets:
      bag = []
      for word in self.bag_of_words:
        bag.append(1) if word in tweet else bag.append(0)
      inputs.append(bag)
    input_size = len(inputs)
    bog_size = len(self.bag_of_words)
    return np.array(inputs, dtype=np.float128).reshape(input_size, bog_size)

  def forward_propagate(self, inputs):
    """Propagate input values through the network

    Keyword arguments:
    inputs -- Matrix containing all inputs to forward
    """
    #Forwarded values from layers 1 to 2
    self.z2 = np.dot(inputs, self.W1).astype(np.float128)
    #Output values from layer 2
    self.a2 = self.activate(self.z2, self.activation_function)
    #Forwarded values from layers 2 to 3
    self.z3 = np.dot(self.a2, self.W2).astype(np.float128)
    #Output from layer 3 (output layer)
    self.prediction = self.activate(self.z3, self.activation_function)

  def activate(self, z, function):
    """Apply an activation function to the activities of a layer

    Keyword arguments:
    z -- Matrix containing all activities of a layer
    function -- Integer representing which activation function to use
    """
    if function == Functions.SIGMOID:
      return sigmoid(z)
    elif function == Functions.SOFTMAX:
      return softmax(z)
    else:
      print("Unrecognized activation function")
      sys.exit(1)

  def back_propagate(self, expected_prediction, inputs):
    """Back propagates error through the network

    Keyword arguments:
    expected_prediction -- Matrix containing the expected net's output values
    inputs -- Matrix containing all inputs used to train the network
    """
    delta3 = self.get_delta3(expected_prediction)
    djdW2 = np.dot(self.a2.T, delta3)

    #Update weights from layers 2 to 3
    self.W2 = self.W2 - (self.learning_rate * djdW2)

    delta2 = self.get_delta2(delta3)
    djdW1 = np.dot(inputs.T, delta2)

    #Update weights from layers 1 to 2
    self.W1 = self.W1 - (self.learning_rate * djdW1)

  def train(self, inputs, expected_prediction):
    """ Trains the neuronal network by updating its weights.

    Keyword arguments:
    inputs -- Matrix containing all inputs used to train the network
    expected_predictions -- Matrix containing the expected net's output values
    max_err -- Expected maximum error for the network
    """
    self.forward_propagate(inputs)
    self.back_propagate(expected_prediction, inputs)
    self.forward_propagate(inputs)
    self.error = self.get_error(Functions.MSE, expected_prediction)

  def get_training_set(self, selected_tweets, rejected_tweets):
    st = fe.extract_features(selected_tweets)
    nst = fe.extract_features(rejected_tweets)
    self.set_bag_of_words(st, nst)
    bog_size = len(self.bag_of_words)
    inputs = []
    outs = []

    for tweet in selected_tweets:
      bag = []
      for word in self.bag_of_words:
        bag.append(1) if word in tweet else bag.append(0)
      inputs.append(bag)
      outs.append([1, 0])

    for tweet in rejected_tweets:
      bag = []
      for word in self.bag_of_words:
        bag.append(1) if word in tweet else bag.append(0)
      inputs.append(bag)
      outs.append([0, 1])
    input_size = len(inputs)
    out_size = len(outs)
    inputs = np.array(inputs, dtype=np.float128).reshape(input_size, bog_size)
    outs = np.array(outs, dtype=np.float128).reshape(out_size, 2)

    return inputs, outs

  def set_bag_of_words(self, st, nst):
    words_selected_tweets = sorted(st.items(), key=operator.itemgetter(1),\
                                   reverse=True)
    words_rejected_teets = sorted(nst.items(), key=operator.itemgetter(1),\
                                  reverse=True)
    bag_selected = [k for k, v in words_selected_tweets]
    bag_rejected = [k for k, v in words_rejected_teets]

    self.bag_of_words = bag_selected[:41] + bag_rejected[:73]

  def get_error(self, function, expected_prediction):
    """ Returns the net's total error.

    Key arguments:
    function -- Integer representing which error function to use
    expected_prediction -- Matrix containing the expected net's output values
    """
    if function == Functions.MSE:
      error = mse(expected_prediction, self.prediction)
      return error

  def get_delta3(self, expected_prediction):
    if self.error_function == Functions.MSE:
      if self.activation_function == Functions.SIGMOID or\
         self.activation_function == Functions.SOFTMAX:
        delta = np.multiply(mse_prime(expected_prediction, self.prediction),\
                            sigmoid_prime(self.prediction))
        return delta
    else:
      print("Error: function not recognized")
      sys.exit(1)

  def get_delta2(self, delta3):
    if self.error_function == Functions.MSE:
      if self.activation_function == Functions.SIGMOID or\
         self.activation_function == Functions.SOFTMAX:
        delta = np.dot(delta3, self.W2.T) * sigmoid_prime(self.z2)
        return delta
    else:
      print("Error: function not recognized")
      sys.exit(1)

def main():
  ann = ANN(Functions.SIGMOID, Functions.MSE)
  X = np.array([[3, 5], [5, 1], [10, 2]]).reshape(3, 2).astype(np.float128)
  X = X/np.amax(X, axis=0)
  Y = np.array([75, 82, 93]).reshape(3, 1).astype(np.float128)
  Y = Y/100

  ann.train(X, Y, 0.0056)
  ann.forward_propagate(X)
  yHat = ann.prediction
  print(yHat)

if __name__ == "__main__":
  main()
