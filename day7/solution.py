import numpy as np

input_nums = np.loadtxt("input.txt", dtype=int, delimiter=",")


# Part 1
align_pos = np.median(input_nums)
fuel = 0
for n in input_nums:
    fuel += abs(align_pos - n)
print(fuel)


# Part 2
cache = {}
def fuel_cost(dist):
    if dist not in cache:
        cache[dist] = (dist+1)*dist/2
    return cache[dist]

# Pretend I did binary search instead of just checking the nums around the mean
align_pos = int(np.round(np.mean(input_nums)))
for pos in range(align_pos-2, align_pos+3):
    fuel = 0
    for n in input_nums:
        fuel += fuel_cost(abs(pos - n))
    print(fuel)
