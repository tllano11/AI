import numpy as np
from enum import IntEnum, auto


class Functions(IntEnum):
  #Activation functions
  SIGMOID = auto()
  SOFTMAX = auto()
  #Error functions
  MSE = auto()

def sigmoid(z):
  """Apply sigmoid activation function

  Keyword arguments:
  z -- Matrix containing forwarded values
  """
  return 1/(1+np.exp(-z))

def sigmoid_prime(prediction):
  return prediction * (1-prediction)

def softmax(z):
  """Compute softmax values for z"""
  e_z = np.exp(z - np.max(z))
  return e_z / e_z.sum(axis=0)

def mse(expected_prediction, prediction):
  """Returns the Mean Squared Error of the net's output values

  Keyword arguments:
  expected_prediction -- Matrix containing the expected net's output values
  prediction -- Matrix containing the net's output values
  """
  return ((expected_prediction-prediction)**2)/2

def mse_prime(expected_prediction, prediction):
  return (prediction - expected_prediction)
