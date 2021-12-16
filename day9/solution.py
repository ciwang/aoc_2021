import numpy as np
from itertools import product

with open("input.txt") as f:
    input_strs = f.readlines()
heightmap = [[int(c) for c in line.strip()] for line in input_strs]
rows = len(heightmap)
cols = len(heightmap[0])


# Part 1
def get_neighbors(row, col):
    # Return list of neighbor coordinates
    neighbors = []
    if row != 0:
        neighbors.append((row-1, col))
    if row != (rows-1):
        neighbors.append((row+1, col))
    if col != 0:
        neighbors.append((row, col-1))
    if col != (cols-1):
        neighbors.append((row, col+1))
    return neighbors

def is_lowest(row, col):
    height = heightmap[row][col]
    neighbors = get_neighbors(row, col)
    return all(height < heightmap[p[0]][p[1]] for p in neighbors)

risk_sum = 0
low_points = []
for i, j in product(range(rows), range(cols)):
    if is_lowest(i, j):
        risk_sum += heightmap[i][j] + 1
        low_points.append((i, j))
print(f"Risk sum: {risk_sum}")
print(f"Num low points: {len(low_points)}")


# Part 2
# for each low point, calculate size of basin using dfs
# keep searching for higher until you hit edge or 9
# if something is already part of a previous basin we can mark it off and not search it

visited = set()

def should_search(row, col):
    if (row, col) in visited:
        return False
    if heightmap[row][col] == 9:
        return False
    return True

def find_basin(low_point):
    basin_size = 0
    to_search = [low_point]
    while len(to_search) > 0:
        curr_point = to_search.pop()
        if curr_point in visited:
            continue

        # Deal with counters
        visited.add(curr_point)
        basin_size += 1

        i, j = curr_point
        to_search += [p for p in get_neighbors(i, j) if should_search(p[0], p[1])]
    return basin_size

basin_sizes = [find_basin(p) for p in low_points]
top_basin_sizes = sorted(basin_sizes, reverse=True)
print(f"Top 3 basin sizes: {top_basin_sizes[:3]}")
print(f"Product: {top_basin_sizes[0] * top_basin_sizes[1] *  top_basin_sizes[2]}")