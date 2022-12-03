import sys

GROUP_SIZE = 3


def find_common_item(first_sack: str, second_sack: str, third_sack) -> str:
    return set(first_sack).intersection(second_sack) \
            .intersection(third_sack).pop()


def priority(item: str) -> int:
    offset = 27 - ord('A') if item.isupper() else 1 - ord('a')
    return ord(item) + offset


def main(input: list[str]):
    groups = [input[i * GROUP_SIZE:(i + 1) * GROUP_SIZE]
              for i in range(len(input) // GROUP_SIZE)]
    badge_items = [find_common_item(*group) for group in groups]
    priorities = [priority(item) for item in badge_items]
    print(sum(priorities))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
