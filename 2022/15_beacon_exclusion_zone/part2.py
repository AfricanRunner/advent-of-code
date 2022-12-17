import re
import sys
import math
from dataclasses import dataclass
from range import Range

LINE_REGEX = '^Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)$'


@dataclass(eq=True, frozen=True)
class Vec:
    x: int
    y: int

    def distance(first: 'Vec', second: 'Vec') -> int:
        return abs(first.x - second.x) + abs(first.y - second.y)

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


@dataclass(eq=True, frozen=True)
class Line:
    m: int
    b: int

    def evaluate(self, value: int) -> int:
        return self.m * value + self.b

    def manhattan_distance(self, pos: Vec) -> int:
        return abs(pos.y - self.evaluate(pos.x))

    def __repr__(self) -> str:
        return f'y = {self.m}x + {self.b}'


def round_inwards(first: float, second: float) -> (int, int):
    first, second = min(first, second), max(first, second)
    return int(math.ceil(first)), int(math.floor(second))


class SensorRegion:

    def __init__(self, center: Vec, distance: int):
        self._center = center
        self._distance = distance

    def intersects(self, line: Line) -> bool:
        return line.manhattan_distance(self._center) <= self._distance

    def get_intercepts(self, line: Line) -> (Vec, Vec):
        x_0 = (line.m * self._center.x + self._center.y - self._distance -
               line.b) / (2 * line.m)
        x_1 = (line.m * self._center.x + self._center.y + self._distance -
               line.b) / (2 * line.m)
        x_0, x_1 = round_inwards(x_0, x_1)
        return (Vec(x_0, line.evaluate(x_0)), Vec(x_1, line.evaluate(x_1)))

    def get_tangential_lines(self) -> list[Line]:
        line1 = Line(1, self._center.y - self._center.x + self._distance + 1)
        line2 = Line(1, self._center.y - self._center.x - self._distance - 1)
        line3 = Line(-1, self._center.y + self._center.x + self._distance + 1)
        line4 = Line(-1, self._center.y + self._center.x - self._distance - 1)
        return [line1, line2, line3, line4]

    def __repr__(self) -> str:
        return f'Sensor: {str(self._center)} -> {self._distance}'


def parse_line(line: str) -> (Vec, Vec):
    if match := re.match(LINE_REGEX, line):
        sensor = Vec(int(match.group(1)), int(match.group(2)))
        beacon = Vec(int(match.group(3)), int(match.group(4)))
        return sensor, beacon
    raise ValueError('Invalid input line!')


def get_range_in_box(line: Line, box: int) -> (int, int):
    if line.b < 0:
        return (-line.b, box)
    else:
        return (0, box - line.b)


def get_gap_in_range(range: Range, line: Line, box: int) -> int | None:
    if abs(line.b) > box:
        return None
    start, end = get_range_in_box(line, box)
    return range.get_gap(start, end)


def get_sensor(sensor: Vec, beacon: Vec) -> SensorRegion:
    return SensorRegion(sensor, Vec.distance(sensor, beacon))


def main(input: list[str]):
    # bounding_box = 20
    bounding_box = 4_000_000
    positions = [parse_line(line) for line in input]
    sensors = [get_sensor(sensor, beacon) for sensor, beacon in positions]
    for target_sensor in sensors:
        for line in target_sensor.get_tangential_lines():
            range = Range()
            for sensor in sensors:
                if sensor.intersects(line):
                    start, end = sensor.get_intercepts(line)
                    range.add(start.x, end.x)
            if gap := get_gap_in_range(range, line, bounding_box):
                x, y = gap, line.evaluate(gap)
                if 0 <= x <= bounding_box and 0 <= y <= bounding_box:
                    print(x * 4_000_000 + y)
                    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
