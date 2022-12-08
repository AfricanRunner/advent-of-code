import sys
from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)


NEIGHBOR_OFFSETS = [Vec(1, 0), Vec(-1, 0), Vec(0, 1), Vec(0, -1)]


class Visibility(Enum):
    VISIBLE = auto()
    HIDDEN = auto()
    UNKNOWN = auto()


class Forrest:

    def __init__(self, heights: list[list[int]]):
        self._heights = heights
        self._visibilities = [[Visibility.UNKNOWN for _ in row]
                              for row in heights]

    def get_height(self, pos) -> int:
        return self._heights[pos.x][pos.y]

    def is_inside(self, pos) -> bool:
        return 0 <= pos.x < len(self._heights) and \
            0 <= pos.y < len(self._heights[0])

    def is_on_border(self, pos) -> bool:
        return pos.x == 0 or pos.y == 0 or \
            pos.x == len(self._heights) - 1 or \
            pos.y == len(self._heights[0]) - 1

    def set_visibility(self, pos: Vec, visibility: Visibility):
        self._visibilities[pos.x][pos.y] = visibility

    def get_visibility(self, pos) -> Visibility:
        return self._visibilities[pos.x][pos.y]

    def is_tallest_from(self, pos: Vec, direction: Vec) -> bool:
        height = self.get_height(pos)
        pos = pos + direction
        while (self.is_inside(pos)):
            other_height = self.get_height(pos)
            if other_height >= height:
                return False
            pos = pos + direction
        return True

    def calculate_visibility(self, pos: Vec):
        if self.is_on_border(pos):
            self.set_visibility(pos, Visibility.VISIBLE)
            return
        for offset in NEIGHBOR_OFFSETS:
            if self.is_tallest_from(pos, offset):
                self.set_visibility(pos, Visibility.VISIBLE)
                return
        self.set_visibility(pos, Visibility.HIDDEN)

    def calculate_all_visibilities(self):
        for x in range(len(self._heights)):
            for y in range(len(self._heights[0])):
                self.calculate_visibility(Vec(x, y))

    def __repr__(self) -> str:
        return '\n'.join([
            ''.join([
                'V' if visibility == Visibility.VISIBLE else 'H'
                for visibility in row
            ]) for row in self._visibilities
        ])

    def get_visible_count(self):
        return sum([
            sum([visibility == Visibility.VISIBLE for visibility in row])
            for row in self._visibilities
        ])


def main(input: list[str]):
    heights = [[int(height) for height in row] for row in input]
    forrest = Forrest(heights)
    forrest.calculate_all_visibilities()
    print(forrest.get_visible_count())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
