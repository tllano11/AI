import numpy as np
from enum import IntEnum, auto

class Functions(IntEnum):
  #Activation functions
  SIGMOID = auto()
  #Error functions
  MSE = auto()


def sigmoid(z):
  """ Apply sigmoid activation function

  Keyword arguments:
  z -- Matrix containing all activities of a layer
  """
  return 1/(1+np.exp(-z))


def sigmoid_prime(z):
  return np.exp(-z)/((1+np.exp(-z))**2)


def mse(expected_prediction, prediction):
  pass


def mse_prime(expected_prediction, prediction):
  return (prediction - expected_prediction)
