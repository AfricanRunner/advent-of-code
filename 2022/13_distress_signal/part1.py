import sys


def scan_next_item(input: str, start_index: int) -> int:
    index = start_index
    bracket_counter = 0
    while index < len(input):
        char = input[index]
        if char == '[':
            bracket_counter += 1
        elif char == ']':
            bracket_counter -= 1
            if bracket_counter == -1:
                return index
        elif char == ',' and bracket_counter == 0:
            return index
        index += 1
    return -1


def parse_packet(packet: str) -> list | int:
    if packet.isdigit():
        return int(packet)
    if packet == '[]':
        return []
    index = 1
    output = []
    while index < len(packet):
        end = scan_next_item(packet, index)
        output.append(parse_packet(packet[index:end]))
        index = end + 1
        if packet[end] == ']':
            return output
    return -1


def is_equal(first: list | int, second: list | int) -> bool:
    if type(first) is int and type(second) is int:
        return first == second
    elif type(first) is int and type(second) is list:
        return is_equal([first], second)
    elif type(first) is list and type(second) is int:
        return is_equal(first, [second])
    for f, s in zip(first, second):
        if not is_equal(f, s):
            return False
    return len(first) == len(second)


def right_order(first: list | int, second: list | int) -> bool:
    if type(first) is int and type(second) is int:
        return first < second
    elif type(first) is int and type(second) is list:
        return right_order([first], second)
    elif type(first) is list and type(second) is int:
        return right_order(first, [second])
    for f, s in zip(first, second):
        if not is_equal(f, s):
            return right_order(f, s)
    return len(first) < len(second)


def main(input: str):
    pairs = [pair.strip().split('\n') for pair in input.split('\n\n')]
    pairs = [(parse_packet(first), parse_packet(second))
             for first, second in pairs]
    correct_orders = [i + 1 for i, (first, second) in enumerate(pairs)
                      if right_order(first, second)]
    print(sum(correct_orders))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        main(input_file.read())
