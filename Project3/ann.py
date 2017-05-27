#!/bin/env python

from functions import *
import numpy as np
import sys

class ANN:

  def __init__(self, activation_function, error_function):
    #Define HyperParameters
    self.input_layer_size = 1
    self.output_layer_size = 2
    self.hidden_layer_size = 3
    self.activation_function = activation_function
    self.error_function = error_function
    #Initialize weights from layers 1-2
    self.W1 = np.random.randn(self.input_layer_size,\
                              self.hidden_layer_size)
    #Initialize weights from layers 2-3
    self.W2 = np.random.randn(self.hidden_layer_size,\
                              self.output_layer_size)


  def forward_propagate(self, inputs):
    """Propagate input values through the network

    Keyword arguments:
    inputs -- Matrix containing all inputs to forward
    """
    #Forwarded values from layers 1 to 2
    self.z2 = np.dot(inputs, self.W1)
    #Output values from layer 2
    self.a2 = self.activate(self.z2, Functions.SIGMOID)
    #Forwarded values from layers 2 to 3
    self.z3 = np.dot(self.a2, self.W2)
    #Output from layer 3 (output layer)
    self.prediction = self.activate(self.z3, Functions.SIGMOID)


  def activate(z, function):
    """Apply an activation function to the activities of a layer

    Keyword arguments:
    z -- Matrix containing all activities of a layer
    function -- Integer representing which activation function to use
    """
    if function == Functions.SIGMOID:
      return sigmoid(z)
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

    delta2 = self.get_delta2(delta3)
    djdW1 = np.dot(inputs.T, delta2)

    return djdW1, djdW2


  def get_delta3(self, expected_prediction):
    if self.error_function == Functions.MSE:
      if self.activation_function == Functions.SIGMOID:
        delta = np.multiply(mse_prime(expected_prediction, self.prediction),\
                            sigmoid_prime(self.prediction))
        return delta
    else:
      print("Error: function not recognized")
      sys.exit(1)


  def get_delta2(self, delta3):
    if self.error_function == Functions.MSE:
      if self.activation_function == Functions.SIGMOID:
        delta = np.dot(delta3, self.W2.T) * sigmoid_prime(self.z2)
        return delta
    else:
      print("Error: function not recognized")
      sys.exit(1)
