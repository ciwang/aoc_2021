from collections import defaultdict

with open("input.txt") as f:
    input_strs = f.readlines()

"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 """

DIGIT_TO_SEGMENTS = {
    0: set('abcefg'),
    1: set('cf'),
    2: set('acdeg'),
    3: set('acdfg'),
    4: set('bcdf'),
    5: set('abdfg'),
    6: set('abdefg'),
    7: set('acf'),
    8: set('abcdefg'),
    9: set('abcdfg')
}
DIGIT_TO_N_SEGMENTS = {
    d: len(segs) for d, segs in DIGIT_TO_SEGMENTS.items()
}
print(DIGIT_TO_N_SEGMENTS)

# Part 1
lens_1478 = {DIGIT_TO_N_SEGMENTS[d]: d for d in [1, 4, 7, 8]}
print(lens_1478)
counts_1478 = 0
for s in input_strs:
    unique_patterns, output_values = s.split(" | ")
    for v in output_values.split():
        if len(v) in lens_1478:
            counts_1478 += 1
print(counts_1478)

# Part 2
def search_for_segment(patterns, mask_out_pattern):
    result = None
    for p in patterns:
        p_minus = p - mask_out_pattern
        if len(p_minus) == 1:
            if result is not None:
                raise ValueError(
                    f"More than one segment found for patterns={patterns}, mask_out_patterns={mask_out_pattern}"
                )
            result = p_minus, p
    if result is None:
        raise ValueError(f"No segment found for patterns={patterns}, mask_out_patterns={mask_out_pattern}")
    return result

def get_output_num(output_values_, pattern_to_digit):
    digits = [pattern_to_digit[p] for p in output_values_]
    return int("".join(str(d) for d in digits))

total = 0
for s in input_strs:
    digit_to_pattern = {}
    unique_patterns, output_values = s.split(" | ")
    unique_patterns = [set(v) for v in unique_patterns.split()]
    output_values = [frozenset(v) for v in output_values.split()]
    unique_patterns_by_len = defaultdict(list)
    for p in unique_patterns:
        unique_patterns_by_len[len(p)].append(p)

    # Assign values for 1, 4, 7, 8
    for p in unique_patterns:
        if len(p) in lens_1478:
            d = lens_1478[len(p)]
            digit_to_pattern[d] = p
    cf = digit_to_pattern[1]
    a = digit_to_pattern[7] - digit_to_pattern[1]
    bd = digit_to_pattern[4] - digit_to_pattern[1]
    g, digit_to_pattern[9] = search_for_segment(unique_patterns_by_len[6], cf | a | bd)
    d, digit_to_pattern[3] = search_for_segment(unique_patterns_by_len[5], cf | a | g)
    b = bd - d
    f, digit_to_pattern[5] = search_for_segment(unique_patterns_by_len[5], a | bd | g)
    c = cf - f
    digit_to_pattern[2] = [p for p in unique_patterns_by_len[5] if p not in (digit_to_pattern[3], digit_to_pattern[5])][0]
    e = digit_to_pattern[2] - (a | c | d | g)
    digit_to_pattern[6] = a | b | d | e | f | g
    digit_to_pattern[0] = a | b | c | e | f | g

    total += get_output_num(output_values, {frozenset(p): d for d, p in digit_to_pattern.items()})
print(total)
