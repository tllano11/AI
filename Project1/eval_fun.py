import heapq
import sys
import time

def dijkstra(player, adjacent, costs, start, end):
    prior_queue = []
    min_dist = {start: 0}
    distance_queue = {}
    predecessor = {}
    visited_set = set([start])
    step_count = 1
    
    for i in adjacent.get(start, []):
        min_dist[i] = costs[start, i]
        item = [min_dist[i], start, i]
        heapq.heappush(prior_queue, item)
        distance_queue[i] = item
    
    while prior_queue:
        cost, parent, left = heapq.heappop(prior_queue)
        if (step_count >= 10) and is_terminal_node(player, left):
          end = left
          
        if left not in visited_set:
            predecessor[left] = parent
            visited_set.add(left)
            if left == end:
                return predecessor, min_dist[left]
            for i in adjacent.get(left, []):
                if min_dist.get(i):
                    if min_dist[i] > costs[left, i] + min_dist[left]:
                        min_dist[i] =  costs[left, i] + min_dist[left]
                        distance_queue[i][0] = min_dist[i]
                        distance_queue[i][1] = left
                        heapq._siftdown(prior_queue, 0, prior_queue.index(distance_queue[i]))
                else:
                    min_dist[i] = costs[left, i] + min_dist[left]
                    item = [min_dist[i], left, i]
                    heapq.heappush(prior_queue, item)
                    distance_queue[i] = item
        step_count = step_count + 1
    return None
  
    '''
      Determines whether Dijkstra's algorithm has reached its goal, 
      which is variant, or must keep searching. 
      Example:
        * left = 10; then the expression ((left%11)-1) == 9 will result in a true
        statement, which means we have reached the right position and Dijkstra's
        new goal.
    '''
def is_terminal_node(player, left):
  if player == 1:                    # Checks if left is one of the board's bottom positions
    return left in range(110, 121)
  else:                              # Checks if left is one of the board's right position
    return ((left%11)-1) == 9
  
def get_start_position(player, game_state):  
  if player == 1:
    if game_state[0] == 0:
      return 0
    elif game_state[1] == 0:
      return 1
    elif game_state[2] == 0:
      return 2
    elif game_state[3] == 0:
      return 3
    elif game_state[4] == 0:
      return 4
    elif game_state[5] == 0:
      return 5
    elif game_state[6] == 0:
      return 6
    elif game_state[7] == 0:
      return 7
    elif game_state[8] == 0:
      return 8
    elif game_state[9] == 0:
      return 9
    elif game_state[10] == 0:
      return 10
  else:
    if game_state[0] == 0:
      return 0
    elif game_state[11] == 0:
      return 11
    elif game_state[22] == 0:
      return 22
    elif game_state[33] == 0:
      return 33
    elif game_state[44] == 0:
      return 44
    elif game_state[55] == 0:
      return 55
    elif game_state[66] == 0:
      return 66
    elif game_state[77] == 0:
      return 77
    elif game_state[88] == 0:
      return 88  
    elif game_state[99] == 0:
      return 99
    elif game_state[110] == 0:
      return 110

def get_neighbours(move):
  # Left side of the board = 0, 11, 22, 33, ..., 110
  if move%11 == 0: 
    neighbours = [move - 11,
                  move - 10,
                  move + 1,
                  move + 11]
  # Right side of the board = 10, 21, 32, ..., 120
  elif ((move%11)-1) == 9:
    neighbours = [move - 11,
                  move - 1,
                  move + 10,
                  move + 11]
  # All the other neighbours
  else:
    neighbours = [move - 11,
                  move - 10,
                  move - 1,
                  move + 1,
                  move + 10,
                  move + 11]    
  return [n for n in neighbours if n > 0 and n < 121]
  
def get_graph(player, game_state):
  adjacents = {}
  cost = {}    
  
  if player == 1:
    cost_player1 = 2
    cost_player2 = float('inf')
  else:
    cost_player1 = float('inf')
    cost_player2 = 2

  for move in range(0,121):
    neighbours = get_neighbours(move)
    adjacents[move] = neighbours
    for neighbour in neighbours:
      if game_state[neighbour] == 0:    # Free space
        cost[(move, neighbour)] = 1
      elif game_state[neighbour] == 1:  # Player 1 has made a move in this position
        cost[(move, neighbour)] = cost_player1
      else:                             # Player 2 has made a move in this position
        cost[(move, neighbour)] = cost_player2
  return adjacents, cost
    
def get_available_moves(game_state):
  children = []
  upper_limit = 120
  for i in range(upper_limit):
    children.append(i)      # Store position in which it's posible to make a move
  return children
    
def evaluate(player, game_state):
  adjacents, cost = get_graph(player, game_state)  
  start = get_start_position(player, game_state)
  if player == 1:
    end = start + 110
  else:
    end = start + 10
  predecessors, min_cost = dijkstra(player, adjacents, cost, start, end)
  return min_cost
"""
def main(argv):
  board = [0] * 121
  board[1] = 1
  board[12] = 1
  board[23] = 1
  board[10] = 1
  player = 2
  s = time.time()
  result = evaluate(player, board)
  e = time.time()
  print(e-s)
  print 'evaluate: ', result
  
if __name__ == "__main__":
    main(sys.argv)
"""