with open("input.txt") as f:
    target_range = f.readline().strip("target_area: ")
    target_x_range, target_y_range = target_range.split(", ")
    target_x_range = tuple(int(n) for n in target_x_range.strip("x=").split(".."))
    target_y_range = tuple(int(n) for n in target_y_range.strip("y=").split(".."))


def get_total_drag(x_vel, t):
    if t > x_vel:
        drag_until_constant = x_vel * (x_vel + 1) / 2
        return drag_until_constant + (t-x_vel) * x_vel
    else:
        return t * (t + 1) / 2


def x_position(x_vel, t):
    return (x_vel * t) - get_total_drag(x_vel, t-1)


def y_position(y_vel, t):
    return (y_vel * t) - t * (t - 1) / 2


def step(x, y, x_vel, y_vel):
    x += x_vel
    y += y_vel
    x_vel = max(x_vel-1, 0)
    y_vel = y_vel-1
    return x, y, x_vel, y_vel


def will_land(x_vel, y_vel, x_range, y_range):
    x = 0
    y = 0
    max_y = 0
    while x < x_range[1] and y > y_range[0]:
        x, y, x_vel, y_vel = step(x, y, x_vel, y_vel)
        if y > max_y:
            max_y = y
        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            return True, max_y
    return False, max_y


# Part 1 -- sorry for the hack
# for _x_vel in range(15, 30):
#     for _y_vel in range(100, 150):
#         lands, max_y = will_land(_x_vel, _y_vel, target_x_range, target_y_range)
#         if lands:
#             print(_x_vel, _y_vel, max_y)


# Part 2
count = 0
for _x_vel in range(1, target_x_range[1]+1):
    for _y_vel in range(121, target_y_range[0]-1, -1):
        lands, _ = will_land(_x_vel, _y_vel, target_x_range, target_y_range)
        if lands:
            count += 1
print(count)
