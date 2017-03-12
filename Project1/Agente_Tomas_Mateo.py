import copy
import sys
import random
import time
import eval_fun

DEPTH_LIMIT = 98
BOARD_SIZE = 121

def get_available_moves(game_state):
  children = []
  upper_limit = BOARD_SIZE-1
  for i in range(upper_limit):
      if ( game_state[i] == 0 ):
        children.append(i)    # Store position in which it's posible to make a move
  return children

def get_min_value(player, game_state, depth, alpha, beta):
    moves = get_available_moves(game_state)
    best_score = float('inf')
    if player == 1:
      chip = 1
      enemy = 2
    else:
      chip = 2
      enemy = 1
    if depth == DEPTH_LIMIT:
        moves = get_available_moves(game_state)
        return eval_fun.evaluate(player, game_state)
    for move in moves:
        following = copy.deepcopy(game_state)
        following[move] = chip
        score = get_max_value(enemy, following, depth+1, alpha, beta)
        if score < best_score:
            best_move = move
            best_score = score
        if best_score < beta and beta <= alpha:
          return best_score
        return best_score

def get_max_value(player, game_state, depth, alpha, beta):
    moves = get_available_moves(game_state)
    best_score = float('-inf')
    if player == 1:
      chip = 1
      enemy = 2
    else:
      chip = 2
      enemy = 1
    if depth == DEPTH_LIMIT:
        return eval_fun.evaluate(player, game_state)
    for move in moves:
        following = copy.deepcopy(game_state)
        following[move] = chip
        score = get_min_value(enemy, following, depth+1, alpha, beta)
        if score > best_score:
            best_move = move
            best_score = score
        if best_score > alpha and beta <= best_score:
          return best_score
        return best_score

def minimax(player, game_state, depth, alpha, beta):
  if player == 1:
    chip = 1
    enemy = 2
  else:
    chip = 2
    enemy = 1
  moves = get_available_moves(game_state)
  best_move = []
  best_score = float('-inf')
  for move in moves:
    following = copy.deepcopy(game_state)
    following[move] = chip
    score = get_min_value(enemy, following, depth+1, alpha, beta)
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
  player = 2
  start = time.time()
  result = minimax(player, board, 0, float('-inf'), float('inf'))
  end = time.time()
  print(result)
  print(end-start)

if __name__ == "__main__":
    main(sys.argv)