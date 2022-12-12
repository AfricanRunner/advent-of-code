import re
import sys


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

    def is_lit(self, pixel) -> bool:
        register = self._register_history[pixel]
        return register - 1 <= (pixel % 40) <= register + 1


def main(input: list[str]):
    cpu = CPU()
    for instruction in input:
        cpu.process(instruction.strip())
    for cycle in range(0, 240, 40):
        print(''.join(['#' if cpu.is_lit(i) else '.'
                       for i in range(cycle, cycle + 40)]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
