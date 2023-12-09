import sys
import re


def first_z(instructions: str, nodes: dict[str, tuple[str, str]],
            start: str) -> int:
    step = 0
    head = start

    while head[2] != 'Z':
        left, right = nodes[head]
        if instructions[step % len(instructions)] == 'R':
            head = right
        else:
            head = left
        step += 1

    return step


def gcd(a: int, b: int) -> int:
    a, b = max(a, b), min(a, b)
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return (a * b) // gcd(a, b)


def main(input: list[str]):
    instructions = input[0]
    heads = []

    nodes: dict[str, tuple[str, str]] = {}
    for line in input[2:]:
        if match := re.match('(\\w{3}) = \\((\\w{3}), (\\w{3})\\)', line):
            source = match.group(1)
            left = match.group(2)
            right = match.group(3)
            nodes[source] = (left, right)
            if source[2] == 'A':
                heads.append(source)
        else:
            print("BAD!")

    counts = [first_z(instructions, nodes, head) for head in heads]
    result = counts[0]
    for i in range(1, len(counts)):
        result = lcm(result, counts[i])
    print(result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
