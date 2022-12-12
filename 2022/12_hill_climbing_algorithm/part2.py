import heapq
import sys
from dataclasses import dataclass
import math


@dataclass(eq=True, frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x + other.x, self.y + other.y)

    def distance(first: 'Vec', second: 'Vec') -> float:
        return math.sqrt((first.x - second.x)**2 + (first.y - second.y)**2)


def find_char(input: list[list[str]], char: str) -> Vec:
    for r in range(len(input)):
        for c in range(len(input[r])):
            if input[r][c] == char:
                return Vec(r, c)


class Graph:

    NEIGHBOR_OFFSETS = [Vec(0, 1), Vec(0, -1), Vec(1, 0), Vec(-1, 0)]

    def __init__(self, input: list[list[str]]):
        self._map = input
        self._start = find_char(input, 'S')
        self._end = find_char(input, 'E')

    def get_start(self) -> Vec:
        return self._start

    def get_end(self) -> Vec:
        return self._end

    def _get_height(self, pos: Vec) -> str:
        if pos == self._start:
            return ord('a') - 1
        elif pos == self._end:
            return ord('z') + 1
        return ord(self._map[pos.x][pos.y])

    def _is_valid(self, pos: Vec) -> bool:
        return 0 <= pos.x < len(self._map) and \
            0 <= pos.y < len(self._map[pos.x])

    def _is_traversable(self, start: Vec, end: Vec) -> bool:
        start_height = self._get_height(start)
        end_height = self._get_height(end)
        return end_height <= start_height + 1

    def get_traversable_neighbors(self, pos: Vec) -> list[Vec]:
        neighbors = [pos + offset for offset in Graph.NEIGHBOR_OFFSETS]
        return [
            neighbor for neighbor in neighbors if self._is_valid(neighbor)
            and self._is_traversable(pos, neighbor)
        ]

    def get_starting_positions(self) -> list[Vec]:
        starts = []
        for r in range(len(self._map)):
            for c in range(len(self._map[r])):
                height = self._map[r][c]
                if height == 'a' or height == 'S':
                    starts.append(Vec(r, c))
        return starts


@dataclass
class Node:
    position: Vec
    f: int

    def __lt__(self, other: 'Node') -> bool:
        return self.f < other.f

    def __eq__(self, other: 'Node') -> bool:
        return self.position == other.position


def reconstruct_path(came_from: dict[Vec, Vec], current: Vec) -> list[Vec]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return reversed(path)


def a_star(start: Vec, goal: Vec, graph: Graph) -> list[Vec]:
    open_set: list[Vec] = []
    heapq.heappush(open_set, Node(start, 0))

    came_from: dict[Vec, Vec] = {}

    g_score: dict[Vec, float] = {}
    g_score[start] = 0

    while open_set:
        current = heapq.heappop(open_set)
        if current.position == goal:
            return reconstruct_path(came_from, current.position)

        for neighbor in graph.get_traversable_neighbors(current.position):
            tentative_g_score = g_score[current.position] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current.position
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + Vec.distance(neighbor, goal)
                heapq.heappush(open_set, Node(neighbor, f_score))

    return []


def main(input: list[str]):
    graph = Graph(input)
    end = graph.get_end()
    starts = graph.get_starting_positions()

    # Could optimize this further by removing starts that have
    # already been traversed by a-star
    paths = [list(a_star(start, end, graph)) for start in starts]
    shortest_path = min([len(path) for path in paths if path])

    print(shortest_path - 1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
