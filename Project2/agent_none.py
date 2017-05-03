# -*- coding: utf-8 -*-

from operator import itemgetter
import random
import numpy

BOARD_SIZE = 25

SHOOT = 1
MEASURE = 2
MOVE = 3

GREEN = "verde"
YELLOW = "amarillo"
ORANGE = "anaranjado"
RED = "rojo"

class Node:
  
  def __init__(self, id, value):
    self.id = id
    self.adjacents = self.__get_adjacents_from_id(id)
    self.value = value
    self.prob_trans = int(1/len(self.adjacents))
  
  def __get_adjacents_from_id(self, position):
    if position == 0 or position == 5 or 10 or position == 15 or position == 20:
      return [position + 5, position + 1]
    elif position == 4 or position == 9 or position == 14 or position == 19 or position == 24:
      return [position + 5, position - 1]
    elif position == 1	or position == 2 or position == 3:
      return [position + 5, position - 1, position + 1]
    elif position == 21 or position == 22 or position == 23:
      return [position - 5, position - 1, position + 1]
    else:
      return [position - 5, position + 5, position - 1, position + 1]
  
  def update_value(self, prob):
    #TODO: Define how to update probabilities based on measurements.
    accum = 0
    for adj in adjacents:
      accum += adj.prob_trans * adj.value
    self.value = accum

class AgentNone:

  def __init__(self):
    self.player = None
    self.init_pos = None
    self.hmm = self.__get_hmm(BOARD_SIZE)
    self.probabilities = [random.random()]*25
  
  def __get_hmm(self, n_cells):
    hmm = [None] * 25
    for i in range(0, n_cells):
      hmm[i] = Node(i, numpy.random.rand())
    return hmm
  
  def run_agent_none(self, current_player, result_enemy_action, enemy_action, init_pos):
    if self.player is None:
      self.player = current_player
    if self.init_pos is None:
      self.init_pos = init_pos
    
    if enemy_action == SHOOT:
      pass
    elif enemy_action == MEASURE:
      if color == GREEN or color == YELLOW:
        move(init_pos, val_measure)        #value of measure
    elif enemy_action == MOVE:
      pass
 
  def desition(self, enemy_action, result_enemy_action):
    if enemy_action == MEASURE:
      if result_enemy_action == GREEN or result_enemy_action == YELLOW:
        move()
    else:
        scan()
  
  def __get_emv(self, R, p, n_actions, n_cells):
    ep = []
    for i in range(0, n_actions):
      accum = 0
      for j in range(0, n_cells):
        accum += R[i][j] * p[j]
      ep.append(accum)
    return max(ep)
  
  def __get_ev_pi(self, R, p, n_actions, n_cells):
    accum = 0
    maxim = 0
    action = 0
    for j in range(0, n_cells):
      for i in range(0, n_actions):
        if R[i][j] > maxim:
          maxim = R[i][j]
      accum += maxim * p[j]
    return accum
  
  def get_evpi(self, R, p, n_actions, n_cells):
    emv = self.__get_emv(R, p, n_actions, n_cells)
    print("EMV:", emv)
    ev_pi = self.__get_ev_pi(R, p, n_actions, n_cells)
    print("EV|PI:", ev_pi)
    evpi = ev_pi - emv
    return evpi
  
  def move(self, position, val_measure):
    """Determines which movement to do, based on the measure made by the enemy
    current_position = position - 5     #Move Up
    current_position = position + 5     #Move Down
    current_position = position - 1     #Move Left
    current_position = position + 1     #Move Right
    """
    #Comprueba la posicion de Sensado y se mueve a esa posicion
    if val_measure - 1 == current_position or val_measure + 1 == current_position or val_measure - 5 == current_position or val_measure + 5 == current_position:
      current_position = val_measure
    else: #Comprueba esquinas y bordes del tablero y se mueve random en los espacios posibles
      if position == 0 or position == 5 or 10 or position == 15 or position == 20:
        current_position = position + int(random.choice(["5","1"]))
      elif position == 4 or position == 9 or position == 14 or position == 19 or position == 24:
        current_position = position - int(random.choice(["-5","1"]))
      elif position == 1	or position == 2 or position == 3:
        current_position = position - int(random.choice(["-5","-1","1"]))
      elif position == 21 or position == 22 or position == 23:
        current_position = position - int(random.choice(["5","-1","1"]))
      else:
        current_position = position - int(random.choice(["-5","5","-1","1"]))
    
    """if val_measure - 1 == current_position or val_measure + 1 == current_position or val_measure - 5 == current_position or val_measure + 5 == current_position or val_measure == current_position:
      if position == 0 or position == 5 or 10 or position == 15 or position == 20:
        current_position = position + 5
        current_position = position + 1
      elif position == 4 or position == 9 or position == 14 or position == 19 or position == 24:
        current_position = position + 5
        current_position = position - 1
      elif position == 1	or position == 2 or position == 3:
        current_position = position + 5
        current_position = position - 1
        current_position = position + 1
      elif position == 21 or position == 22 or position == 23:
        current_position = position - 5
        current_position = position - 1
        current_position = position + 1
      else:
        current_position = position - 5
        current_position = position + 5
        current_position = position - 1
        current_position = position + 1"""
    return current_position
  
  def shoot(self):
    #DIE
    pass
    
  def scan(self):
    #GOT YOU
    pass
  
def main():
  p = numpy.random.rand(25)
  R = numpy.random.rand(3, 25)
  
  print("p: ", p)
  print("R: ", R)
  a = AgentNone()
  print(a.get_evpi(R.tolist(), p.tolist(), 3, 25))
  
if __name__ == "__main__":
  main()