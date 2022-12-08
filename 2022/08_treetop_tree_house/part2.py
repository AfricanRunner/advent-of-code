import sys
import operator
import functools
from dataclasses import dataclass


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)


NEIGHBOR_OFFSETS = [Vec(1, 0), Vec(-1, 0), Vec(0, 1), Vec(0, -1)]


class Forrest:

    def __init__(self, heights: list[list[int]]):
        self._heights = heights
        self._scenic_scores = [[0 for _ in row] for row in heights]

    def get_height(self, pos) -> int:
        return self._heights[pos.x][pos.y]

    def is_inside(self, pos) -> bool:
        return 0 <= pos.x < len(self._heights) and \
            0 <= pos.y < len(self._heights[0])

    def set_scenic_score(self, pos: Vec, score: int):
        self._scenic_scores[pos.x][pos.y] = score

    def get_scenic_score(self, pos) -> int:
        return self._scenic_scores[pos.x][pos.y]

    def trees_visible_from(self, pos: Vec, direction: Vec) -> bool:
        height = self.get_height(pos)
        pos = pos + direction
        count = 0
        while (self.is_inside(pos)):
            other_height = self.get_height(pos)
            if other_height >= height:
                return count + 1
            count += 1
            pos = pos + direction
        return count

    def calculate_scenic_score(self, pos: Vec):
        views = [self.trees_visible_from(pos, offset)
                 for offset in NEIGHBOR_OFFSETS]
        score = functools.reduce(operator.mul, views, 1)
        self.set_scenic_score(pos, score)

    def calculate_all_scenic_scores(self):
        for x in range(len(self._heights)):
            for y in range(len(self._heights[0])):
                self.calculate_scenic_score(Vec(x, y))

    def get_best_scenic_score(self):
        return max([max(row) for row in self._scenic_scores])


def main(input: list[str]):
    heights = [[int(height) for height in row] for row in input]
    forrest = Forrest(heights)
    forrest.calculate_all_scenic_scores()
    print(forrest.get_best_scenic_score())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
