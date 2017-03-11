import copy
import random
import sys
import time

# ALPHA -> Maximizer
# BETA -> Minimizer

PLAYER_1 = 1
BOARD_SIZE = 121
DEPTH_LIMIT = 3
BOARD = []

# Function to get following nodes
def get_successors(board):
  successors = []
  upper_limit = BOARD_SIZE-1
  for i in range(upper_limit):
      if ( board[i] == 0 ):
        # Store position in which it's posible to make a move
        successors.append(i)
  return successors

def get_goal_state(board):
  return False

def evaluate (board):
  heuristic = random.randrange(1, 500)
  return heuristic

def minimax(board, depth, alpha, beta, turn):
  global BOARD
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
      result = minimax(next, depth+1, alpha, beta, 2)
      if ( result > alpha ):
        alpha = result
        BOARD = board
      # Checks if pruning can be done
      if ( alpha >= beta ):
        return alpha
    return alpha
  else:
    for i in successors:
      next = copy.deepcopy(board)
      next[i] = 2
      result = minimax(next, depth+1, alpha, beta, 1)
      if ( result < beta):
        beta = result
        BOARD = board
      # Checks if pruning can be done
      if ( beta <= alpha ):
        return beta
    return beta

def main(argv):
  board = [0] * 121
  board[4] = 1
  start = time.time()
  result = minimax(board, 0, -2000, 2000, 1)
  end = time.time()
  print(BOARD)
  print(result)
  print(end-start)

if __name__ == "__main__":
    main(sys.argv)