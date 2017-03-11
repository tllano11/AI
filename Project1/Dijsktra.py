import heapq
import time

def dijkstra(adjacent, costs, sets, t):
    prior_queue = []
    min_dist = {sets: 0}
    distance_queue = {}
    predecessor = {}
    visited_set = set([sets])

    for i in adjacent.get(sets, []):
        min_dist[i] = costs[sets, i]
        item = [min_dist[i], sets, i]
        heapq.heappush(prior_queue, item)
        distance_queue[i] = item

    while prior_queue:
        cost, parent, left = heapq.heappop(prior_queue)
        if left not in visited_set:
            predecessor[left] = parent
            visited_set.add(left)
            if left == t:
                return predecessor, min_dist[left]
            for i in adjacent.get(left, []):
                if min_dist.get(i):
                    if min_dist[i] > costs[left, i] + min_dist[left]:
                        min_dist[i] =  costs[left, i] + min_dist[left]
                        distance_queue[i][0] = min_dist[i]    # decrease key
                        distance_queue[i][1] = left           # update predecessor
                        heapq._siftdown(prior_queue, 0, prior_queue.index(distance_queue[i]))
                else:
                    min_dist[i] = costs[left, i] + min_dist[left]
                    item = [min_dist[i], left, i]
                    heapq.heappush(prior_queue, item)
                    distance_queue[i] = item
    return None

def make_undirected(cost):
    ucost = {}
    for i, j in cost.iteritems():
        ucost[i] = j
        ucost[(i[1],i[0])] = j
    return ucost

if __name__=='__main__':
  
    start = time.time()
    adjacent = { 1: [2,3,6], 2: [1,3,4], 3: [1,2,4,6], 4: [2,3,5,7], 5: [4,6,7], 6: [1,3,5,7], 7: [4,5,6]}

    cost = { (1,2):7, (1,3):9, (1,6):14, (2,3):10, (2,4):15, (3,4):11, (3,6):2, (4,5):6, (5,6):9, (4,7):2, (5,7):1, (6,7):12}

    cost = make_undirected(cost)

    sets, t = 1, 7
    predecessors, min_cost = dijkstra(adjacent, cost, sets, t)
    c = t
    path = [c]
    print 'minimun cost:', min_cost
    while predecessors.get(c):
        path.insert(0, predecessors[c])
        c = predecessors[c]
    end = time.time()
    print (end-start)
    print 'shortest path:', path