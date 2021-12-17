from typing import Dict
from collections import defaultdict


class Cave:
    def __init__(self, name):
        self.name = name
        self.is_start = self.name == "start"
        self.is_end = self.name == "end"
        self.is_small = not self.is_start and not self.is_end and self.name.islower()
        self.neighbors = set()

    def add_neighbor(self, cave):
        self.neighbors.add(cave)

    def is_neighbor(self, cave):
        return cave in self.neighbors

    def __repr__(self):
        return self.name


def make_graph(_segments):
    graph: Dict[str, Cave] = {}
    for s in _segments:
        name_1, name_2 = s
        cave_1 = graph.get(name_1, Cave(name_1))
        cave_2 = graph.get(name_2, Cave(name_2))
        cave_1.add_neighbor(cave_2)
        cave_2.add_neighbor(cave_1)
        graph[name_1] = cave_1
        graph[name_2] = cave_2
    return graph


def find_valid_paths(start_cave, small_visited, path_so_far):
    # Find paths that visit small caves at most once
    if start_cave.is_end:
        # print(f"Found path: {path_so_far + ['end']}")
        return 1
    if start_cave in small_visited:
        return 0
    paths = 0
    if start_cave.is_small:
        small_visited = small_visited | {start_cave}
    for cave in start_cave.neighbors:
        if cave.is_start:
            continue
        paths += find_valid_paths(cave, small_visited, path_so_far + [start_cave])
    return paths


def find_valid_paths_2(start_cave, small_visited, path_so_far):
    # Find paths that visit one small cave at most twice, and other small caves at most once
    if start_cave.is_end:
        # print(f"Found path: {path_so_far + ['end']}")
        return 1
    if small_visited[start_cave] == 2:
        return 0
    if small_visited[start_cave] == 1 and 2 in small_visited.values():
        # Trying to visit this small cave twice but another cave has already been visited twice
        return 0
    paths = 0
    if start_cave.is_small:
        small_visited = small_visited.copy()
        small_visited[start_cave] += 1
    for cave in start_cave.neighbors:
        if cave.is_start:
            continue
        paths += find_valid_paths_2(cave, small_visited, path_so_far + [start_cave])
    return paths


segments = []
with open("input.txt") as f:
    for line in f:
        start, end = line.strip().split("-")
        segments.append((start, end))
graph = make_graph(segments)

# Part 1
n_paths = find_valid_paths(graph['start'], small_visited=set(), path_so_far=[])
print(n_paths)

# Part 2
n_paths = find_valid_paths_2(graph['start'], small_visited=defaultdict(int), path_so_far=[])
print(n_paths)
