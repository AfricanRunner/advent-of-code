import sys


# This is also a mess...
def main(input: list[str]):
    parts: dict[tuple[int, int], list[int]] = {}
    for i, row in enumerate(input):
        j = 0
        while j < len(row):
            if not row[j].isdigit():
                j += 1
                continue
            j_end = j
            while j_end < len(row) and row[j_end].isdigit():
                j_end += 1

            number = int(row[j:j_end])

            for i_off in [-1, 0, 1]:
                if 0 > i + i_off or i + i_off >= len(input):
                    continue
                for j_off in range(max(0, j - 1), min(j_end + 1, len(row))):
                    if input[i + i_off][j_off] != '.' and not input[
                            i + i_off][j_off].isdigit():
                        loc = (i + i_off, j_off)
                        if loc not in parts:
                            parts[loc] = []
                        parts[loc].append(number)
            j = j_end

    result = 0
    for loc, nums in parts.items():
        i, j = loc
        if input[i][j] == '*' and len(nums) == 2:
            result += nums[0] * nums[1]
    print(result)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
