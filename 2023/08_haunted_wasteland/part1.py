import sys
import re


def main(input: list[str]):
    instructions = input[0]

    nodes: dict[str, tuple[str, str]] = {}
    for line in input[2:]:
        if match := re.match('([A-Z]{3}) = \\(([A-Z]{3}), ([A-Z]{3})\\)', line):
            source = match.group(1)
            left = match.group(2)
            right = match.group(3)
            nodes[source] = (left, right)
        else:
            print("Failed!")

    step_index = 0
    current_head = 'AAA'
    steps = 0

    while current_head != 'ZZZ':
        left, right = nodes[current_head]
        if instructions[step_index] == 'R':
            current_head = right
        else:
            current_head = left
        step_index = (step_index + 1) % len(instructions)
        steps += 1

    print(steps)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
