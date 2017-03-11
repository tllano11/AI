import copy
import random

# ALPHA -> Maximizer
# BETA -> Minimizer

PLAYER_1 = 1
BOARD_SIZE = 121
DEPTH_LIMIT = 3
'''
# Function to get the Player Number
def get_player(state, playerNumber):
  actualState = state
  player = playerNumber
  if player == PLAYER_1:
    #Do white Magic  (Up to Down)
  else:
    #Do black Magic  (Left to Right)
'''
# Function to get following nodes
def get_successors(board):
  successors = []
  upper_limit = BOARD_SIZE-1
  for i in range(0, upper_limit):
      if ( board[i] == 0 ):
        # Store position in which it's posible to make a move
        successors.append(i)
  return successors

def evaluate (board):
  return random.choice(range(11))

def minimax(board, depth, alpha, beta, turn):
  # Checks if at search bound
  if ( depth == DEPTH_LIMIT):
    return evaluate(board)
  # Checks if it has not already won
  if ( get_goal_state(board) == True ):
    return winning_state(board), board
  successors = get_successors(board)
  # Checks which player is playing: 1 -> Player 1, 2 -> Player 2
  if ( turn == 1 ):
    for i in successors:
      # Create successor state based on possible move
      next = copy.deepcopy(board)
      next[i] = 1
      min_value = minimax(next, depth+1, alpha, beta, 2)
      if ( alpha < min_value ):
        alpha = min_value
      # Checks if pruning can be done
      if ( beta < alpha ):
        return alpha, next
    return alpha, next
  else:
    for i in successors:
      next = copy.deepcopy(board)
      next[i] = 2
      max_value = minimax(next, depth+1, alpha, beta, 1)
      if ( beta > max_value ):
        beta = max_value
      # Checks if pruning can be done
      if ( alpha > beta ):
        return beta, next
    return beta, next
'''
# Function to get the value of Alpha
def get_alpha():
  

# Function to get the value of Beta  
def get_beta():
  

# Function to get the state of the winner
def get_goal_state(board):
  #LOST MAGIC STUFF
  
# Function to get the actual Winner
def winning_state(board):
  # DO SOMETHING *poke with a stick*

def main():
 '''