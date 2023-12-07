import sys
from dataclasses import dataclass

CARD_STRENGTHS = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}


@dataclass
class Hand:
    cards: str
    strength: int

    def __init__(self, cards: str):
        card_counts: dict[str, int] = {}
        for card in cards:
            if card not in card_counts:
                card_counts[card] = 0
            card_counts[card] += 1

        hand_type = 0

        if len(card_counts) == 1:
            # Five of a kind
            hand_type = 7
        elif len(card_counts) == 2:
            first = next(iter(card_counts.values()))
            if first == 1 or first == 4:
                # Four of a kind
                hand_type = 5
            else:
                # Full house
                hand_type = 4
        elif len(card_counts) == 3:
            values = iter(card_counts.values())
            first = next(values)
            second = next(values)
            third = next(values)
            if first == 3 or second == 3 or third == 3:
                # Three of a kind
                hand_type = 3
            else:
                # Two pair
                hand_type = 2
        elif len(card_counts) == 4:
            # One pair
            hand_type = 1
        else:
            # High card
            hand_type = 0

        strength = hand_type
        for card in cards:
            strength = strength * 100 + CARD_STRENGTHS[card]

        self.cards = cards
        self.strength = strength


def main(input: list[str]):
    hands_bets = []
    for line in input:
        cards, bet = line.split(' ')
        hands_bets.append((Hand(cards), int(bet)))

    hands_bets.sort(key=lambda hand_bet: hand_bet[0].strength)

    result = 0
    for i, (hand, bet) in enumerate(hands_bets):
        result += (i + 1) * bet
    print(result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
