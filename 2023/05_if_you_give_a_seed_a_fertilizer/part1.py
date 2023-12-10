import re
import sys
from dataclasses import dataclass


@dataclass
class Interval:
    start: int
    end: int


@dataclass
class IntervalsMap:
    intervals: list[Interval]
    destination_offsets: list[int]

    def map_value(self, value: int) -> int:
        for i in range(len(self.intervals)):
            if value >= self.intervals[i].end:
                continue
            elif value >= self.intervals[i].start:
                return self.destination_offsets[i] + value - self.intervals[
                    i].start
            return value
        return value

    def add(self, interval: Interval, destination_offset: int):
        insert_index = 0
        while insert_index < len(self.intervals):
            if interval.end <= self.intervals[insert_index].start:
                break
            insert_index += 1
        self.intervals = self.intervals[:insert_index] + [
            interval
        ] + self.intervals[insert_index:]
        self.destination_offsets = self.destination_offsets[:insert_index] + [
            destination_offset
        ] + self.destination_offsets[insert_index:]

    @staticmethod
    def parse(input: list[str]) -> 'IntervalsMap':
        imap = IntervalsMap([], [])
        for line in input:
            values = line.split(' ')
            destination_offset = int(values[0])
            start = int(values[1])
            length = int(values[2])
            imap.add(Interval(start, start + length), destination_offset)
        return imap


def main(input: list[str]):
    match = re.match('seeds: (.+)', input[0])
    seeds = [int(seed) for seed in match.group(1).split(' ')]
    maps: list[IntervalsMap] = []
    previous_map_input = []
    for line in input[2:]:
        if line != '':
            if not line[0].isdigit():
                continue
            previous_map_input.append(line)
            continue
        maps.append(IntervalsMap.parse(previous_map_input))
        previous_map_input = []
    maps.append(IntervalsMap.parse(previous_map_input))

    results = []
    for seed in seeds:
        value = seed
        for m in maps:
            value = m.map_value(value)
        results.append(value)
    print(min(results))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
