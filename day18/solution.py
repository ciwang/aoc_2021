import math
from itertools import product


fname = "input.txt"
with open(fname) as f:
    input_strs = [line.strip() for line in f]


def get_value(num, i):
    val_str = ""
    while num[i].isnumeric():
        val_str += num[i]
        i += 1
    return int(val_str), len(val_str)


def get_pair(num, i):
    val_1, val_len_1 = get_value(num, i + 1)  # [
    val_2, val_len_2 = get_value(num, i+val_len_1 + 2)  # [ ,
    return (val_1, val_2), val_len_1 + val_len_2 + 3  # [ , ]


def can_explode(num):
    left_index = None
    level = 0
    i = 0
    while i < len(num):
        if num[i].isnumeric():
            left_index = i
            _, val_len = get_value(num, i)
            i += val_len
        else:
            if num[i] == '[':
                level += 1
                if level == 5:
                    return i, left_index
            elif num[i] == ']':
                level -= 1
            i += 1
    return None


def explode(num, explode_index, left_index):
    explode_pair, explode_len = get_pair(num, explode_index)

    # Add pair's right value to number to the right
    right_index = None
    for i in range(explode_index + explode_len, len(num)):
        if num[i].isnumeric():
            right_index = i
            break
    if right_index:
        right_value, right_len = get_value(num, right_index)
        num = f"{num[:right_index]}{explode_pair[1] + right_value}{num[right_index+right_len:]}"

    # Replace pair with 0
    num = f"{num[:explode_index]}0{num[explode_index+explode_len:]}"

    # Add pair's left value to number to the left
    if left_index:
        left_value, left_len = get_value(num, left_index)
        num = f"{num[:left_index]}{explode_pair[0] + left_value}{num[left_index+left_len:]}"

    return num


# num = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
# explode_index, left_index = can_explode(num)
# print(explode_index, left_index)
# print(explode(num, explode_index, left_index))


def can_split(num):
    i = 0
    while i < len(num):
        if num[i].isnumeric():
            val, val_len = get_value(num, i)
            if val >= 10:
                return i
            i += val_len
        else:
            i += 1
    return None


def split(num, split_index):
    split_val, split_len = get_value(num, split_index)
    val_1 = split_val // 2
    val_2 = math.ceil(split_val / 2)
    return f"{num[:split_index]}[{val_1},{val_2}]{num[split_index + split_len:]}"


# num = "[[[[0,7],4],[15,[0,13]]],[1,1]]"
# split_index = can_split(num)
# print(split(num, split_index))


def add(num_1, num_2):
    result = f"[{num_1},{num_2}]"
    while True:
        explode_indices = can_explode(result)
        if explode_indices is None:
            split_index = can_split(result)
            if split_index is None:
                break
            else:
                result = split(result, split_index)
        else:
            result = explode(result, *explode_indices)
    return result


# print(add("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"))


def magnitude(num) -> int:
    if type(num) == str:
        num = eval(num)
    if type(num) == int:
        return num
    if type(num) == list:
        return 3 * magnitude(num[0]) + 2 * magnitude(num[1])


# Part 1
result = input_strs[0]
for num in input_strs[1:]:
    result = add(result, num)
print(magnitude(result))


# Part 2
max_mag = max(
    magnitude(add(num_1, num_2)) for num_1, num_2 in product(input_strs, input_strs)
)
print(max_mag)
