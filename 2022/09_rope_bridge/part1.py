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


class Rope:

    def __init__(self):
        self._head = Vec(0, 0)
        self._tail = Vec(0, 0)

    def get_tail(self) -> Vec:
        return self._tail

    def _is_tail_touching_head(self) -> bool:
        return abs(self._head.x - self._tail.x) <= 1 and \
            abs(self._head.y - self._tail.y) <= 1

    def move(self, direction: Vec):
        previous_head = self._head
        self._head += direction
        if not self._is_tail_touching_head():
            self._tail = previous_head


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
