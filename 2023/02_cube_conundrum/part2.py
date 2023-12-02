import re
import sys
from dataclasses import dataclass
from enum import Enum, auto


class Color(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()

    @staticmethod
    def parse(input: str) -> 'Color | None':
        if input == 'red':
            return Color.RED
        elif input == 'blue':
            return Color.BLUE
        elif input == 'green':
            return Color.GREEN
        return None


@dataclass
class Game:
    id: int
    sets: list[dict[Color, int]]

    @staticmethod
    def parse(input: str) -> 'Game | None':
        if match := re.match("Game (\\d+): (.+)", input):
            id = int(match.group(1))
            sets = match.group(2)
            sets = [[
                cube.strip().split(' ') for cube in subset.strip().split(',')
            ] for subset in sets.split(';')]
            sets = [{Color.parse(cube[1]): int(cube[0])
                     for cube in subsets}
                    for subsets in sets]
            return Game(id, sets)
        return None


def minimum_cubes(game: Game) -> dict[Color, int]:
    result = {Color.RED: 0, Color.BLUE: 0, Color.GREEN: 0}
    for subset in game.sets:
        for color, count in subset.items():
            result[color] = max(count, result[color])
    return result


def set_power(cube_set: dict[Color, int]) -> int:
    result = 1
    for count in cube_set.values():
        result *= count
    return result


def main(input: list[str]):
    games = [Game.parse(line) for line in input]
    answer = sum(set_power(minimum_cubes(game)) for game in games)
    print(answer)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
