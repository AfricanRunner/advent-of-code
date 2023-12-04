import sys
import re
from dataclasses import dataclass


@dataclass
class Scratchcard:
    id: int
    winning_numbers: list[int]
    numbers: list[int]

    def score(self) -> int:
        matches = len(set(self.winning_numbers).intersection(self.numbers))
        return 2**(matches - 1) if matches else 0

    @staticmethod
    def parse(input: str) -> 'Scratchcard | None':
        if match := re.match('^Card +(\\d+): (.+)', input):
            id = int(match.group(1))
            wn, n = match.group(2).split('|')
            winning_numbers = [
                int(num) for num in wn.strip().split(' ') if len(num)
            ]
            numbers = [int(num) for num in n.strip().split(' ') if len(num)]
            return Scratchcard(id, winning_numbers, numbers)
        return None


def main(input: list[str]):
    cards = [Scratchcard.parse(line) for line in input]
    scores = [card.score() for card in cards]
    print(sum(scores))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
