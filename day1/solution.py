import numpy as np

# Part 1
with open("input.txt") as f:
    n = 0
    prev = float("inf")
    for line in f:
        val = int(line)
        if val > prev:
            n += 1
        prev = val
    print(n)

# Part 2
inputs = np.loadtxt("input.txt", int)
n = 0
prev = float("inf")
for i in range(len(inputs-2)):
    val = sum(inputs[i:i+3])
    if val > prev:
        n += 1
    prev = val
print(n)