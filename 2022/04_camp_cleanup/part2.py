import sys
from dataclasses import dataclass


@dataclass
class Range:
    lower_bound: int
    upper_bound: int

    def parse(input: str) -> 'Range | None':
        lower_bound, upper_bound = input.split('-')
        return Range(int(lower_bound), int(upper_bound))

    def overlaps(self, other: 'Range') -> bool:
        if self.upper_bound < other.lower_bound or \
                other.upper_bound < self.lower_bound:
            return False
        return True


def main(input: list[str]):
    pairs = [assignment.split(',') for assignment in input]
    ranges = [(Range.parse(first), Range.parse(second))
              for first, second in pairs]
    overlaps = [first.overlaps(second) for first, second in ranges]
    print(sum(overlaps))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
