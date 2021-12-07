import numpy as np


BOARD_SIZE = 5


class Board:
    def __init__(self, array):
        self.board = np.array(array)
        self.state = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

    def play(self, num):
        pos = np.nonzero(self.board == num)
        self.state[pos] = 1
        rows, cols = pos
        return self.is_winning(np.unique(rows), np.unique(cols))

    def is_winning(self, rows, cols):
        return any(self.state[r, :].all() for r in rows) or any(
            self.state[:, c].all() for c in cols
        )

    def get_score(self, last_num):
        sum_unmarked = self.board[self.state == 0].sum()
        return sum_unmarked * last_num


with open("input.txt") as f:
    numbers = np.fromstring(f.readline(), sep=",")
    boards = []
    curr_board = []
    for line in f:
        if line.strip():
            curr_board.append(np.fromstring(line, sep=" "))
        if len(curr_board) == BOARD_SIZE:
            boards.append(Board(curr_board))
            curr_board = []

turns = [0]*len(boards)
scores = [0]*len(boards)
for i, b in enumerate(boards):
    for t, n in enumerate(numbers):
        win = b.play(n)
        if win:
            turns[i] = t
            scores[i] = b.get_score(n)
            break
# Part 1
win_first_idx = np.argmin(turns)
# Part 2
win_last_idx = np.argmax(turns)
print(scores[win_first_idx])
print(scores[win_last_idx])
