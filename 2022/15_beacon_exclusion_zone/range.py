from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Segment:
    start: int
    end: int

    def distance(self) -> int:
        return self.end - self.start + 1

    def contains(self, value: int) -> bool:
        return self.start <= value <= self.end

    def __repr__(self) -> str:
        return f'[{self.start}, {self.end}]'


class Range:

    def __init__(self):
        self._segments = []

    def add(self, start: int, end: int):
        self._add(Segment(min(start, end), max(start, end)))

    def count(self) -> int:
        return sum([segment.distance() for segment in self._segments])

    def get_gap(self, start, end) -> int | None:
        if not self._segments:
            return None
        start_index = self._find_lower_segment(start)
        segment = self._segments[start_index]
        if segment.start <= start and end <= segment.end:
            return None
        return segment.end + 1

    def contains(self, value: int) -> int:
        start = self._segments[0].start
        end = self._segments[-1].end
        if value < start or end < value:
            return False
        lower_segment = self._segments[self._find_lower_segment(value)]
        return lower_segment.start <= value and value <= lower_segment.end

    def _find_lower_segment(self, target: int) -> int:
        # To-do: Optimize with binary search
        for i, segment in enumerate(self._segments):
            if target < segment.start:
                return i - 1
        return len(self._segments) - 1

    def _find_upper_segment(self, target: int) -> int:
        # To-do: Optimize with binary search
        for i, segment in reversed(list(enumerate(self._segments))):
            if segment.end < target:
                return i + 1
        return 0

    def _merge_segments(first: Segment, second: Segment) -> list[Segment]:
        if first.end < second.start and first.end != second.start - 1:
            return [first, second]
        else:
            return [
                Segment(min(first.start, second.start),
                        max(first.end, second.end))
            ]

    def _add(self, segment: Segment):
        if not self._segments:
            self._segments.append(segment)
            return
        start = self._segments[0].start
        end = self._segments[-1].end
        if segment.end < start:
            self._segments = Range._merge_segments(
                segment, self._segments[0]) + self._segments[1:]
            return
        elif end < segment.start:
            self._segments = self._segments[:-1] + Range._merge_segments(
                self._segments[-1], segment)
            return
        elif segment.start <= start and end <= segment.end:
            self._segments = [segment]
            return
        elif segment.start <= start:
            upper_index = self._find_upper_segment(segment.end)
            upper_segment = self._segments[upper_index]
            merged_segments = Range._merge_segments(segment, upper_segment)
            self._segments = merged_segments + self._segments[upper_index + 1:]
            return
        elif end <= segment.end:
            lower_index = self._find_lower_segment(segment.start)
            lower_segment = self._segments[lower_index]
            merged_segments = Range._merge_segments(lower_segment, segment)
            self._segments = self._segments[:lower_index] + merged_segments
            return
        lower_index = self._find_lower_segment(segment.start)
        upper_index = self._find_upper_segment(segment.end)
        if lower_index == upper_index:
            return
        lower_segment = self._segments[lower_index]
        upper_segment = self._segments[upper_index]
        merged = Range._merge_segments(lower_segment, segment)
        if len(merged) == 1:
            merged = Range._merge_segments(merged[0], upper_segment)
        else:
            merged = [merged[0]] + Range._merge_segments(
                merged[1], upper_segment)
        self._segments = self._segments[:lower_index] + merged + self._segments[
            upper_index + 1:]

    def __repr__(self) -> str:
        return 'Range:' + ' U '.join(
            [str(segment) for segment in self._segments])


def main():
    range = Range()
    range.add(0, 5)
    range.add(0, 15)
    print(range)


if __name__ == '__main__':
    main()
