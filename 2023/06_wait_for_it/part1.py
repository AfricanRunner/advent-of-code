import sys
import math


def record_range(time: int, record_distance: int) -> tuple[int, int]:
    lower_bound = int(
        math.floor((time - math.sqrt(time * time - 4 * record_distance)) / 2 +
                   1))
    upper_bound = int(
        math.ceil((time + math.sqrt(time * time - 4 * record_distance)) / 2 -
                  1))
    return lower_bound, upper_bound


def main(input: list[str]):
    times = [
        int(time) for time in input[0].split(':')[1].strip().split(' ') if time
    ]
    distances = [
        int(distance)
        for distance in input[1].split(':')[1].strip().split(' ')
        if distance
    ]
    result = 1
    for time, distance in zip(times, distances):
        lower, upper = record_range(time, distance)
        result *= upper - lower + 1
    print(result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
