from collections import Counter, defaultdict


def part_1():
    with open("input.txt") as f:
        template = f.readline().strip()
        rules = {}
        for line in f:
            if not line.strip():
                continue
            key, insertion = line.strip().split(" -> ")
            rules[key] = insertion

    def step(sequence, rules_dict):
        new_sequence = ""
        # for each bigram, see if it matches a rule
        # add the first char and the inserted char if so
        for i in range(len(sequence)):
            insert_char = rules_dict.get(sequence[i:i+2], "")
            new_sequence += sequence[i] + insert_char
        return new_sequence

    def run_steps(sequence, rules_dict, n):
        for i in range(n):
            sequence = step(sequence, rules_dict)
        return sequence

    def get_score(sequence):
        counter = Counter(sequence)
        return max(counter.values()) - min(counter.values())

    # Sample tests
    # assert run_steps(template, rules, 1) == "NCNBCHB"
    # assert run_steps(template, rules, 2) == "NBCCNBBBCBHCB"
    # assert run_steps(template, rules, 3) == "NBBBCNCCNBBNBNBBCHBHHBCHB"
    # assert run_steps(template, rules, 4) == "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"

    sequence_10 = run_steps(template, rules, 10)
    print(get_score(sequence_10))


def part_2():
    with open("input.txt") as f:
        template = f.readline().strip()
        rules = {}
        for line in f:
            if not line.strip():
                continue
            key, insertion = line.strip().split(" -> ")
            rules[key] = insertion
    template_chars = Counter(template)
    template_bigrams = defaultdict(int)
    for i in range(len(template) - 1):
        template_bigrams[template[i:i+2]] += 1

    def step(sequence_chars, sequence_bigrams, rules_dict):
        new_sequence_chars = sequence_chars.copy()
        new_sequence_bigrams = sequence_bigrams.copy()
        for bigram, count in sequence_bigrams.items():
            insert_char = rules_dict.get(bigram)
            if insert_char:
                new_sequence_bigrams[bigram] -= count
                new_sequence_bigrams[bigram[0] + insert_char] += count
                new_sequence_bigrams[insert_char + bigram[1]] += count
                new_sequence_chars[insert_char] += count
        return new_sequence_chars, new_sequence_bigrams

    def run_steps(sequence_chars, sequence_bigrams, rules_dict, n):
        for _ in range(n):
            sequence_chars, sequence_bigrams = step(sequence_chars, sequence_bigrams, rules_dict)
        return sequence_chars, sequence_bigrams

    def get_score(sequence_chars, sequence_bigrams, rules, steps):
        output_chars, output_bigrams = run_steps(sequence_chars, sequence_bigrams, rules, steps)
        return max(output_chars.values()) - min(output_chars.values())

    # Sample tests
    # assert run_steps(template_chars, template_bigrams, rules, 1)[0] == Counter("NCNBCHB")
    # assert run_steps(template_chars, template_bigrams, rules, 2)[0] == Counter("NBCCNBBBCBHCB")
    # assert run_steps(template_chars, template_bigrams, rules, 3)[0] == Counter("NBBBCNCCNBBNBNBBCHBHHBCHB")
    # assert run_steps(template_chars, template_bigrams, rules, 4)[0] == Counter("NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB")
    # assert get_score(template_chars, template_bigrams, rules, 40) == 2188189693529

    # output_chars, output_bigrams = run_steps(template_chars, template_bigrams, rules, 40)
    print(get_score(template_chars, template_bigrams, rules, 40))


part_1()
part_2()
