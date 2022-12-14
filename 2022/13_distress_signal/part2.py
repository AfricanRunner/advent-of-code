import sys
from functools import cmp_to_key


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


def compare(first: list | int, second: list | int) -> int:
    if is_equal(first, second):
        return 0
    return -1 if right_order(first, second) else 1


def main(input: str):
    packets = [parse_packet(packet) for pair in input.split('\n\n')
               for packet in pair.strip().split('\n')]
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]
    packets.append(divider_packet_1)
    packets.append(divider_packet_2)
    packets.sort(key=cmp_to_key(compare))
    signal = 1
    for i, packet in enumerate(packets):
        if is_equal(packet, divider_packet_1) or is_equal(
                packet, divider_packet_2):
            signal *= i + 1
    print(signal)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        main(input_file.read())
