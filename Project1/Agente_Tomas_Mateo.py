import copy
import eval_fun

DEPTH_LIMIT = 98
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
    if score < best_score:
      best_move = following
      best_score = score
    if best_score < beta and beta <= best_score:
      beta = best_score
      return best_move
  return best_move

'''
  A pseudo "main"-like function called when it is desired to 
  to get the best possible move by using the minimax algorithm.
'''
def main(player, game_state):
  game_state = [item for sublist in game_state for item in game_state]
  result =  minimax(player, board, 0, float('-inf'), float('inf'))
  tmp = []
  result_matrix = []
  for i in range(0, 121):
    tmp.append(result[i])     # Append to make the temporal list that will be added to the final matrix as a result
    if (i%11)-1 == 9:
      result_matrix.append(tmp)   # Append to the temp list to give us a result
      tmp = []                    # tmp gets empty to start over
  return result_matrix