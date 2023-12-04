import re
import sys
from dataclasses import dataclass

VALVE_RE = 'Valve ([A-Z]{2}) has flow rate=(\\d+); tunnels? leads? to valves? (.+)'
MAX_DISTANCE = 1_000_000
START_VALVE = 'AA'


@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbors: list[str]

    @staticmethod
    def parse(input: str) -> 'Valve | None':
        if match := re.match(VALVE_RE, input):
            name = match.group(1)
            flow_rate = int(match.group(2))
            neighbors = [
                neighbor.strip() for neighbor in match.group(3).split(',')
            ]
            return Valve(name, flow_rate, neighbors)
        return None


def get_distances(valves: list[Valve]) -> list[list[int]]:
    dist = [
        [MAX_DISTANCE for _ in range(len(valves))] for _ in range(len(valves))
    ]
    index_of_valve = {valve.name: index for index, valve in enumerate(valves)}
    for i, valve in enumerate(valves):
        dist[i][i] = 0
        for neighbor in valve.neighbors:
            j = index_of_valve[neighbor]
            dist[i][j] = 1

    for k in range(len(valves)):
        for i in range(len(valves)):
            dist_ik = dist[i][k]
            if dist_ik == MAX_DISTANCE:
                continue
            for j in range(len(valves)):
                dist_ij_via_k = dist_ik + dist[k][j]
                if dist[i][j] > dist_ij_via_k:
                    dist[i][j] = dist_ij_via_k

    return dist


def filter_out_zero_flow_rate(valves: list[Valve], distances: list[list[int]]):
    i = 1
    while i < len(valves):
        if not valves[i].flow_rate == 0 or valves[i].name == START_VALVE:
            i += 1
            continue

        valves = valves[:i] + valves[i + 1:]
        distances = distances[:i] + distances[i + 1:]
        for j in range(len(distances)):
            distances[j] = distances[j][:i] + distances[j][i + 1:]
    return valves, distances


def order_by_potential_pressure(valves: list[Valve], distances: list[list[int]],
                                time_remaining: int,
                                start_index: int) -> list[int]:
    potential_pressures = [
        max(0, valves[index].flow_rate * (time_remaining - distance - 1))
        for index, distance in enumerate(distances[start_index])
    ]
    return []


def get_upper_bound_pressure(valves: list[Valve], distances: list[list[int]],
                             open_valves: list[bool], time_remaining: int,
                             a_target_index: int, a_trave_time: int,
                             b_target_index: int, b_trave_time: int) -> int:
    upper_bound = 0
    for index, valve in enumerate(valves):
        if open_valves[index]:
            continue

        a_pressure = max(
            0, valve.flow_rate * time_remaining -
            distances[a_target_index][index] - 1 - a_trave_time)
        b_pressure = max(
            0, valve.flow_rate * time_remaining -
            distances[b_target_index][index] - 1 - b_trave_time)

        upper_bound += min(a_pressure, b_pressure)
    return upper_bound


def get_max_pressure(valves: list[Valve], distances: list[list[int]],
                     open_valves: list[bool], time_remaining: int,
                     a_target_index: int, a_trave_time: int,
                     b_target_index: int, b_trave_time: int, best_pressure: int,
                     current_pressure: int, current_flow_rate: int) -> int:

    if time_remaining == 0:
        # Maybe return max of current and best for better pruning?
        return max(current_pressure, best_pressure)
        # return current_pressure
    upper_bound = current_pressure + current_flow_rate * time_remaining + get_upper_bound_pressure(
        valves, distances, open_valves, time_remaining, a_target_index,
        a_trave_time, b_target_index, b_trave_time)
    if upper_bound < best_pressure:
        return best_pressure

    if a_trave_time == 0 and b_trave_time == 0 and not open_valves[
            a_target_index] and not open_valves[b_target_index]:
        open_valves[a_target_index] = True
        open_valves[b_target_index] = True

        added_flow_rate = valves[a_target_index].flow_rate
        if a_target_index != b_target_index:
            added_flow_rate += valves[b_target_index].flow_rate

        pressure = get_max_pressure(valves, distances, open_valves,
                                    time_remaining - 1, a_target_index,
                                    a_trave_time, b_target_index, b_trave_time,
                                    best_pressure,
                                    current_pressure + current_flow_rate,
                                    current_flow_rate + added_flow_rate)

        open_valves[a_target_index] = False
        open_valves[b_target_index] = False
        return pressure
    elif a_trave_time == 0 and open_valves[a_target_index]:
        for index, valve in enumerate(valves):
            if open_valves[index]:
                continue
            travel_time = distances[a_target_index][index]
            if travel_time + 1 > time_remaining:
                continue

            time_passed = min(travel_time, b_trave_time)

            new_best_pressure = get_max_pressure(
                valves, distances, open_valves, time_remaining - time_passed,
                index, travel_time - time_passed, b_target_index,
                b_trave_time - time_passed, best_pressure,
                current_pressure + time_passed * current_flow_rate,
                current_flow_rate)

            if new_best_pressure > best_pressure:
                best_pressure = new_best_pressure
    if b_trave_time == 0 and open_valves[b_target_index]:
        for index, valve in enumerate(valves):
            if open_valves[index]:
                continue
            travel_time = distances[b_target_index][index]
            if travel_time + 1 > time_remaining:
                continue

            time_passed = min(travel_time, a_trave_time)

            new_best_pressure = get_max_pressure(
                valves, distances, open_valves, time_remaining - time_passed,
                a_target_index, a_trave_time - time_passed, index,
                travel_time - time_passed, best_pressure,
                current_pressure + time_passed * current_flow_rate,
                current_flow_rate)

            if new_best_pressure > best_pressure:
                best_pressure = new_best_pressure
    if a_trave_time == 0 and not open_valves[a_target_index]:
        open_valves[a_target_index] = True

        pressure = get_max_pressure(
            valves, distances, open_valves, time_remaining - 1, a_target_index,
            a_trave_time, b_target_index, b_trave_time - 1, best_pressure,
            current_pressure + current_flow_rate,
            current_flow_rate + valves[a_target_index].flow_rate)

        open_valves[a_target_index] = False

        return pressure
    if b_trave_time == 0 and not open_valves[b_target_index]:
        open_valves[b_target_index] = True

        pressure = get_max_pressure(
            valves, distances, open_valves, time_remaining - 1, a_target_index,
            a_trave_time - 1, b_target_index, b_trave_time, best_pressure,
            current_pressure + current_flow_rate,
            current_flow_rate + valves[b_target_index].flow_rate)

        open_valves[b_target_index] = False

        return pressure

    do_nothing_pressure = time_remaining * current_flow_rate + current_pressure
    if do_nothing_pressure > best_pressure:
        print(f'{do_nothing_pressure = }')
        return do_nothing_pressure

    return best_pressure


# To-do: Make faster. Maybe by exploring valves in the order of their potential
# pressure release given the time to reach them and the time remaining, we
# would end up with better results sooner which would help prune out bad orders
# faster.
def main(input: list[str]):
    valves = [Valve.parse(line) for line in input]
    distances = get_distances(valves)
    valves, distances = filter_out_zero_flow_rate(valves, distances)
    start_index = -1
    for index, valve in enumerate(valves):
        if valve.name == START_VALVE:
            start_index = index
            break
    print(
        get_max_pressure(valves, distances,
                         [i == start_index for i in range(len(valves))], 26,
                         start_index, 0, start_index, 0, 0, 0, 0))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
