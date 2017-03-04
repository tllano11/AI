#!/usr/bin/python
import numpy as np

def getNext(node, parent):
    if (node == 'B') or (node == 'E'):
        if parent == 0:
            return 'C'
        else:
            return 'e'
    elif node == 'C':
        if parent == 'B':
            return np.random.choice(['A', 'E', 'D'], p=[0.1, 0.1, 0.8])
        elif parent == 'E':
            return np.random.choice(['A', 'B', 'D'], p=[0.1, 0.1, 0.8])



def addV(node, parent, V):
    if node == 'A':
        reward = np.int64(-10)
        V[0][0] += reward
        V[1][0] += 1
        return reward
    elif node == 'D':
        reward = np.int64(10)
        V[0][3] += reward
        V[1][3] += 1
        return reward
    elif node == 'C':
        next = getNext(node, parent)
        reward = np.int64(-1)
        accum = reward + addV(next, parent, V)
        V[0][2] += accum
        V[1][2] += 1
        return accum
    elif node == 'B':
        next = getNext(node, parent)
        reward = np.int64(-1)
        if next == 'e':
            accum = reward
        else:
            accum = reward + addV(next, 'B', V)
        V[0][1] += accum
        V[1][1] += 1
        return accum
    elif node == 'E':
        next = getNext(node, parent)
        reward = np.int64(-1)
        if next == 'e':
            accum = reward
        else:
            accum = reward + addV(next, 'E', V)
        V[0][4] += accum
        V[1][4] += 1
        return accum


baseModel = np.array([[-10, 0, 3, 0, 0],
                      [-1, 0, 0, 3, 0],
                      [-1, 1, 5, 4, 2],
                      [10, 0, 0, 0, 3],
                      [-1, 3, 0, 0, 0]]).astype("int64")

estModel = np.zeros((5,3))

V = np.array([[0,0,0,0,0], [0,0,0,0,0]])

init = ['B', 'E']
nInit = np.random.choice(init, p=[0.5, 0.5])

for i in range(0,100000):
    addV(nInit, 0, V)

for j in range(0, 5):
      V[0][j] = V[0][j]/V[1][j]

print(V)
