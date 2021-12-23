from itertools import product
from heapq import heappush, heappop, heapify
import numpy as np


with open("input.txt") as f:
    risk_grid = [[int(c) for c in line.strip()] for line in f]


def neighbors(pos, rows, cols):
    row, col = pos
    neighbors = []
    if row != (rows - 1):
        neighbors.append((row + 1, col))
    if col != (cols - 1):
        neighbors.append((row, col + 1))
    if col != 0:
        neighbors.append((row, col - 1))
    if row != 0:
        neighbors.append((row - 1, col))
    return neighbors


def find_shortest_path(cost_grid):
    rows = len(cost_grid)
    cols = len(cost_grid[0])
    start = (0, 0)
    end = (rows-1, cols-1)
    pos = start
    unvisited_heap = []  # list((float("inf"), pos) for pos in product(range(rows), range(cols)))
    unvisited_set = set(product(range(rows), range(cols)))
    deleted_set = set()
    cost_map = {start: 0}
    while end in unvisited_set:
        curr_cost = cost_map[pos]
        for n in neighbors(pos, rows, cols):
            if n in unvisited_set:
                row, col = n
                n_cost = curr_cost + cost_grid[row][col]
                n_prev_cost = cost_map.get(n, float("inf"))
                if n_cost < n_prev_cost:
                    deleted_set.add((n_prev_cost, n))
                    heappush(unvisited_heap, (n_cost, n))
                    cost_map[n] = n_cost
        unvisited_set.remove(pos)  # remove this pos
        if len(unvisited_set) == 0:
            break
        _, pos = heappop(unvisited_heap)  # get min element as new pos
        if len(deleted_set) >= 10:
            # Clean up the lazy deleted elements
            unvisited_heap = [elem for elem in unvisited_heap if elem[1] not in deleted_set]
            heapify(unvisited_heap)
            deleted_set = set()
    return cost_map[end]


def expanded_grid(cost_grid):
    grid = np.array(cost_grid)
    grid_tiles = [(grid + i) % 9 for i in range(5)]
    grid_row = np.concatenate(grid_tiles, axis=0)
    grid_rows = [(grid_row + i) % 9 for i in range(5)]
    grid_complete = np.concatenate(grid_rows, axis=1)
    grid_complete[grid_complete == 0] = 9
    return grid_complete


print(find_shortest_path(risk_grid))
print(find_shortest_path(expanded_grid(risk_grid)))
