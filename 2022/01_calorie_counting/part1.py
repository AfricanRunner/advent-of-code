import sys


def sum_calories(calories: list[str]) -> list[int]:
    totals = []
    current_total = 0
    for item in calories:
        if item == '':
            totals.append(current_total)
            current_total = 0
        else:
            current_total += int(item)
    totals.append(current_total)
    return totals


def main(input: list[str]):
    calories = sum_calories(input)
    print(max(calories))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
