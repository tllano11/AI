import numpy as np
import copy

# ALPHA -> Maximizer
# BETA -> Minimizer

PLAYER_1 = 1
BOARD_SIZE = 121

# Function to get the Player Number
def get_player(state, playerNumber):
  actualState = state
  player = playerNumber
  if player == PLAYER_1:
    #Do white Magic  (Up to Down)
  else:
    #Do black Magic  (Left to Right)

# Function to get following nodes
def get_successors(board):
  successors = []
  upper_limit = BOARD_SIZE-1
  for i in range(0, upper_limit):
      if ( board[i] == 0 ):
        # Store position in which it's posible to make a move
        successors.append(i)
  return successors

# Function to get the max value for the minmax algorithm
def get_max_value(board, alpha, beta):
  if ( get_goal_state(board) == True ):
    return winning_state(board), board
  successors = get_successors(board)
  new_board = []
  for i in successors:
    # Create successor state based on possible move
    next = copy.deepcopy(board)
    next[i] = 1
    value = get_min_value(next)
    # Checks if pruning can be done
    if ( beta < value ):
      break
    if ( alpha < value ):
      alpha = value
      new_board = i
  return new_board, alpha

# Function to get the min value for the minmax algorithm
def get_min_value(board, alpha, beta):
  if ( get_goal_state(board) == True ):
    return winning_state(board), board
  successors = get_successors(board)
  new_board = []
  for i in successors:
      next = copy.deepcopy(board)
      next[i] = -1
      value = get_max_value(next)
      if ( alpha > value ):
        break
      if ( beta > value ):
        beta = value
        new_board = i
      return new_board, beta

# Function to get the value of Alpha
def get_alpha():
  
  
# AlphaBetaSearch performs the alpha beta pruning
# on min max algorithm and return the best position
def alpha_beta_search(board):
    #print board
    val, c = alpha_beta_max_value(board, -10, 10)
    return val, c

#The Alpha Beta Max Value
def alpha_beta_max_value(board, alpha, beta):

    if(goal_condition(board) == True):
        return Utility(board), board

    v = -10
   
    a = Successors(board, 'O')
    newboard = []
    
    for i in a:
        val, c = alpha_beta_min_value(i, alpha, beta)
        

        v = max( v, val)
        
        if( v > beta ):
            return v, board
        alpha = max( alpha, v )
        newboard = i
    return v, newboard

#The Alpha Beta Min Value
def alpha_beta_min_value(board,alpha,beta):
    if(goal_condition(board) == True):
        return Utility(board), board
    v = 10
    a = Successors(board, 'X')
    newboard = []
    for j in a:
        val, c = alpha_beta_max_value(j,alpha,beta)
        v = min( v, val)
        if(v < alpha):
            return v, board
        beta = min( beta, v )
        newboard = j
    return v, newboard
  
  
# Function to get the value of Beta  
def get_beta():
  

# Function to get the state of the winner
def get_goal_state(board):
  #LOST MAGIC STUFF
  
# Function to get the actual Winner
def winning_state(board):
  # DO SOMETHING

def main():
  