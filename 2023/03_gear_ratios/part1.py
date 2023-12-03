import sys

DIRECTIONS = [(0, 1), (0, -1), (1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0),
              (-1, -1)]


# This is a mess. I know :')
def main(input: list[str]):
    numbers: list[int] = []
    for i, row in enumerate(input):
        j = 0
        while j < len(row):
            if not row[j].isdigit():
                j += 1
                continue
            j_end = j
            while j_end < len(row) and row[j_end].isdigit():
                j_end += 1

            is_part_number = False
            for k in range(j, j_end):
                for i_off, j_off in DIRECTIONS:
                    if 0 < i + i_off < len(input) and 0 < k + j_off < len(row):
                        if input[i + i_off][k + j_off] != '.' and not input[
                                i + i_off][k + j_off].isdigit():
                            is_part_number = True
                            break
                if is_part_number:
                    break
            if is_part_number:
                numbers.append(int(row[j:j_end]))
            j = j_end
    print(sum(numbers))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
