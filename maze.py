"""
A simple maze generator using Prim's algorithm.
"""

import random
import sys

heap = [None]

def insert(item):
    global heap
    index = len(heap)
    heap.append(item)

    while index > 1:
        new = index >> 1
        if heap[new] > heap[index]:
            temp = heap[index]
            heap[index] = heap[new]
            heap[new] = temp
        else:
            break
        index = new

def extract():
    global heap

    if len(heap) == 1:
        return None
    if len(heap) == 2:
        return heap.pop()

    root = heap[1]
    heap[1] = heap.pop()
    index = 1

    while (index << 1) < len(heap):
        new = index << 1
        if new+1 < len(heap) and heap[new+1] < heap[new]:
            new += 1
        if heap[new] < heap[index]:
            temp = heap[index]
            heap[index] = heap[new]
            heap[new] = temp
        else:
            break
        index = new

    return root

# m x n maze with m and n greater than 2
m = 10
n = 10

if len(sys.argv) >= 2 and sys.argv[1].isdigit():
    m = max(3, int(sys.argv[1]))

if len(sys.argv) >= 3 and sys.argv[2].isdigit():
    n = max(3, int(sys.argv[2]))
else:
    n = m

size = m * n

maze = [[random.randint(1, 100) for i in range(2*n-1)] for j in range(2*m-1)]
maze[0][1] = float("inf")
maze[-1][-2] = float("inf")
maze[0][0] = 0
insert((maze[1][0], (2, 0), (1, 0)))
insert((maze[0][1], (0, 2), (0, 1)))

found = 1

while found < size and len(heap) > 1:
    edge = extract()
    pt = edge[1]
    el = edge[2]
    if maze[pt[0]][pt[1]] == 0:
        continue
    else:
        found += 1
        maze[pt[0]][pt[1]] = 0
        maze[el[0]][el[1]] = 0

    if pt[0]-2 >= 0:
        insert((maze[pt[0]-1][pt[1]], (pt[0]-2, pt[1]), (pt[0]-1, pt[1])))
    if pt[0]+2 < 2*m-1:
        insert((maze[pt[0]+1][pt[1]], (pt[0]+2, pt[1]), (pt[0]+1, pt[1])))
    if pt[1]-2 >= 0:
        insert((maze[pt[0]][pt[1]-1], (pt[0], pt[1]-2), (pt[0], pt[1]-1)))
    if pt[1]+2 < 2*n-1:
        insert((maze[pt[0]][pt[1]+1], (pt[0], pt[1]+2), (pt[0], pt[1]+1)))

print("# " + "#" * (2*n-1))
for i in range(2*m-1):
    print("#", end="")
    for j in range(2*n-1):
        if maze[i][j] == 0:
            print(" ", end="")
        else:
            print("#", end="")
    print("#")
print("#" * (2*n-1) + " #")
