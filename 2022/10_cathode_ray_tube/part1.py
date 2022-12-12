import re
import sys
from dataclasses import dataclass


class CPU:

    def __init__(self):
        self._register_history = [1]
        self._register = 1

    def addx(self, value):
        self._register_history.append(self._register)
        self._register += value
        self._register_history.append(self._register)

    def noop(self):
        self._register_history.append(self._register)

    def process(self, instruction: str):
        if match := re.match('^addx (-?\\d+)$', instruction):
            value = int(match.group(1))
            self.addx(value)
        elif match := re.match('^noop$', instruction):
            self.noop()
        else:
            raise RuntimeError(f'Invalid instruction: {instruction}')

    def signal_strength(self, cycle: int) -> int:
        return cycle * self._register_history[cycle - 1]


def main(input: list[str]):
    cpu = CPU()
    for instruction in input:
        cpu.process(instruction.strip())
    strength_sum = 0
    for cycle in range(20, 260, 40):
        strength_sum += cpu.signal_strength(cycle)
    print(strength_sum)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
