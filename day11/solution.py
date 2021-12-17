import numpy as np
from itertools import product

FLASH_LIMIT = 9

with open("input.txt") as f:
    input_strs = [line.strip() for line in f]
input_energies = np.array([[int(c) for c in line] for line in input_strs])
rows = len(input_energies)
cols = len(input_energies[0])


def apply_flashes(energies, flashers):
    for f in flashers:
        i, j = f
        for n_i, n_j in product(range(i-1, i+2), range(j-1, j+2)):
            if (n_i, n_j) == (i, j):
                continue
            if n_i < 0 or n_i >= rows:
                continue
            if n_j < 0 or n_j >= cols:
                continue
            energies[n_i, n_j] += 1
    return energies


def get_flashers(energies, all_flashers):
    return [
        (i, j)
        for i, j in product(range(rows), range(cols))
        if energies[i, j] > FLASH_LIMIT and (i, j) not in all_flashers
    ]


def step(energies):
    energies += 1  # Increase every energy by 1
    flashers = get_flashers(energies, [])
    all_flashers = set(flashers)
    flashes = 0
    while len(flashers) > 0:
        energies = apply_flashes(energies, flashers)
        flashes += len(flashers)
        flashers = get_flashers(energies, all_flashers)
        all_flashers.update(set(flashers))
    for f in all_flashers:
        energies[f] = 0
    return flashes, energies


def simulate(energies, steps):
    total_flashes = 0
    for s in range(steps):
        flashes, energies = step(energies)
        total_flashes += flashes
    print(energies)
    print(total_flashes)


def simulate_until_sync(energies):
    steps = 0
    flashes = 0
    while flashes != rows*cols:
        flashes, energies = step(energies)
        steps += 1
    print(steps)


simulate(input_energies, 100)
simulate_until_sync(input_energies)
