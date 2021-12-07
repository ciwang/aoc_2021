import numpy as np


fish = np.loadtxt("input.txt", delimiter=",")


# Part 1
def simulate(state, days, spawn_days=6, newborn_days=8):
    for _ in range(days):
        spawners, = np.nonzero(state == 0)
        state = np.concatenate([state - 1, [newborn_days]*len(spawners)])
        state[spawners] = spawn_days
    return state


print(len(simulate(fish, days=80)))

# Part 2
cache = {}


def simulate_single(s, days):
    # How many fish does this one fish become after days?
    result = cache.get((s, days))
    if result is None:
        if days <= 0:
            return 1
        result = simulate_single(s-1 if s > 0 else 6, days-1)
        if s == 0:
            result += simulate_single(8, days-1)  # spawned fish
        cache[(s, days)] = result
    return result


total = 0
for f in fish:
    total += simulate_single(f, 256)
print(total)
