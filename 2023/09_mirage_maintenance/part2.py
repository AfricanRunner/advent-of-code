import sys


def is_all_zero(sequence: list[int]) -> bool:
    return all(value == 0 for value in sequence)


def reduce_sequence(sequence: list[int]) -> list[int]:
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def get_next(sequence: list[int]) -> int:
    total = 0
    sign = 1
    while not is_all_zero(sequence):
        total += sign * sequence[0]
        sign *= -1
        sequence = reduce_sequence(sequence)

    return total


def main(input: list[str]):
    lines = [[int(num) for num in line.strip().split(' ')] for line in input]
    print(sum(get_next(sequence) for sequence in lines))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
