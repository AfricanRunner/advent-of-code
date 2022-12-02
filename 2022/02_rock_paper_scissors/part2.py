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
        if input == 'A':
            return Shape.ROCK
        elif input == 'B':
            return Shape.PAPER
        elif input == 'C':
            return Shape.SCISSORS
        return None


class Result:
    WIN = Stats(6, 'WIN')
    DRAW = Stats(3, 'DRAW')
    LOSE = Stats(0, 'LOSE')

    def parse(input: str) -> 'Result | None':
        if input == 'X':
            return Result.LOSE
        elif input == 'Y':
            return Result.DRAW
        elif input == 'Z':
            return Result.WIN
        return None


def get_my_move(opponent_move: Shape, desired_result: Result) -> Shape:
    if desired_result == Result.DRAW:
        return opponent_move
    elif desired_result == Result.WIN:
        if opponent_move == Shape.ROCK:
            return Shape.PAPER
        elif opponent_move == Shape.PAPER:
            return Shape.SCISSORS
        else:  # opponent_move == Shape.SCISSORS
            return Shape.ROCK
    else:  # desired_result == Result.LOSE
        if opponent_move == Shape.ROCK:
            return Shape.SCISSORS
        elif opponent_move == Shape.PAPER:
            return Shape.ROCK
        else:  # opponent_move == Shape.SCISSORS
            return Shape.PAPER


def score(my_move: Shape, result: Result) -> int:
    return my_move.get_score() + result.get_score()


def main(input: list[str]):
    rounds = [round.split() for round in input]
    rounds = list(
        map(lambda moves: (Shape.parse(moves[0]), Result.parse(moves[1])),
            rounds))
    my_moves = [get_my_move(opponent_move, desired_result)
                for opponent_move, desired_result in rounds]
    scores = [score(my_move, result)
              for ((_, result), my_move) in zip(rounds, my_moves)]
    print(sum(scores))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
