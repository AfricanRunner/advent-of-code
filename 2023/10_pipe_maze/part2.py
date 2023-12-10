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


def find_start(maze: list[list[str]]) -> Vec:
    for x, row in enumerate(input):
        for y, value in enumerate(row):
            if value == 'S':
                return Vec(x, y)
    return Vec(-1, -1)


def enter_loop(maze: list[list[str]], start: Vec) -> Vec:
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


def follow_pipe(maze: list[list[str]], pos: Vec, prev: Vec) -> Vec:
    pipe = maze[pos.x][pos.y]
    opening_a, opening_b = PIPE_OPENINGS[pipe]
    if pos + opening_a == prev:
        return pos + opening_b
    else:
        return pos + opening_a


def get_pipe(maze: list[list[str]]) -> list[Vec]:
    start = find_start(maze)
    pipe = [start, enter_loop(maze, start)]

    while input[pipe[-1].x][pipe[-1].y] != 'S':
        pipe.append(follow_pipe(maze, pipe[-1], pipe[-2]))

    return pipe


def remove_random_pipe(maze: list[list[str]], pipe: list[Vec]):
    parts_per_row: list[list[Vec]] = [[] for _ in range(len(maze))]
    for part in pipe:
        parts_per_row[part.x].append(part)

    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if Vec(x, y) not in parts_per_row[x]:
                maze[x][y] = '.'


def flood_fill(maze: list[list[str]], filled_spots: list[list[bool]], pos: Vec):
    if pos.x < 0 or pos.x >= len(maze) or pos.y < 0 or pos.y >= len(
            maze[pos.x]):
        return
    elif filled_spots[pos.x][pos.y] or maze[pos.x][pos.y] != '.':
        return
    filled_spots[pos.x][pos.y] = True
    flood_fill(maze, filled_spots, pos + Vec(1, 0))
    flood_fill(maze, filled_spots, pos + Vec(-1, 0))
    flood_fill(maze, filled_spots, pos + Vec(0, 1))
    flood_fill(maze, filled_spots, pos + Vec(0, -1))


def flood_fill_left_helper(maze: list[list[str]],
                           filled_spots: list[list[bool]], pos: Vec, prev: Vec):
    piece = maze[pos.x][pos.y]
    # Going up
    if pos.y == prev.y and pos.x + 1 == prev.x:
        if piece == '|':
            flood_fill(maze, filled_spots, pos + Vec(0, -1))
        elif piece == 'F':
            flood_fill(maze, filled_spots, pos + Vec(0, -1))
            flood_fill(maze, filled_spots, pos + Vec(-1, 0))
    # Going left
    elif pos.x == prev.x and pos.y - 1 == prev.y:
        if piece == '-':
            flood_fill(maze, filled_spots, pos + Vec(-1, 0))
        elif piece == '7':
            flood_fill(maze, filled_spots, pos + Vec(-1, 0))
            flood_fill(maze, filled_spots, pos + Vec(0, 1))
    # Going down
    elif pos.y == prev.y and pos.x - 1 == prev.x:
        if piece == '|':
            flood_fill(maze, filled_spots, pos + Vec(0, 1))
        elif piece == 'J':
            flood_fill(maze, filled_spots, pos + Vec(0, 1))
            flood_fill(maze, filled_spots, pos + Vec(1, 0))
    # Going right
    elif pos.x == prev.x and pos.y + 1 == prev.y:
        if piece == '-':
            flood_fill(maze, filled_spots, pos + Vec(1, 0))
        elif piece == 'L':
            flood_fill(maze, filled_spots, pos + Vec(1, 0))
            flood_fill(maze, filled_spots, pos + Vec(0, -1))


def flood_fill_left(maze: list[list[str]], filled_spots: list[list[bool]],
                    pipe: list[Vec]):
    for i in range(1, len(pipe)):
        flood_fill_left_helper(maze, filled_spots, pipe[i], pipe[i - 1])
    flood_fill_left_helper(maze, filled_spots, pipe[0], pipe[-1])


def count_empty_space(maze: list[list[str]]) -> int:
    return sum(sum(1 for value in row if value == '.') for row in maze)


def count_filled_space(filled_spots: list[list[bool]]) -> int:
    return sum(sum(1 for value in row if value) for row in filled_spots)


def filled_to_edges(filled_spots: list[list[bool]]) -> bool:
    for x in range(len(filled_spots)):
        if filled_spots[x][0] or filled_spots[x][-1]:
            return True
    for y in range(len(filled_spots[0])):
        if filled_spots[0][y] or filled_spots[-1][y]:
            return True
    return False


def print_maze(maze: list[list[str]]):
    for row in maze:
        print(''.join(row))


def print_maze_filled(maze: list[list[str]], filled_spots: list[list[bool]]):
    for x, row in enumerate(maze):
        print(''.join(value if not filled_spots[x][y] else '@'
                      for y, value in enumerate(row)))


def main(input: list[str]):
    sys.setrecursionlimit(150000)
    maze = [[value for value in row] for row in input]
    pipe = get_pipe(maze)
    remove_random_pipe(maze, pipe)

    filled_spots = [[False for _ in row] for row in input]
    flood_fill_left(maze, filled_spots, pipe)

    empty_spot_count = count_empty_space(maze)
    filled_spot_count = count_filled_space(filled_spots)

    if filled_to_edges(filled_spots):
        print(empty_spot_count - filled_spot_count)
    else:
        print(filled_spot_count)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
