import sys
from dataclasses import dataclass


@dataclass
class Range:
    lower_bound: int
    upper_bound: int

    def parse(input: str) -> 'Range | None':
        lower_bound, upper_bound = input.split('-')
        return Range(int(lower_bound), int(upper_bound))

    def contains(self, other: 'Range') -> bool:
        if self.lower_bound <= other.lower_bound and \
                self.upper_bound >= other.upper_bound:
            return True
        return False


def main(input: list[str]):
    pairs = [assignment.split(',') for assignment in input]
    ranges = [(Range.parse(first), Range.parse(second))
              for first, second in pairs]
    contains = [first.contains(second) or second.contains(first)
                for first, second in ranges]
    print(sum(contains))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
