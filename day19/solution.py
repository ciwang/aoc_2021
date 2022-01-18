import numpy as np
from itertools import product

scanners = []
with open("input.txt") as f:
    beacons = []
    for line in f:
        if line == '\n':
            scanners.append(np.array(beacons))
            beacons = []
        elif line.startswith("--- scanner"):
            continue
        else:
            beacons.append(np.array([int(v) for v in line.strip().split(",")]))
    scanners.append(np.array(beacons))


def get_facing_orientations(s):
    orientations = [
        s,  # (x, y, z)
        s[:, [2, 1, 0]] * [-1, 1, 1],  # (-z, y, x)
        s * [-1, 1, -1],  # (-x, y, -z)
        s[:, [2, 1, 0]] * [1, 1, -1],  # (z, y, -x)
        s[:, [0, 2, 1]] * [1, -1, 1],  # (x, -z, y)
        s[:, [0, 2, 1]] * [1, 1, -1]  # (x, z, -y)
    ]
    return orientations


def get_orientations(s):
    if s.shape[1] < 3:
        return [s]
    # s is an array (n_beacons, 3)
    scanner_orientations = []
    for facing in get_facing_orientations(s):
        scanner_orientations.extend([
            facing,
            facing * [-1, -1, 1],
            facing[:, [1, 0, 2]] * [1, -1, 1],
            facing[:, [1, 0, 2]] * [-1, 1, 1]
        ])
    return scanner_orientations


def pairwise_diffs(s):
    # Get pairwise diffs between all beacons
    diffs = []
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            diffs.append((tuple(s[i]), tuple(s[j]), s[i] - s[j]))
    return diffs


def count_overlap(diff0, diff1, n_required=12):
    dists0 = set(tuple(d[2]) for d in diff0) | set(tuple(-d[2]) for d in diff0)
    dists1 = set(tuple(d[2]) for d in diff1) | set(tuple(-d[2]) for d in diff1)
    n_diffs_required = (n_required + 1) * n_required / 2
    if len(dists0.intersection(dists1)) < n_diffs_required:
        return None

    overlap_beacons0 = []
    overlap_beacons1 = []
    for b0_a, b0_b, dist0 in diff0:
        if b0_a in overlap_beacons0 or b0_b in overlap_beacons0:
            continue
        for b1_a, b1_b, dist1 in diff1:
            if b1_a in overlap_beacons1 or b1_b in overlap_beacons1:
                continue
            if np.array_equal(dist0, dist1):
                overlap_beacons0.extend([b0_a, b0_b])
                overlap_beacons1.extend([b1_a, b1_b])
                break
            if np.array_equal(-dist0, dist1):
                overlap_beacons0.extend([b0_a, b0_b])
                overlap_beacons1.extend([b1_b, b1_a])
                break
        if len(overlap_beacons0) == n_required:
            break
    return list(zip(overlap_beacons0, overlap_beacons1))


def get_offset(b0, b1):
    return np.array(b0) - np.array(b1)


def offsets_match(overlap_beacons):
    offset = get_offset(*overlap_beacons[0])
    for b0, b1 in overlap_beacons[1:]:
        if not np.array_equal(get_offset(b0, b1), offset):
            return False
    return True


def get_overlap(s0, s1, n_required=12):
    diff0 = pairwise_diffs(s0)
    for s1_rotated in get_orientations(s1):
        overlap_beacons = count_overlap(diff0, pairwise_diffs(s1_rotated), n_required)
        if overlap_beacons:
            return overlap_beacons, s1_rotated
        # else:
        #     print(f"No overlap found")
    return None, None


# def find_total_beacons(n_required=12):
#     n_beacons = sum(len(s) for s in scanners)
#     for i in range(len(scanners)):
#         for j in range(i+1, len(scanners)):
#             print(f"Comparing scanners {i}, {j}")
#             overlap_beacons = get_overlap(scanners[i], scanners[j], n_required)
#             if overlap_beacons:
#                 n_beacons -= len(overlap_beacons)
#                 print(f"Found overlap of size {len(overlap_beacons)}, n_beacons = {n_beacons}")
#                 print(overlap_beacons)
#     return n_beacons


def construct_map(n_required=12):
    abs_beacons = set(tuple(b) for b in scanners[0])
    found_scanners = {0: scanners[0]}
    remaining_scanners = list(range(1, len(scanners)))
    searched = set()
    scanner_pos = {0: np.array([0, 0, 0])}
    while len(remaining_scanners) > 0:
        for i in found_scanners:
            found = -1
            for j in remaining_scanners:
                if (i, j) in searched:
                    continue
                print(f"Comparing scanners {i}, {j}")
                searched.add((i, j))
                overlap_beacons, beacons_rotated = get_overlap(found_scanners[i], scanners[j], n_required)
                if overlap_beacons:
                    offset = get_offset(*overlap_beacons[0])
                    print(f"Found overlap of size {len(overlap_beacons)} between scanners {i} and {j}")
                    print(overlap_beacons)
                    print(f"Offset of {j} is {offset}")
                    scanner_pos[j] = offset
                    found_scanners[j] = beacons_rotated + offset
                    abs_beacons_j = set(tuple(b) for b in found_scanners[j])
                    abs_beacons.update(abs_beacons_j)
                    found = j
                    break

            if found != -1:
                remaining_scanners.remove(found)
                break

    return abs_beacons, scanner_pos


def manhattan_dist(p0, p1):
    return np.abs(p0 - p1).sum()


absolute_beacons, scanner_positions = construct_map()
print(len(absolute_beacons))
print(
    max(manhattan_dist(p0, p1) for p0, p1 in product(scanner_positions.values(), scanner_positions.values()))
)

# Goal: how many beacons are there?
# For each scanner, find any overlap
# Recover the location absolute position of all its beacons
# Add to the set of absolute beacons
