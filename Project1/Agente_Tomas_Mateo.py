import copy
from eval_fun import evaluate
import sys

DEPTH_LIMIT = 3
BOARD_SIZE = 121

'''
  Determines which positions are free to make a move and
  returns a list containing them.
'''
def get_available_moves(game_state):
  children = []
  upper_limit = BOARD_SIZE-1
  for i in range(upper_limit):
      if ( game_state[i] == 0 ):
        children.append(i)    # Store position in which it's posible to make a move
  return children

'''
  Obtains the min value from the max values.
'''
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
        return evaluate(player, game_state)
    for move in moves:
        following = copy.deepcopy(game_state)
        following[move] = chip
        score = get_max_value(enemy, following, depth+1, alpha, beta)
        if score is None:
          score = float('inf')
        if score < best_score:
            best_move = move
            best_score = score
        if best_score < beta and beta <= alpha:
          return best_score
        return best_score

'''
  Obtains the max value from the min values.
'''
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
        return evaluate(player, game_state)
    for move in moves:
        following = copy.deepcopy(game_state)
        following[move] = chip
        score = get_min_value(enemy, following, depth+1, alpha, beta)
        if score is None:
          score = float('-inf')
        if score > best_score:
            best_move = move
            best_score = score
        if best_score > alpha and beta <= best_score:
          return best_score
        return best_score

'''
  Obtains the minimax value from a given game state and
  returns the best possible move to make.
  Note that the "get_max_value" function is called after
  iterating according to the "get_min_value" function's
  structure (i.e. a get_min_value like iteration was made
  before calling get_max_value). It's done that way due to
  our evaluation function return value (Dijkstra's algoritm
  finds a minimum length path, not a maximum one).
'''
def minimax(player, game_state, depth, alpha, beta):
  if player == 1:
    chip = 1
    enemy = 2
  else:
    chip = 2
    enemy = 1
  moves = get_available_moves(game_state)
  best_move = []
  best_score = float('inf')
  for move in moves:
    following = copy.deepcopy(game_state)
    following[move] = chip
    score = get_max_value(enemy, following, depth+1, alpha, beta)
    if score is None:
      continue
    if score < best_score:
      best_move = move
      best_score = score
    if best_score < beta and beta <= best_score:
      beta = best_score
      return best_move
  return best_move

'''
  Obtains the values of the rows in order to return an answer to jupyter
'''
def get_row(it):
  if it in range(0, 11):
    return 0
  elif it in range(11, 22):
    return 1
  elif it in range(22, 33):
    return 2
  elif it in range(33, 44):
    return 3
  elif it in range(44, 55):
    return 4
  elif it in range(55, 66):
    return 5
  elif it in range(66, 77):
    return 6
  elif it in range(77, 88):
    return 7
  elif it in range(88, 99):
    return 8
  elif it in range(99,110):
    return 9
  else:
    return 10

'''
  Obtains the values of the columns in order to return an answer to jupyter
'''
def get_column(it, row):
  if row == 0:
    return it
  if row == 1:
    return it - 11
  if row == 2:
    return it - 22
  if row == 3:
    return it - 33
  if row == 4:
    return it - 44
  if row == 5:
    return it - 55
  if row == 6:
    return it - 66
  if row == 7:
    return it - 77
  if row == 8:
    return it - 88
  if row == 9:
    return it - 99
  if row == 10:
    return it - 110

'''
  A pseudo "main"-like function called when it is desired to
  to get the best possible move by using the minimax algorithm.
'''
def Agente_Tomas_Mateo(player, game_state):
  game_state = [item for sublist in game_state for item in sublist]
  result =  minimax(player, game_state, 0, float('-inf'), float('inf'))
  if result == []:
    for i in range(len(game_state)):
      if game_state[i] == 0:
          row = get_row(i)
          column = get_column(i, row)
          position = [row, column]
          return position

  row = get_row(result)
  column = get_column(result, row)
  position = [row, column]
  return position
