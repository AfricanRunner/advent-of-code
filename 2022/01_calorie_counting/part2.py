import sys


def main(input: str):
    calorie_totals = [sum([int(item) for item in group.split()])
                      for group in input.split('\n\n')]
    calorie_totals.sort()
    print(calorie_totals[-1] + calorie_totals[-2] + calorie_totals[-3])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        main(input_file.read())
