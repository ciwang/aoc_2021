import numpy as np


class Line:
    def __init__(self, line_str):
        p1, p2 = line_str.split(" -> ")
        self.x1, self.y1 = map(int, p1.split(","))
        self.x2, self.y2 = map(int, p2.split(","))

    def is_diag(self):
        return (self.x1 != self.x2) and (self.y1 != self.y2)

    def to_mask(self):
        # Returns mask of points that this line covers
        xvals = list(range(self.x1, self.x2, 1 if self.x1 < self.x2 else -1)) + [self.x2]
        yvals = list(range(self.y1, self.y2, 1 if self.y1 < self.y2 else -1)) + [self.y2]
        return yvals, xvals

    def __repr__(self):
        return f"({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})"


lines = []
xmax = 0
ymax = 0
with open("input.txt") as f:
    for l in f:
        line = Line(l)
        lines.append(line)
        xmax = max(xmax, line.x1, line.x2)
        ymax = max(ymax, line.y1, line.y2)

graph = np.zeros((ymax+1, xmax+1))
for line in lines:
    graph[line.to_mask()] += 1
print(graph)
print((graph >= 2).sum())
