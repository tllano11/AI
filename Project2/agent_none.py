from operator import itemgetter
import random
import numpy as np
#from hmm import HMM

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


class AgentNone:

  def viterbi(hmm, initial, emissions):
    
    """transition_probabilities = np.array([[0.7, 0.4], [0.3, 0.6]])
        emissions = [2, 1, 0]
        emission_probabilities = np.array([[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]])
        initial = np.array([[0.6, 0.4]])
        hmm = HMM(transition_probabilities, emission_probabilities)
        print(viterbi(hmm, initial, emissions))
    """
    
    probabilities = hmm.emission(emissions[0]) * initial
    stack = []

    for emission in emissions[1:]:
        trans_probabilities = hmm.transition_probabilities * np.row_stack(probabilities)
        max_col_ixs = np.argmax(trans_probabilities, axis=0)
        probabilities = hmm.emission(emission) * trans_probabilities[max_col_ixs, np.arange(hmm.num_states)]

        stack.append(max_col_ixs)

    state_seq = [np.argmax(probabilities)]

    while stack:
        max_col_ixs = stack.pop()
        state_seq.append(max_col_ixs[state_seq[-1]])

    state_seq.reverse()

    return state_seq
  
  def __init__(self):
    self.player = None
    self.init_pos = None
    self.ct = self.__get_color_table()
    #self.net = self.__get_net(BOARD_SIZE)
    self.net = self.__get_net(25)
    self.probabilities = [random.random()]*25
    #self.__set_initial_probs()
  
  def __get_color_table(self):
    """Returns the probabilities for obtaining an specific
    color, green, yellow, orange or red, when measuring
    given a Manhattan distance of 0, 2, 3, 4 or more.
    """
    #Color:  Green    Yellow  Orange  Red     Distance:
    return [[0.70,    0.15,   0.1,    0.05],  # 0
            [0.17,    0.6,    0.17,   0.06],  # 1
            [0.06,    0.17,   0.6,    0.17],  # 2
            [0.05,    0.12,   0.23,   0.6],   # 3
            [0.05,    0.1,    0.15,   0.8]]   # >= 4 
    
  def __get_net(self, nodes):
    """Returns an array of Node objects.Returns.
    
    Keyword arguments:
    nodes -- Number of nodes to be created.
    """
    net = []
    #Creates a net and sets each node's probability,
    #for the enemy being there, to 1/25 due to the lack
    #of information regarding their position.
    for i in range(0, nodes):
      net.append(Node(i))
      net[i].value = 1/25
    return net
  
  def __get_distance(self, i, j):
    """Returns the Manhattan distance between two positions.
    
    Keyword arguments:
    i -- Position to be compared with j
    j -- Position to be compared with i
    """
    row_i = i // 5
    column_i = i % 5
    row_j = j // 5
    column_j = j % 5
    distance = abs(row_i-row_j) + abs(column_i-column_j)
    return distance
    
  def update_probs(self, measure, p):
    """Updates board probabilities regarding where the enemy might be.
    
    Keyword arguments:
    measure -- Color obtained from measure: green, yellow, orange, red
    p -- The position where the measure was made
    """
    tmp_net = []
    net_size = len(self.net)
    #Maps a given color to its corresponding column in the color's 
    #probability table.
    if measure == GREEN:
      color = 0
    elif measure == YELLOW:
      color = 1
    elif measure == ORANGE:
      color = 2
    elif measure == RED:
      color = 3
    #Obtains new probabilities by using the distance between the
    #observed position (the one measured) and any other position.
    for j in range(0, net_size):
      distance = self.__get_distance(p, j)
      if distance == 0: #When updating the measured position's probability.
        tmp_net.append(self.net[j].value * self.ct[0][color])
      elif distance == 1: #When updating an adjacent position to the one measured.
        tmp_net.append(self.net[j].value * self.ct[1][color])
      elif distance == 2: #When updating a position at two cells from the one measured.
        tmp_net.append(self.net[j].value * self.ct[2][color])
      elif distance == 3: #When updating a position at three cells from the one measured.
        tmp_net.append(self.net[j].value * self.ct[3][color])
      else: #When updating a position at four or more cells from the one measured.
        tmp_net.append(self.net[j].value * self.ct[4][color])
    #Obtains summation of new probabilities in order to execute 
    #a posterior normalization.
    total = sum(tmp_net)
    #Normalizes new probabilities and assigns them to its 
    #corresponding position.
    for i in range(0, net_size):
      self.net[i].value = tmp_net[i]/total
  
  def determine_measure_position(self):
    """Returns the best position to measure.
    In order to achieve it, the function calculates
    the Manhattan distance between all positions and
    each position being analyzed, performing inference
    by applying the belief propagation algorithm. It
    mainly aims to maximize the probability of measure
    green at a time t+1.
    """
    green_probs = []
    net_size = len(self.net)
    #Belief propagation:
    #Analyzes each position's probability of obtaining
    #green when measuring at a time t+1.
    for i in range(0, net_size):
      accum = 0
      for j in range(0, net_size):
        distance = self.__get_distance(i, j)
        if distance == 0: #Probability of measure green at distance 0 from 'i'.
          accum += self.net[i].value * self.ct[0][0]
        elif distance == 1: #Probability of measure green at distance 1 from 'i'.
          accum += self.net[i].value * self.ct[1][0]
        elif distance == 2: #Probability of measure green at distance 2 from 'i'.
          accum += self.net[i].value * self.ct[2][0]
        elif distance == 3: #Probability of measure green at distance 3 from 'i'.
          accum += self.net[i].value * self.ct[3][0]
        else: #Probability of measure green at a distance >= 4 from 'i'.
          accum += self.net[i].value * self.ct[4][0]
      green_probs.append(accum)
    #Returns the position in which the probability of
    #obtaining green when measuring is the highest.
    return np.argmax(green_probs)
  
  def __set_initial_probs(self):
    tmp_net = []
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
      tmp_net.append((prob_dist_0*self.ct[0][0] + prob_dist_1*self.ct[1][0] + prob_dist_2*self.ct[2][0] + prob_dist_3*self.ct[3][0] + prob_dist_4*self.ct[4][0])/25)
    
    total = sum(tmp_net)
    for i in range(0, len(self.net)):
      self.net[i].value = tmp_net[i]/total
  
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
  print("ANTES: ",[x.value for x in a.net], "\n")
  print("Measure position: ", a.determine_measure_position())
  a.update_probs("amarillo", 19)
  print("DESPUES: ",[x.value for x in a.net])
  print("Measure position: ", a.determine_measure_position())
  
if __name__ == "__main__":
  main()