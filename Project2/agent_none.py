from operator import itemgetter
import random
import numpy as np
from hmm import HMM

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
    """Returns adjacent positions from a given position.
    
    Keyword arguments:
    position -- Position from which to find adjacent positions.
    """
    if position == 1:                                        #Upper-left corner.
      return [position + 5, position + 1]
    elif position == 5:                                      #Upper-right corner.
      return [position + 5, position - 1]
    elif position == 21:                                     #Lower-left corner.
      return [position - 5, position + 1]
    elif position == 25:                                     #Lower-right corner.
      return [position - 5, position - 1]
    elif position == 2 or position == 3 or position == 4:    #Upper wall.
      return [position + 5, position - 1, position + 1]
    elif position == 10 or position == 15 or position == 20: #Right wall.
      return [position + 5, position - 5, position - 1]
    elif position == 6 or position == 11 or position == 16:  #Left wall.
      return [position + 5, position - 5, position + 1]
    elif position == 22 or position == 23 or position == 24: #Bottom wall.
      return [position - 5, position - 1, position + 1]
    else:                                                    #All other positions.
      return [position - 5, position + 5, position - 1, position + 1]


class AgentNone:
 
  def __init__(self):
    self.player = None
    self.current_pos = None
    self.last_measured_pos = None
    self.ct = self.__get_color_table()
    self.net = self.__get_net(BOARD_SIZE)
    self.enemy_net = self.__get_net(BOARD_SIZE)
  
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
      net.append(Node(i+1))
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
    
  def update_probs(self, measure, p, enemy_net = False):
    """Updates board probabilities regarding where the enemy might be.
    
    Keyword arguments:
    measure -- Color obtained from measure: green, yellow, orange, red
    p -- The position where the measure was made
    enemy_net -- If true, then all updates will be done to the enemy's net.
    """
    tmp_net = []
    net_size = len(self.net) 
    if not enemy_net:
      net = self.net
    else:
      net = self.enemy_net
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
        tmp_net.append(net[j].value * self.ct[0][color])
      elif distance == 1: #When updating an adjacent position to the one measured.
        tmp_net.append(net[j].value * self.ct[1][color])
      elif distance == 2: #When updating a position at two cells from the one measured.
        tmp_net.append(net[j].value * self.ct[2][color])
      elif distance == 3: #When updating a position at three cells from the one measured.
        tmp_net.append(net[j].value * self.ct[3][color])
      else: #When updating a position at four or more cells from the one measured.
        tmp_net.append(net[j].value * self.ct[4][color])
    #Obtains summation of new probabilities in order to execute 
    #a posterior normalization.
    total = sum(tmp_net)
    #Normalizes new probabilities and assigns them to its 
    #corresponding position.
    for i in range(0, net_size):
      net[i].value = tmp_net[i]/total
  
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
    return self.net[np.argmax(green_probs)].id

  def determine_move_position(self):
    """Returns the best position to move.
    In order to achieve it, the function calculates
    the Manhattan distance between all positions and
    each position being analyzed (adjacents), performing 
    inference by applying the belief propagation algorithm. It
    mainly aims to minimize the enemy's probability of measure
    green at a time t+1.
    """
    green_probs = []
    net_size = len(self.net)
    adjacents = self.net[self.current_pos].adjacents
    #Belief propagation:
    #Analyzes each position's probability of obtaining
    #green when measuring at a time t+1.
    for i in adjacents:
      accum = 0
      for j in range(0, net_size):
        distance = self.__get_distance(i-1, j)
        if distance == 0: #Probability of measure green at distance 0 from 'i'.
          accum += self.enemy_net[i-1].value * self.ct[0][0]
        elif distance == 1: #Probability of measure green at distance 1 from 'i'.
          accum += self.enemy_net[i-1].value * self.ct[1][0]
        elif distance == 2: #Probability of measure green at distance 2 from 'i'.
          accum += self.enemy_net[i-1].value * self.ct[2][0]
        elif distance == 3: #Probability of measure green at distance 3 from 'i'.
          accum += self.enemy_net[i-1].value * self.ct[3][0]
        else: #Probability of measure green at a distance >= 4 from 'i'.
          accum += self.enemy_net[i-1].value * self.ct[4][0]
      green_probs.append((i, accum))
    #Returns the position in which the probability of
    #obtaining green when measuring is the lowest.
    return min(green_probs, key=itemgetter(1))[0]
  
  def __get_net_probs(self):
    """Returns a matrix containing all probabilities from each node 
    inside the net.
    """
    return np.array([node.value for node in self.net]).reshape(5,5)
  
  def run_agent_none(self, current_player, our_result, enemy_action, init_pos):
    """Returns a list comprising an action, Move, Measure or shoot,
    and its corresponding parameters.
    
    Keyword arguments:
    current_player -- Which player is the agent playing as (1 or 2)
    our_result -- The result of the agent's last action
    enemy_action -- The result of the agent's enemy last action
    init_pos -- Position where the agent starts playing.
    """

    if enemy_action[1] is not None:
      enemy_action[1] -= 1
    
    if self.player is None:
      self.player = current_player

    self.current_pos = init_pos - 1
    #If player 1 is playing for the first time, then there is no
    #information to rely on for taking an action different than
    #measure.
    if self.last_measured_pos is None and self.player == 1:
      pos_measure = self.determine_measure_position()
      return self.measure(pos_measure)

    #Obtains an action based on the result of the last one.
    action_based_on_us = self.desition_based_on_us(our_result)
    #Obtains an action based on the result of the enemy's last action
    action_based_on_enemy = self.desition_based_on_enemy(enemy_action)
    #If the enemy's last action represents a threat for the agent,
    #then it plays defensively by moving to another position rather
    #than measure or shoot.
    if action_based_on_enemy[0] == MOVE:
      return action_based_on_enemy
    #If the enemy's last action does not represent a threat, 
    #then the agent measures or shoots.
    else:
      return action_based_on_us
    
  def __get_best_pos_to_shoot(self):
    """Returns a position in which is more likely to shoot the enemy.
    """
    #Gets the state of the markov model at time t.
    transition_probabilities = self.__get_net_probs()
    emission_probabilities = self.__get_net_probs()
    hmm = HMM(transition_probabilities, emission_probabilities)
    emissions = [2, 1, 0]
    initial = self.__get_net_probs()
    return(self.net[self.viterbi(hmm, initial, emissions)[0]].id)

  def desition_based_on_us(self, action_result):
    """Returns an action and its parameters based on the results
    obtained on a previous turn.
    
    Keyword parameters:
    action_result -- Either a string, which reprents the measured color
    at time t-2, an integer, which can be 1 if the agent shot its enemy
    or 0 if it missed, or None, if move was the agent's last action.
    """
    if isinstance(action_result, int) or action_result is None:
      pos_to_measure = self.determine_measure_position()
      return self.measure(pos_to_measure)
    #If the agent's last action was to measure, then shooting
    #should be considered only if green or yellow were the
    #result.
    elif isinstance(action_result, str):
      self.update_probs(action_result, self.last_measured_pos)
      #It is unlikely for the enemy to stay on a position if
      #it is being targeted. Based on that assumption, the
      #agent supposes measuring at the same position will
      #result on obtaining yellow.
      if action_result == GREEN:
        self.update_probs(YELLOW, self.last_measured_pos)
        pos_to_shoot = self.__get_best_pos_to_shoot()
        return self.shoot(pos_to_shoot)
      elif action_result == YELLOW:
        pos_to_shoot = self.__get_best_pos_to_shoot()
        return self.shoot(pos_to_shoot)
  
    pos_to_measure = self.determine_measure_position()
    return self.measure(pos_to_measure)

  def desition_based_on_enemy(self, enemy_action):
    """Returns an action and its parameters based on the results
    obtained on a the enemy's last action.
    
    Keyword arguments:
    enemy_action -- An array comprised of three values:
    The enemy's last action (move, measure or shoot), its
    parameters and the corresponding results. 
    """
    #If it is the first turn for player one, then 
    #enemy_action will be None.
    if enemy_action[0] is not None:
      #If the enemy measured a position, then it is in the agent's
      #best interest to track what information does they posses.
      if enemy_action[0] == MEASURE:
        self.update_probs(enemy_action[2], enemy_action[1], True)
        if enemy_action[2] == GREEN or enemy_action[2] == YELLOW:
          pos_to_move = self.determine_move_position()
          return self.move(pos_to_move)
      elif enemy_action[0] == SHOOT:
        if self.__get_distance(self.current_pos, enemy_action[1]) < 2:
          pos_to_move = self.determine_move_position()
          return self.move(pos_to_move)

    pos_to_measure = self.determine_measure_position()
    return self.measure(pos_to_measure)
  
  def viterbi(self, hmm, initial, emissions):
    """Returns the best position to shoot.
    In order to achieve it, the function uses HMM (Hidden Markov Models)
    to get the best options and choose from the list the one that suits
    our game in the best way possible, the Markov Model is located in the
    same directory inside hmm.py file
    """
    probabilities = hmm.emission(emissions[0]) * initial
    stack = []
    
    for emission in emissions[5:]:
        trans_probabilities = hmm.transition_probabilities * np.row_stack(probabilities)                        #Matrix for transition probabilities
        max_col_ixs = np.argmax(trans_probabilities, axis=0)
        probabilities = hmm.emission(emission) * trans_probabilities[max_col_ixs, np.arange(hmm.num_states)]    #Probabilities
        stack.append(max_col_ixs)                                                                               #Store the axis and the data in the stack
    state_seq = [np.argmax(probabilities)]                                                                      #Store the resulted probabilities

    while stack:
        max_col_ixs = stack.pop()                                                                               #Take out the top data store in stack
        state_seq.append(max_col_ixs[state_seq[-1]])
    state_seq.reverse()
    return state_seq
  
  def move(self, pos_to_move): 
    """Returns a list with the "move" action and its parameters.
    
    Key arguments:
    pos_to_move -- Position in which to move next.
    """
    if (self.current_pos + 1) - pos_to_move == 1:     #Move to the left
      direction = 4
    elif (self.current_pos + 1) - pos_to_move == -1:  #Move to the right
      direction = 2
    elif (self.current_pos + 1) - pos_to_move == 5:   #Move to the top
      direction = 1
    else:                                             #Move to the bottom
      direction = 3
    return [MOVE, direction]
  
  def shoot(self, pos_to_shoot):
    """Returns a list with the "shoot" action and its parameters.
    
    Key arguments:
    pos_to_shoot -- Position in which to shoot next.
    """
    return [SHOOT, pos_to_shoot]
    
  def measure(self, pos_to_measure):
    """Returns a list with the "measure" action and its parameters.
    
    Key arguments:
    pos_to_measure -- Position in which to measure next.
    """
    self.last_measured_pos = pos_to_measure - 1
    return [MEASURE, pos_to_measure]