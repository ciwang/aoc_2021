with open("input.txt") as f:
    input_strs = [line.strip() for line in f]

ERROR_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
AUTOCOMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
OPEN = {"(", "[", "{", "<"}
CLOSE = {")", "]", "}", ">"}
BRACKET_MAP = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

def get_autocomplete_score(open_chars):
    score = 0
    for c in reversed(open_chars):
        score *= 5
        score += AUTOCOMPLETE_POINTS[BRACKET_MAP[c]]
    return score

syntax_error_score = 0
autocomplete_scores = []
for line in input_strs:
    open_stack = []
    for c in line:
        if c in OPEN:
            open_stack.append(c)
        else:
            open_c = open_stack.pop()
            # If this isn't the expected closing char, break and move on
            if c != BRACKET_MAP[open_c]:
                syntax_error_score += ERROR_POINTS[c]
                open_stack = []
                break
    if len(open_stack) != 0:
        autocomplete_scores.append(get_autocomplete_score(open_stack))

print(f"Syntax error score: {syntax_error_score}")
print(f"Median autocomplete score: {sorted(autocomplete_scores)[len(autocomplete_scores)//2]}")