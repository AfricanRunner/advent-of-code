import sys
from dataclasses import dataclass


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)

    def __eq__(self, other: 'Vec') -> 'Vec':
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def sign(n: int) -> int:
    if n == 0:
        return 0
    return 1 if n > 0 else -1


def is_touching(one: Vec, two: Vec) -> bool:
    return abs(one.x - two.x) <= 1 and abs(one.y - two.y) <= 1


def get_next_pos(target: Vec, current: Vec) -> Vec:
    if is_touching(target, current):
        return current
    offset = Vec(sign(target.x - current.x), sign(target.y - current.y))
    return current + offset


class Rope:

    def __init__(self):
        self._rope = [Vec(0, 0) for _ in range(10)]

    def get_tail(self) -> Vec:
        return self._rope[-1]

    def move(self, direction: Vec):
        self._rope[0] = self._rope[0] + direction
        for i in range(len(self._rope) - 1):
            knot = self._rope[i]
            previous_knot = self._rope[i + 1]
            self._rope[i + 1] = get_next_pos(knot, previous_knot)


DIRECTIONS = {'R': Vec(1, 0), 'L': Vec(-1, 0), 'U': Vec(0, 1), 'D': Vec(0, -1)}


def main(input: list[str]):
    moves = [line.split() for line in input]
    moves = [(direction, int(distance)) for direction, distance in moves]
    rope = Rope()
    positions = set()
    for direction, distance in moves:
        direction = DIRECTIONS[direction]
        for _ in range(distance):
            rope.move(direction)
            positions.add(rope.get_tail())
    print(len(positions))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
