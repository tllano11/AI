import heapq

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
        Suppose it was given to us a hex board (formatted as a flatten matrix, i.e. a list) 
        in which position number 10 is occupied by our enemy and we are playing as player 2,
        such as board[10] = 1. Therefore, the board's cost dictionary would contain:
        {..., (9, 10):Inf, (20, 10):Inf, (21, 10):Inf, ...} and there would be 120 free 
        positions in which to make a move.
        The get_start_position(2, board) function would return '0', as it is the first possible
        position in which to make a move and "end" would be set to 10 (read the "evaluation" function
        for more details). Therefore, Dijkstra's algorithm would try to stablish the minimum cost path
        to get from start to end, returning "Infinity", as all costs from 10's neighbours to itself are
        "Infinity", and passing through 21.
        To avoid Dijkstra's algorithm to return "Infinity", "is_terminal_node" would evaluate whether 21
        is at the rightmost position of the board: ((21%11)-1) == 9? or not. It is, so "end" will be now
        equal to 21 and the minimum cost path would be returned.
    '''
def is_terminal_node(player, left):
  if player == 1:                    # Checks if left is one of the board's bottom positions
    return left in range(110, 121)
  else:                              # Checks if left is one of the board's right position
    return ((left%11)-1) == 9
  
  '''
    Determines which position is suitable to be Dijkstra's algorithm starting node
    based on which player is playing. 
    If player 1 is playing, then only the board's top positions (0, 1, 2, ... , 10) 
    are considered; otherwise it is assumed player 2 is playing and only the board's
    right positions (0, 11, 22, ... , 110) are considered.
  '''
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

  '''
    Determines an specific move's near positions based on which player
    if playing.
  '''   
def get_neighbours(move):
  if move%11 == 0:             # Left side of the board = 0, 11, 22, 33, ..., 110
    neighbours = [move - 11,
                  move - 10,
                  move + 1,
                  move + 11]
  elif ((move%11)-1) == 9:     # Right side of the board = 10, 21, 32, ..., 120
    neighbours = [move - 11,
                  move - 1,
                  move + 10,
                  move + 11]
  else:                        # All the other neighbours
    neighbours = [move - 11,
                  move - 10,
                  move - 1,
                  move + 1,
                  move + 10,
                  move + 11]    
  return [n for n in neighbours if n > 0 and n < 121]
  
  '''
    Based on the graph main concept of having a group of
    nodes, their adjacents and the cost of moving from
    one of them to another, two dictionaries are returned.
    Their structure is as following:
      1) adjacents = {<node>:[<node's neighbour>, <node's neighbour>, ...]}
      2) cost = {(<source node>, <destination node>):<cost>, ...}
  '''
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
  
  '''
    Uses Dijkstra's algorithm to get a reliable heuristic regarding the
    minimum path cost to get from the top to the bottom of the board,
    if player 1, or the right to the left side of the board, if player 2.
    Remark:
      The algorithm works by iterating over a 11 x 11 flatten matrix (i.e. a list),
      which means moving across rows is done by adding 11 to a given position 
      (it also means 11 is the jump value between rows and 1 is the jump value 
      between columns).
  '''
def evaluate(player, game_state):
  adjacents, cost = get_graph(player, game_state)  
  start = get_start_position(player, game_state)
  if player == 1:
    end = start + 110  # start + ((number_of_rows - 1) * jump_between_rows)
  else:
    end = start + 10   # start + ((number_of_columns -1) * jump_between_columns)
  predecessors, min_cost = dijkstra(player, adjacents, cost, start, end)
  return min_cost