from enum import Enum
from dataclasses import dataclass


class Command(Enum):
    FORWARD = "forward"
    DOWN = "down"
    UP = "up"


# Part 1
@dataclass
class Submarine:
    pos: int = 0
    depth: int = 0

    def move(self, command: Command, units: int):
        if command == Command.FORWARD:
            self.pos += units
        elif command == Command.DOWN:
            self.depth += units
        elif command == Command.UP:
            self.depth -= units

    def get_final(self):
        return self.pos * self.depth


s = Submarine()
with open("input.txt") as f:
    for line in f:
        c, u = line.split()
        s.move(Command(c), int(u))
print(s.get_final())


# Part 2
@dataclass
class Submarine2(Submarine):
    aim: int = 0

    def move(self, command: Command, units: int):
        if command == Command.FORWARD:
            self.pos += units
            self.depth += self.aim * units
        elif command == Command.DOWN:
            self.aim += units
        elif command == Command.UP:
            self.aim -= units


s = Submarine2()
with open("input.txt") as f:
    for line in f:
        c, u = line.split()
        s.move(Command(c), int(u))
print(s.get_final())
