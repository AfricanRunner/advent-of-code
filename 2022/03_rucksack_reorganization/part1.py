import sys


def find_duplicate(first_compartment: str, second_compartment: str) -> str:
    return set(first_compartment).intersection(second_compartment).pop()


def priority(item: str) -> int:
    offset = 27 - ord('A') if item.isupper() else 1 - ord('a')
    return ord(item) + offset


def main(input: list[str]):
    rucksacks = [(rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:])
                 for rucksack in input]
    duplicates = [find_duplicate(first_compartment, second_compartment)
                  for first_compartment, second_compartment in rucksacks]
    priorities = [priority(duplicate) for duplicate in duplicates]
    print(sum(priorities))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
