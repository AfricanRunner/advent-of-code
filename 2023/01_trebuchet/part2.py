import sys

NUMBERS = [('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'),
           ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'),
           ('nine', '9')]
REVERSED_NUMBERS = [(number[::-1], value) for (number, value) in NUMBERS]


def get_first_digit(line, alternative_digits):
    for i in range(len(line)):
        if line[i].isdigit():
            return line[i]
        for number, value in alternative_digits:
            if line[i:].startswith(number):
                return value
    return ""


def main(input: list[str]):
    digits = [
        get_first_digit(line, NUMBERS) +
        get_first_digit(line[::-1], REVERSED_NUMBERS) for line in input
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
