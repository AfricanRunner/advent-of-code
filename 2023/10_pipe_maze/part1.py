import sys
from dataclasses import dataclass


@dataclass(eq=True)
class Vec:
    x: int
    y: int

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)


PIPE_OPENINGS: dict[str, tuple[Vec, Vec]] = {
    'F': (Vec(0, 1), Vec(1, 0)),
    '7': (Vec(0, -1), Vec(1, 0)),
    'J': (Vec(0, -1), Vec(-1, 0)),
    'L': (Vec(0, 1), Vec(-1, 0)),
    '|': (Vec(1, 0), Vec(-1, 0)),
    '-': (Vec(0, 1), Vec(0, -1)),
}


def find_start(maze: list[str]) -> Vec:
    for x, row in enumerate(input):
        for y, value in enumerate(row):
            if value == 'S':
                return Vec(x, y)
    return Vec(-1, -1)


def enter_loop(maze: list[str], start: Vec) -> Vec:
    up = start + Vec(-1, 0)
    down = start + Vec(1, 0)
    left = start + Vec(0, -1)
    right = start + Vec(0, 1)

    if 0 <= up.x < len(maze) and 0 <= up.y < len(
            maze[up.x]) and maze[up.x][up.y] in ['|', 'F', '7']:
        return up
    elif 0 <= down.x < len(maze) and 0 <= down.y < len(
            maze[down.x]) and maze[down.x][down.y] in ['|', 'J', 'L']:
        return down
    elif 0 <= left.x < len(maze) and 0 <= left.y < len(
            maze[left.x]) and maze[left.x][left.y] in ['-', 'F', 'L']:
        return left
    elif 0 <= right.x < len(maze) and 0 <= right.y < len(
            maze[right.x]) and maze[right.x][right.y] in ['-', '7', 'J']:
        return right
    else:
        return Vec(-1, -1)


def follow_pipe(maze: list[str], pos: Vec, prev: Vec) -> Vec:
    pipe = maze[pos.x][pos.y]
    opening_a, opening_b = PIPE_OPENINGS[pipe]
    if pos + opening_a == prev:
        return pos + opening_b
    else:
        return pos + opening_a


def main(input: list[str]):
    start = find_start(input)
    steps = 1
    prev = start
    pos = enter_loop(input, start)

    while input[pos.x][pos.y] != 'S':
        prev, pos = pos, follow_pipe(input, pos, prev)
        steps += 1

    print(steps // 2)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
