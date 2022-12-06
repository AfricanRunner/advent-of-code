import sys


def contains_unique_characters(string: str) -> bool:
    return len(set(string)) == len(string)


def find_start_marker(stream: str, sequence_size: int) -> int:
    for i in range(sequence_size, len(stream)):
        if contains_unique_characters(stream[i - sequence_size:i]):
            return i
    return -1


def main(input: list[str]):
    for line in input:
        print(find_start_marker(line, 4))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
