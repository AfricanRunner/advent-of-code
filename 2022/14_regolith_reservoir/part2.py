import sys
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)


class Material:
    AIR = '.'
    ROCK = '#'
    SAND = 'o'


class CaveWall:

    def __init__(self, rock_patterns: list[list[Vec]]):
        max_y = max([max([pos.y for pos in pattern])
                     for pattern in rock_patterns]) + 2
        min_x = 500 - max_y
        self._wall = [[Material.AIR for _ in range(2 * max_y + 1)]
                      for _ in range(max_y + 1)]
        for pattern in rock_patterns:
            for i in range(len(pattern) - 1):
                start, end = pattern[i], pattern[i + 1]
                for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                    self._wall[start.y][x - min_x] = Material.ROCK
                for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                    self._wall[y][start.x - min_x] = Material.ROCK
        self._wall[0][500 - min_x] = '+'
        for x in range(len(self._wall[-1])):
            self._wall[-1][x] = Material.ROCK
        self._min_x = min_x

    def get_height(self) -> int:
        return len(self._wall)

    def set_material(self, pos: Vec, material: str):
        self._wall[pos.y][pos.x - self._min_x] = material

    def get_material(self, pos: Vec) -> str:
        return self._wall[pos.y][pos.x - self._min_x]

    def _next_sand_pos(self, start: Vec) -> Vec:
        down = start + Vec(0, 1)
        if self.get_material(down) == Material.AIR:
            return down
        left_diagonal = start + Vec(-1, 1)
        if self.get_material(left_diagonal) == Material.AIR:
            return left_diagonal
        right_diagonal = start + Vec(1, 1)
        if self.get_material(right_diagonal) == Material.AIR:
            return right_diagonal
        return start

    def process_sand(self) -> Vec:
        falling_history = []
        current = Vec(500, 0)
        height = self.get_height()
        while current.y < height - 1:
            next = self._next_sand_pos(current)
            if next == current:
                self.set_material(current, Material.SAND)
                if not falling_history:
                    break
                current = falling_history.pop()
            else:
                falling_history.append(current)
                current = next
        return current

    def count_sand(self) -> int:
        count = 0
        for row in self._wall:
            for material in row:
                if material == Material.SAND:
                    count += 1
        return count

    def __repr__(self) -> str:
        output = ''
        for y in range(len(self._wall)):
            for x in range(len(self._wall[y])):
                output += self._wall[y][x]
            output += '\n'
        return output


def main(input: list[str]):
    rock_patters = [pattern.strip().split(' -> ') for pattern in input]
    rock_patters = [[pos.strip().split(',') for pos in pattern]
                    for pattern in rock_patters]
    rock_patters = [[Vec(int(x), int(y)) for x, y in pattern]
                    for pattern in rock_patters]
    wall = CaveWall(rock_patters)
    wall.process_sand()
    print(wall.count_sand())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
