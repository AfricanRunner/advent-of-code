import re
import sys

OPERATIONS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b,
}


class Monkey:

    def __init__(self, number: int, items: list[int], operation: str,
                 operation_value: int | None, test_value: int,
                 true_destination: bool, false_destination: bool):
        self._number = number
        self._items = items
        self._operation = operation
        self._operation_value = operation_value
        self._test_value = test_value
        self._true_destination = true_destination
        self._false_destination = false_destination
        self._inspections = 0
        self._test_lcm = 1

    def get_number(self) -> int:
        return self._number

    def get_test_value(self) -> int:
        return self._test_value

    def set_test_lcm(self, lcm_value):
        self._test_lcm = lcm_value

    def add_items(self, new_items: list[int]):
        self._items += new_items

    def get_inspections(self) -> int:
        return self._inspections

    def inspect(self) -> dict[int, list[int]]:
        destinations = {
            self._true_destination: [],
            self._false_destination: []
        }
        for item in self._items:
            self._inspections += 1
            if self._operation_value is None:
                item = OPERATIONS[self._operation](item, item)
            else:
                item = OPERATIONS[self._operation](item, self._operation_value)
            item %= self._test_lcm
            if item % self._test_value == 0:
                destinations[self._true_destination].append(item)
            else:
                destinations[self._false_destination].append(item)
        self._items = []
        return destinations

    def parse(input: list[str]) -> 'Monkey':
        match = re.match('^Monkey (\\d+):$', input[0])
        number = int(match.group(1))
        match = re.match('^Starting items: (.+)$', input[1])
        items = [int(item) for item in match.group(1).split(', ')]
        operation = None
        operation_value = None
        if match := re.match('^Operation: new = old (.) (\\d+)$', input[2]):
            operation = match.group(1)
            operation_value = int(match.group(2))
        elif match := re.match('^Operation: new = old (.) old$', input[2]):
            operation = match.group(1)
        match = re.match('^Test: divisible by (\\d+)$', input[3])
        test_value = int(match.group(1))
        match = re.match('^If true: throw to monkey (\\d+)$', input[4])
        true_destination = int(match.group(1))
        match = re.match('^If false: throw to monkey (\\d+)$', input[5])
        false_destination = int(match.group(1))
        return Monkey(number, items, operation, operation_value, test_value,
                      true_destination, false_destination)


def process_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        destinations = monkey.inspect()
        for destination, items in destinations.items():
            monkeys[destination].add_items(items)


def gcd_helper(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd_helper(b, a % b)


def gcd(numbers: list[int]) -> int:
    result = numbers[0]
    for number in numbers[1:]:
        result = gcd_helper(max(result, number), min(result, number))
    return result


def lcm(numbers: list[int]) -> int:
    result = 1
    for number in numbers:
        result *= number
    return result // gcd(numbers)


def main(input: str):
    monkeys = [[line.strip() for line in monkey.split('\n')]
               for monkey in input.split('\n\n')]
    monkeys = [Monkey.parse(monkey) for monkey in monkeys]
    test_values = [monkey.get_test_value() for monkey in monkeys]
    lcm_value = lcm(test_values)
    for monkey in monkeys:
        monkey.set_test_lcm(lcm_value)
    for i in range(10_000):
        process_round(monkeys)

    inspections = [monkey.get_inspections() for monkey in monkeys]
    inspections.sort()
    print(inspections[-1] * inspections[-2])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        main(input_file.read())
