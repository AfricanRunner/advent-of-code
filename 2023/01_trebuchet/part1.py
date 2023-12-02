import sys


def get_first_digit(line):
    for char in line:
        if char.isdigit():
            return char
    return ""


def main(input: list[str]):
    digits = [
        get_first_digit(line) + get_first_digit(reversed(line))
        for line in input
    ]
    answer = sum(int(number) for number in digits)
    print(answer)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
