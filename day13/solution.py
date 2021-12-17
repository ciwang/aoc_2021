import numpy as np

with open("input.txt") as f:
    r_vals = []
    c_vals = []
    instructions = []
    for line in f:
        if not line.strip():
            break
        x, y = line.strip().split(",")
        r_vals.append(int(y))
        c_vals.append(int(x))
    for line in f:
        axis, val = line.strip("fold along ").split("=")
        instructions.append((axis, int(val)))

# Make paper
rows = max(r_vals) + 1
cols = max(c_vals) + 1
paper = np.zeros((rows, cols), dtype=bool)
for r, c in zip(r_vals, c_vals):
    paper[r, c] = 1


def fold_on_horizontal(val, paper):
    rows = paper.shape[0]
    new_paper = paper[:val, :]
    for r, c in zip(*paper.nonzero()):
        if r <= val:
            continue
        new_r = rows - r - 1
        new_paper[new_r, c] = True
    return new_paper


def fold_on_vertical(val, paper):
    cols = paper.shape[1]
    new_paper = paper[:, :val]
    for r, c in zip(*paper.nonzero()):
        if c <= val:
            continue
        new_c = cols - c - 1
        new_paper[r, new_c] = True
    return new_paper


# Fold
for fold in instructions:
    axis, val = fold
    if axis == 'y':
        paper = fold_on_horizontal(val, paper)
    if axis == 'x':
        paper = fold_on_vertical(val, paper)
    print(paper.sum())

# Print nicely
for row in paper:
    row_to_print = "".join(["#" if v else "." for v in row])
    print(row_to_print)