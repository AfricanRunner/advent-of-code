import re
import sys
from dataclasses import dataclass


@dataclass
class Procedure:
    quantity: int
    origin: int
    destination: int

    def parse(input: str) -> 'Procedure | None':
        if match := re.match("move (\\d+) from (\\d+) to (\\d+)", input):
            quantity = int(match.group(1))
            origin = int(match.group(2)) - 1
            destination = int(match.group(3)) - 1
            return Procedure(quantity, origin, destination)
        return None


class CrateStacks:

    def __init__(self, crates: list[list[str]]):
        self._crates = crates

    def count(self) -> int:
        return len(self._crates)

    def pop(self, stack: int) -> str:
        return self._crates[stack].pop()

    def peek(self, stack: int) -> str:
        return self._crates[stack][-1]

    def push(self, crate: str, stack: int):
        return self._crates[stack].append(crate)

    def shift(self, origin: int, destination: int):
        crate = self.pop(origin)
        self.push(crate, destination)

    def process(self, procedure: Procedure):
        for _ in range(procedure.quantity):
            self.shift(procedure.origin, procedure.destination)

    def __repr__(self):
        return '\n'.join([f'{index + 1}: {stack}'
                          for index, stack in enumerate(self._crates)])

    def parse(input: str) -> 'CrateStacks':
        crate_diagram = [line for line in input.split('\n')]
        crate_count = int(crate_diagram[-1].split()[-1])
        crates = [[] for _ in range(crate_count)]
        for column in reversed(range(len(crate_diagram) - 1)):
            for row in range(crate_count):
                crate = crate_diagram[column][row * 4 + 1]
                if crate == ' ':
                    continue
                crates[row].append(crate)
        return CrateStacks(crates)


def main(input: str):
    crate_diagram, procedure = input.split('\n\n')

    stacks = CrateStacks.parse(crate_diagram)
    procedures = [Procedure.parse(line)
                  for line in procedure.split('\n') if line != '']

    for procedure in procedures:
        stacks.process(procedure)

    tops = ''.join([stacks.peek(stack) for stack in range(stacks.count())])
    print(tops)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        main(input_file.read())
