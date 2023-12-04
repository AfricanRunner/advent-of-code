import re
import sys
from dataclasses import dataclass


@dataclass
class Scratchcard:
    id: int
    winning_numbers: list[int]
    numbers: list[int]

    def matches(self) -> int:
        return len(set(self.winning_numbers).intersection(self.numbers))

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


def get_score(card_id: int, all_cards: dict[int, Scratchcard],
              history: dict[int, int]) -> int:
    matches = all_cards[card_id].matches()
    if matches == 0:
        return 1
    elif card_id in history:
        return history[card_id]
    score = 1 + sum(
        get_score(card_id + i + 1, all_cards, history) for i in range(matches))
    history[card_id] = score
    return score


def main(input: list[str]):
    cards = [Scratchcard.parse(line) for line in input]
    card_dict = {card.id: card for card in cards}
    history: dict[int, int] = {}
    score = sum(get_score(card.id, card_dict, history) for card in cards)
    print(score)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
