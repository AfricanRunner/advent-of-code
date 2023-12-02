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


LIMITS = {Color.RED: 12, Color.GREEN: 13, Color.BLUE: 14}


def is_valid_game(game: Game) -> bool:
    for subset in game.sets:
        for color, count in subset.items():
            if count > LIMITS[color]:
                return False
    return True


def main(input: list[str]):
    games = [Game.parse(line) for line in input]
    answer = sum(game.id for game in games if is_valid_game(game))
    print(answer)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
