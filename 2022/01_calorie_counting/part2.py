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
    total_calories = sum_calories(input)
    total_calories.sort()
    print(total_calories[-1] + total_calories[-2] + total_calories[-3])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
