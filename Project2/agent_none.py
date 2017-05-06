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
  
  def __init__(self, id):
    self.id = id
    self.adjacents = self.__get_adjacents_from_id(id)
    self.prob_trans = 1/len(self.adjacents)
    self.value = None
    
  def __get_adjacents_from_id(self, position):    
    if position == 0:
      return [position + 5, position + 1]
    elif position == 4:
      return [position + 5, position - 1]
    elif position == 20:
      return [position - 5, position + 1]
    elif position == 24:
      return [position - 5, position - 1]
    elif position == 1 or position == 2 or position == 3:
      return [position + 5, position - 1, position + 1]
    elif position == 9 or position == 14 or position == 19:
      return [position + 5, position - 5, position - 1]
    elif position == 5 or position == 10 or position == 15:
      return [position + 5, position - 5, position + 1]
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
    self.ct = self.__get_color_table()
    self.net = self.__get_net(BOARD_SIZE)
    self.probabilities = [random.random()]*25
    self.__set_initial_probs()
    
  def __get_color_table(self):
    return [[0.70, 0.15, 0.1, 0.05],
            [0.17, 0.6, 0.17, 0.06],
            [0.06, 0.17, 0.6, 0.17],
            [0.05, 0.12, 0.23, 0.6],
            [0.05, 0.1, 0.15, 0.8]]
    
  def __get_net(self, nodes):
    net = []
    for i in range(0, nodes):
      net.append(Node(i))
    return net
    
  def update_probs(self, measure, net, ct):
    if measure == GREEN:
      color = 0
    elif measure == YELLOW:
      color = 1
    elif measure == ORANGE:
      color = 3
    elif measure == RED:
      color = 4
    for i in range(0, len(net)):
      accum = 0
      for j in range(0, len(net)):
        tmp = abs(i-j)
        if j==i:
          accum += net[j].value * self.ct[0][color]
        elif tmp == 1 or tmp == 5:
          accum += net[j].value * self.ct[1][color]
        elif tmp == 2 or tmp == 10:
          accum += net[j].value * self.ct[2][color]
        elif tmp == 3 or tmp == 15:
          accum += net[j].value * self.ct[3][color]
        else:
          accum += net[j].value * self.ct[4][color]
      net[i].value = accum
      
  def __set_initial_probs(self):
    for i in range(0, len(self.net)):
      prob_dist_0 = 1
      prob_dist_1 = len(self.net[i].adjacents)
      if prob_dist_1 == 4:
        if i == 12:
          prob_dist_2 = 8
          prob_dist_3 = 8  
        else:
          prob_dist_2 = 7
          prob_dist_3 = 7
      elif prob_dist_1 == 3:
        if i == 10 or i == 14 or i == 2 or i == 22:
          prob_dist_2 = 5
        else:
          prob_dist_2 = 4
        prob_dist_3 = 5
      else:
        prob_dist_2 = 3
        prob_dist_3 = 4
      prob_dist_4 = 25 - (prob_dist_0 + prob_dist_1 + prob_dist_2 + prob_dist_3)
      self.net[i].value = (prob_dist_0*self.ct[0][0] + prob_dist_1*self.ct[1][0] + prob_dist_2*self.ct[2][0] + prob_dist_3*self.ct[3][0] + prob_dist_4*self.ct[4][0])/25
  
  def run_agent_none(self, current_player, result_enemy_action, enemy_action, init_pos):
    if self.player is None:
      self.player = current_player
    if self.init_pos is None:
      self.current_pos = init_pos
    
    if enemy_action == SHOOT:
      pass
    elif enemy_action == MEASURE:
      if color == GREEN or color == YELLOW:
        move(net[current_pos], val_measure)
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
  
  def move(self, state, val_measure):
    possible_moves = state.adjacents
    current_position = random.choice(possible_moves)    
  
  def shoot(self):
    #DIE
    pass
    
  def scan(self):
    #GOT YOU
    pass
  
def main():
  a = AgentNone()
  print("ANTES: ",[x.value for x in a.net])
  a.update_probs("amarillo", a.net, a.ct)
  print("DESPUES: ",[x.value for x in a.net])
  
if __name__ == "__main__":
  main()