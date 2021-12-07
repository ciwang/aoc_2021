from functools import reduce
from operator import xor
import numpy as np


def bit_arr_to_int(arr):
    return int("".join(map(str, arr)), 2)


def most_common_bit(arr):
    return int(sum(arr) >= len(arr)/2)


def least_common_bit(arr):
    return xor(most_common_bit(arr), 1)


# Part 1
with open("input.txt") as f:
    input_strs = f.readlines()
input_bits = np.array([[int(c) for c in s.strip()] for s in input_strs])
n_vals, n_pos = input_bits.shape

gamma = bit_arr_to_int(np.apply_along_axis(most_common_bit, 0, input_bits))
epsilon = bit_arr_to_int(np.apply_along_axis(least_common_bit, 0, input_bits))
print(f"""
gamma: {gamma}
epsilon: {epsilon}
power consumption: {gamma * epsilon}
""")


# Part 2
def find_rating(criteria):
    masks = [True] * n_vals
    for pos in range(n_pos):
        val = criteria(input_bits[masks, pos])
        masks = masks & (input_bits[:, pos] == val)
        if sum(masks) == 1:
            break
    return bit_arr_to_int(input_bits[masks].flatten())


ogr = find_rating(most_common_bit)
csr = find_rating(least_common_bit)
print(f"""
oxygen: {ogr}
co2: {csr}
life support rating: {ogr * csr}
""")
