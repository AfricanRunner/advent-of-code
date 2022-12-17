import re
import sys
from dataclasses import dataclass
from range import Range

LINE_REGEX = '^Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)$'


@dataclass(eq=True, frozen=True)
class Vec:
    x: int
    y: int

    def distance(first: 'Vec', second: 'Vec') -> int:
        return abs(first.x - second.x) + abs(first.y - second.y)


def find_positions_without_beacon(sensor: Vec, beacon: Vec,
                                  row: int) -> tuple[int, int] | None:
    beacon_distance = Vec.distance(sensor, beacon)
    row_distance = Vec.distance(Vec(sensor.x, row), sensor)
    if row_distance > beacon_distance:
        return None
    start_x = sensor.x - (beacon_distance - row_distance)
    end_x = sensor.x + (beacon_distance - row_distance)
    return (start_x, end_x)


def parse_line(line: str) -> (Vec, Vec):
    if match := re.match(LINE_REGEX, line):
        sensor = Vec(int(match.group(1)), int(match.group(2)))
        beacon = Vec(int(match.group(3)), int(match.group(4)))
        return sensor, beacon
    raise ValueError('Invalid input line!')


def main(input: list[str]):
    target_row = 2_000_000
    # target_row = 10
    positions = [parse_line(line) for line in input]
    invalid_beacons = Range()
    for sensor, beacon in positions:
        result = find_positions_without_beacon(sensor, beacon, target_row)
        if result is None:
            continue
        start, end = result
        invalid_beacons.add(start, end)
    beacons = set([beacon for _, beacon in positions])
    beacon_positions_in_row = sum([
        True for beacon in beacons
        if beacon.y == target_row and invalid_beacons.contains(beacon.x)
    ])
    print(invalid_beacons.count() - beacon_positions_in_row)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
