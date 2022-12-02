import sys


class Stats:

    def __init__(self, score: int, name: str):
        self._score = score
        self._name = name

    def get_score(self) -> int:
        return self._score

    def get_name(self) -> str:
        return self._name

    def __repr__(self):
        return self.get_name()


class Shape:
    ROCK = Stats(1, 'ROCK')
    PAPER = Stats(2, 'PAPER')
    SCISSORS = Stats(3, 'SCISSORS')

    def parse(input: str) -> 'Shape | None':
        if input == 'A' or input == 'X':
            return Shape.ROCK
        elif input == 'B' or input == 'Y':
            return Shape.PAPER
        elif input == 'C' or input == 'Z':
            return Shape.SCISSORS
        return None


class Result:
    WIN = Stats(6, 'WIN')
    DRAW = Stats(3, 'DRAW')
    LOSE = Stats(0, 'LOSE')


def play(opponent_move: Shape, my_move: Shape) -> Result:
    if opponent_move == my_move:
        return Result.DRAW
    elif opponent_move == Shape.ROCK:
        return Result.WIN if my_move == Shape.PAPER else Result.LOSE
    elif opponent_move == Shape.PAPER:
        return Result.WIN if my_move == Shape.SCISSORS else Result.LOSE
    else:  # opponent_move == Shape.SCISSORS
        return Result.WIN if my_move == Shape.ROCK else Result.LOSE


def score(my_move: Shape, result: Result) -> int:
    return my_move.get_score() + result.get_score()


def main(input: list[str]):
    rounds = [round.split() for round in input]
    rounds = list(
        map(lambda moves: (Shape.parse(moves[0]), Shape.parse(moves[1])),
            rounds))
    results = [play(opponent_move, my_move)
               for opponent_move, my_move in rounds]
    scores = [score(my_move, result)
              for ((_, my_move), result) in zip(rounds, results)]
    print(sum(scores))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
