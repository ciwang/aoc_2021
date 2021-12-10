import numpy as np

input_nums = np.loadtxt("input.txt", dtype=int, delimiter=",")

with open("input.txt") as f:
    input_strs = f.readlines()
