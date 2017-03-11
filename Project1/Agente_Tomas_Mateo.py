import copy
import sys
import random
import time

DEPTH_LIMIT = 100
BOARD_SIZE = 121

def evaluate (game_state):
  heuristic = random.randint(0, 500)
  return heuristic

def get_available_moves(game_state):
  children = []
  upper_limit = BOARD_SIZE-1
  for i in range(upper_limit):
      if ( game_state[i] == 0 ):
        # Store position in which it's posible to make a move
        children.append(i)
  return children

def get_min_value(game_state, depth, alpha, beta):
    if depth == DEPTH_LIMIT:
        return evaluate(game_state)
    moves = get_available_moves(game_state)
    best_score = float('inf')
    for move in moves:
        following = copy.deepcopy(game_state)
        following[move] = 2
        score = get_max_value(following, depth+1, alpha, beta)
        if score < best_score:
            best_move = move
            best_score = score
        if best_score < beta and beta <= alpha:
          return best_score
        return best_score

def get_max_value(game_state, depth, alpha, beta):
    if depth == DEPTH_LIMIT:
        return evaluate(game_state)
    moves = get_available_moves(game_state)
    best_score = float('-inf')
    for move in moves:
        following = copy.deepcopy(game_state)
        following[move] = 1
        score = get_min_value(following, depth+1, alpha, beta)
        if score > best_score:
            best_move = move
            best_score = score
        if best_score > alpha and beta <= best_score:
          return best_score
        return best_score

def minimax(game_state, depth, alpha, beta):
  moves = get_available_moves(game_state)
  best_move = []
  best_score = float('-inf')
  for move in moves:
    following = copy.deepcopy(game_state)
    following[move] = 1
    score = get_min_value(following, depth+1, alpha, beta)
    if score > best_score:
      best_move = following
      best_score = score
    if best_score > alpha and beta <= best_score:
      alpha = best_score
      return best_move
  return best_move

def main(argv):
  board = [0] * 121
  board[4] = 1

  start = time.time()
  result = minimax(board, 0, float('-inf'), float('inf'))
  end = time.time()
  print(result)
  print(end-start)

if __name__ == "__main__":
    main(sys.argv)